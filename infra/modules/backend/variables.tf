variable "prod_version" {
  type        = string
  description = "Production version tag for both backend and frontend images (they share the same version)"
}

variable "ecr_backend_repo" {
  type = string
}

variable "ecr_nginx_repo" {
  type = string
}

variable "db_endpoint" {
  type = string
}

variable "db_port" {
  type        = string
  description = "Database port (default: 5432 for PostgreSQL)"
}

variable "db_name" {
  type        = string
  description = "Database name"
}

variable "db_username" {
  type        = string
  description = "Database username (use variables initially, switch to secrets later)"
}

variable "db_password" {
  type        = string
  sensitive   = true
  description = "Database password (use variables initially, switch to secrets later)"
}
