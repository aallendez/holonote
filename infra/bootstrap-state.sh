#!/bin/bash
# Bootstrap script to create S3 bucket and DynamoDB table for Terraform state backend

set -e

REGION="eu-west-1"
BUCKET_NAME="holonote-terraform-state"
TABLE_NAME="holonote-terraform-locks"

echo "Creating S3 bucket for Terraform state..."
aws s3api create-bucket \
  --bucket "$BUCKET_NAME" \
  --region "$REGION" \
  --create-bucket-configuration LocationConstraint="$REGION" \
  2>/dev/null || echo "Bucket may already exist"

echo "Enabling versioning on S3 bucket..."
aws s3api put-bucket-versioning \
  --bucket "$BUCKET_NAME" \
  --versioning-configuration Status=Enabled

echo "Enabling encryption on S3 bucket..."
aws s3api put-bucket-encryption \
  --bucket "$BUCKET_NAME" \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

echo "Creating DynamoDB table for state locking..."
aws dynamodb create-table \
  --table-name "$TABLE_NAME" \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region "$REGION" \
  2>/dev/null || echo "Table may already exist"

echo "Waiting for DynamoDB table to be active..."
aws dynamodb wait table-exists --table-name "$TABLE_NAME" --region "$REGION" || true

echo "✅ Terraform state backend is ready!"
echo ""
echo "Next steps:"
echo "1. Run: cd infra && terraform init -migrate-state"
echo "2. This will migrate your local state to S3"
