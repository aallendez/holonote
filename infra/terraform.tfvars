# --- Frontend ---
frontend_bucket_name = "holonote-frontend-prod"

# --- Database ---
# Database credentials are retrieved from AWS Secrets Manager secret "holonote-db-login"
# The secret should contain JSON with "username" and "password" fields
db_name = "holonotedb"
# db_username and db_password retrieved from AWS Secrets Manager

# --- PROD VERSION ---
# Single version for both backend and frontend
prod_version = "1.13.7"

ecr_backend_repo = "ghcr.io/aallendez/holonote-backend"
ecr_nginx_repo   = "ghcr.io/aallendez/holonote-frontend"

# Firebase service account key is stored in AWS Secrets Manager
# Secret name: holonote-firebase-service-account-key
