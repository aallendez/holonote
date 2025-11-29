output "endpoint" {
  value = aws_db_instance.this.address
}

output "port" {
  value = aws_db_instance.this.port
}

output "username" {
  value     = var.db_username
  sensitive = true
}

output "password" {
  value     = var.db_password
  sensitive = true
}
