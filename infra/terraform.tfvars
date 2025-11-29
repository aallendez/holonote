# --- Frontend ---
frontend_bucket_name = "holonote-frontend-prod"

# --- Database ---
# These credentials will be used to create the database initially.
# After DB creation, create AWS Secrets Manager secrets:
#   - holonote_db_user (with the username value)
#   - holonote_db_password (with the password value)
# Then update the backend module to use secrets instead of variables.
db_name     = "holonotedb"
db_username = ""
db_password = ""

# --- Backend images ---
# Single version for both backend and frontend (they're built together)
prod_version = "1.12.0"

ecr_backend_repo = "ghcr.io/aallendez/holonote-backend"
ecr_nginx_repo   = "ghcr.io/aallendez/holonote-frontend"
