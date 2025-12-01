#!/bin/bash
set -e

WORKSPACE_ID="$1"
WORKSPACE_ENDPOINT="$2"
ADMIN_EMAILS="$3"
DASHBOARD_FILE="$4"
REGION="$5"

echo "🚀 Setting up Grafana workspace: $WORKSPACE_ID"

# Wait for workspace to be fully ready
echo "⏳ Waiting for Grafana workspace to be ACTIVE..."
MAX_ATTEMPTS=40
ATTEMPT=0
STATUS=""
while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  STATUS=$(aws grafana describe-workspace --workspace-id "$WORKSPACE_ID" --region "$REGION" --query 'workspace.status' --output text 2>/dev/null || echo "NOT_READY")
  if [ "$STATUS" = "ACTIVE" ]; then
    echo "✅ Workspace is ACTIVE!"
    break
  fi
  ATTEMPT_NUM=$((ATTEMPT + 1))
  echo "   Attempt $ATTEMPT_NUM/$MAX_ATTEMPTS: Status is $STATUS, waiting..."
  sleep 10
  ATTEMPT=$((ATTEMPT + 1))
done

if [ "$STATUS" != "ACTIVE" ]; then
  echo "⚠️  Warning: Workspace may not be fully ready. Continuing anyway..."
fi

# Assign admin users if emails provided
if [ -n "$ADMIN_EMAILS" ] && [ "$ADMIN_EMAILS" != "[]" ] && [ "$ADMIN_EMAILS" != "" ]; then
  echo "👤 Assigning admin users..."

  # Get SSO instance ID
  SSO_INSTANCE_ARN=$(aws sso-admin list-instances --region "$REGION" --query 'Instances[0].InstanceArn' --output text 2>/dev/null || echo "")

  if [ -n "$SSO_INSTANCE_ARN" ] && [ "$SSO_INSTANCE_ARN" != "None" ] && [ "$SSO_INSTANCE_ARN" != "" ]; then
    IDENTITY_STORE_ID=$(echo "$SSO_INSTANCE_ARN" | cut -d'/' -f2)
    USER_IDS=()
    ASSIGNED_COUNT=0
    FAILED_EMAILS=()

    # Parse emails from JSON array
    EMAIL_COUNT=$(echo "$ADMIN_EMAILS" | jq 'length' 2>/dev/null || echo "0")

    # Process each email (continue even if one fails)
    EMAIL_MAX=$((EMAIL_COUNT - 1))
    for i in $(seq 0 $EMAIL_MAX 2>/dev/null || echo ""); do
      if [ -z "$i" ]; then
        break
      fi
      ADMIN_EMAIL=$(echo "$ADMIN_EMAILS" | jq -r ".[$i]" 2>/dev/null || echo "")
      if [ -z "$ADMIN_EMAIL" ] || [ "$ADMIN_EMAIL" = "null" ]; then
        continue
      fi
      echo "   Processing: $ADMIN_EMAIL"

      # Get user ID from email (continue on error)
      USER_ID=$(aws identitystore list-users \
        --identity-store-id "$IDENTITY_STORE_ID" \
        --region "$REGION" \
        --filters "AttributePath=UserName,AttributeValue=$ADMIN_EMAIL" \
        --query 'Users[0].UserId' \
        --output text 2>/dev/null || echo "") || USER_ID=""

      if [ -n "$USER_ID" ] && [ "$USER_ID" != "None" ] && [ "$USER_ID" != "" ]; then
        USER_IDS+=("$USER_ID")
        echo "   ✅ Found user ID for $ADMIN_EMAIL"
      else
        FAILED_EMAILS+=("$ADMIN_EMAIL")
        echo "   ⚠️  Could not find SSO user with email: $ADMIN_EMAIL"
      fi
    done || true

    # Assign all users at once if we found any
    if [ ${#USER_IDS[@]} -gt 0 ]; then
      # Build update instruction batch
      UPDATE_BATCH="["
      for i in "${!USER_IDS[@]}"; do
        if [ $i -gt 0 ]; then
          UPDATE_BATCH+=","
        fi
        UPDATE_BATCH+="{\"action\":\"ADD\",\"role\":\"ADMIN\",\"users\":[{\"id\":\"${USER_IDS[$i]}\",\"type\":\"SSO_USER\"}]}"
      done
      UPDATE_BATCH+="]"

      # Assign users as admin
      aws grafana update-permissions \
        --workspace-id "$WORKSPACE_ID" \
        --update-instruction-batch "$UPDATE_BATCH" \
        --region "$REGION" 2>/dev/null && \
      echo "✅ ${#USER_IDS[@]} user(s) assigned as admin!" || \
      echo "⚠️  Could not assign users automatically. Please assign manually via AWS Console."
    fi

    # Report failed emails
    if [ ${#FAILED_EMAILS[@]} -gt 0 ]; then
      echo "⚠️  Could not find SSO users for the following emails:"
      for email in "${FAILED_EMAILS[@]}"; do
        echo "   - $email"
      done
      echo "   Please assign these users manually via AWS Console:"
      echo "   Amazon Managed Grafana > Workspace > Users and groups"
    fi
  else
    echo "⚠️  Could not find SSO instance. Please assign users manually via AWS Console."
  fi
else
  echo "ℹ️  No admin emails provided. Skipping user assignment."
  echo "   To assign users as admin, go to:"
  echo "   Amazon Managed Grafana > Workspace > Users and groups"
fi

# Import dashboard via Grafana API
if [ -f "$DASHBOARD_FILE" ]; then
  echo "📊 Importing dashboard from $DASHBOARD_FILE"

  # Wait a bit more for user assignment to propagate
  if [ -n "$ADMIN_EMAILS" ] && [ "$ADMIN_EMAILS" != "[]" ] && [ "$ADMIN_EMAILS" != "" ]; then
    echo "   Waiting for user assignment to propagate..."
    sleep 15
  fi

  # Try to create API key for dashboard import
  API_KEY_NAME="terraform-auto-import-$(date +%s)"
  echo "   Creating temporary API key..."

  API_KEY_RESPONSE=$(aws grafana create-workspace-api-key \
    --workspace-id "$WORKSPACE_ID" \
    --key-name "$API_KEY_NAME" \
    --key-role ADMIN \
    --seconds-to-live 300 \
    --region "$REGION" 2>&1) || {
    echo "⚠️  Could not create API key automatically."
    echo "   This usually means you need to assign yourself as admin first."
    echo "   Steps:"
    echo "   1. Go to AWS Console > Amazon Managed Grafana > Workspace"
    echo "   2. Click 'Users and groups' > 'Assign users and groups'"
    echo "   3. Select your user and assign as Admin"
    echo "   4. Then run: terraform apply -replace=module.monitoring.null_resource.setup_grafana[0]"
    exit 0
  }

  API_KEY=$(echo "$API_KEY_RESPONSE" | jq -r '.key' 2>/dev/null || echo "")

  if [ -n "$API_KEY" ] && [ "$API_KEY" != "null" ] && [ "$API_KEY" != "" ]; then
    echo "   ✅ API key created, importing dashboard..."

    DASHBOARD_JSON=$(cat "$DASHBOARD_FILE")
    IMPORT_PAYLOAD=$(echo "$DASHBOARD_JSON" | jq -c '{dashboard: ., overwrite: true}')

    IMPORT_RESPONSE=$(curl -s -w "\n%{http_code}" \
      -X POST \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $API_KEY" \
      -d "$IMPORT_PAYLOAD" \
      "https://$WORKSPACE_ENDPOINT/api/dashboards/db")

    HTTP_CODE=$(echo "$IMPORT_RESPONSE" | tail -n1)
    BODY=$(echo "$IMPORT_RESPONSE" | sed '$d')

    if [ "$HTTP_CODE" -eq 200 ]; then
      DASHBOARD_URL=$(echo "$BODY" | jq -r '.url' 2>/dev/null || echo "")
      echo "   ✅ Dashboard imported successfully!"
      if [ -n "$DASHBOARD_URL" ] && [ "$DASHBOARD_URL" != "null" ]; then
        echo "   📍 Dashboard URL: https://$WORKSPACE_ENDPOINT$DASHBOARD_URL"
      fi
    else
      echo "   ⚠️  Dashboard import failed (HTTP $HTTP_CODE)"
      echo "   Response: $BODY"
    fi

    # Clean up API key
    aws grafana delete-workspace-api-key \
      --workspace-id "$WORKSPACE_ID" \
      --key-name "$API_KEY_NAME" \
      --region "$REGION" 2>/dev/null || true
  else
    echo "   ⚠️  Could not extract API key from response."
    echo "   Please import dashboard manually via Grafana UI."
  fi
else
  echo "⚠️  Dashboard file not found: $DASHBOARD_FILE"
fi

echo ""
echo "✅ Grafana setup complete!"
echo "🌐 Access Grafana at: https://$WORKSPACE_ENDPOINT"
