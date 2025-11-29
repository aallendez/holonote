## HOLONOTE PROD

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
module "db" {
  source      = "./modules/db"
  db_name     = var.db_name
  db_username = var.db_username
  db_password = var.db_password
}
