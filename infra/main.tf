## HOLONOTE PROD

# --- DATABASE CREDENTIALS FROM AWS SECRETS MANAGER ---
data "aws_secretsmanager_secret" "db_login" {
  name = "holonote-db-login"
}

data "aws_secretsmanager_secret_version" "db_login" {
  secret_id = data.aws_secretsmanager_secret.db_login.id
}

locals {
  db_credentials = jsondecode(data.aws_secretsmanager_secret_version.db_login.secret_string)
}

# --- FRONTEND (S3 for React SPA) ---
module "frontend" {
  source      = "./modules/frontend"
  bucket_name = var.frontend_bucket_name
}

# --- BACKEND (ECS Fargate + ALB + Task Definition) ---
# Backend creates the ECS security group that RDS will reference
module "backend" {
  source       = "./modules/backend"
  prod_version = var.prod_version

  ecr_backend_repo = var.ecr_backend_repo
  ecr_nginx_repo   = var.ecr_nginx_repo

  db_endpoint = module.db.endpoint
  db_port     = module.db.port
  db_name     = var.db_name
  db_username = module.db.username
  db_password = module.db.password
}

# --- DATABASE (RDS PostgreSQL) ---
# Migrated from Lightsail to RDS for better VPC integration and security
# DB module uses a data source to find the ECS security group by name
# This allows RDS to only accept connections from ECS tasks
# Database credentials are retrieved from AWS Secrets Manager secret "holonote-db-login"
module "db" {
  source      = "./modules/db"
  db_name     = var.db_name
  db_username = local.db_credentials.username
  db_password = local.db_credentials.password
}
