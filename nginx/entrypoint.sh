#!/bin/sh
set -e

# S3 bucket name (can be overridden via environment variable)
S3_BUCKET=${S3_BUCKET:-holonote-frontend-prod}

echo "Syncing frontend files from s3://${S3_BUCKET} to /usr/share/nginx/html..."

# Sync files from S3 to nginx html directory
aws s3 sync s3://${S3_BUCKET}/ /usr/share/nginx/html/ --delete --quiet

echo "Frontend files synced successfully."

# Start nginx
exec "$@"
