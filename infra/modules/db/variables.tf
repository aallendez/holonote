variable "db_name" {
  type = string
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
