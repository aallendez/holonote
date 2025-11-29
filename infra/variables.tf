# Frontend (S3)

variable "frontend_bucket_name" {
  type        = string
  description = "S3 bucket name for React frontend"
}

# Database (RDS PostgreSQL)

variable "db_name" {
  type        = string
  description = "Name of the RDS PostgreSQL database"
}

variable "db_username" {
  type        = string
  description = "Database admin username"
}

variable "db_password" {
  type        = string
  sensitive   = true
  description = "Database admin password"
}

# Backend (ECS)

variable "prod_version" {
  type        = string
  description = "Production version tag for both backend and frontend images (they share the same version)"
}

variable "ecr_backend_repo" {
  type        = string
  description = "Docker image repository URI for backend (e.g., ghcr.io/org/repo)"
}

variable "ecr_nginx_repo" {
  type        = string
  description = "Docker image repository URI for frontend/nginx (e.g., ghcr.io/org/repo)"
}
