# Data sources for VPC and subnets
data "aws_vpc" "default" {
  default = true
}

# Look up ECS security group by name (created by backend module)
# This data source will be evaluated at apply time, after the backend module creates the security group
data "aws_security_group" "ecs_sg" {
  name   = "holonote-ecs-sg"
  vpc_id = data.aws_vpc.default.id

  # Ensure this is evaluated after backend module creates the security group
  # Terraform will handle the dependency through the reference chain
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
  filter {
    name   = "map-public-ip-on-launch"
    values = ["false"]
  }
}

# If no private subnets exist, use all subnets (fallback)
data "aws_subnets" "all" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

locals {
  # Use private subnets if available, otherwise use all subnets
  db_subnets = length(data.aws_subnets.private.ids) > 0 ? data.aws_subnets.private.ids : data.aws_subnets.all.ids
}

# DB Subnet Group
resource "aws_db_subnet_group" "this" {
  name       = "${var.db_name}-subnet-group"
  subnet_ids = local.db_subnets

  tags = {
    Name = "${var.db_name}-subnet-group"
  }
}

# Security group for RDS - allows connections from ECS tasks
resource "aws_security_group" "rds_sg" {
  name        = "${var.db_name}-rds-sg"
  description = "Security group for RDS PostgreSQL database - allows ECS tasks"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [data.aws_security_group.ecs_sg.id]
    description     = "Allow PostgreSQL connections from ECS tasks"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "${var.db_name}-rds-sg"
  }
}

# RDS PostgreSQL Instance
resource "aws_db_instance" "this" {
  identifier            = var.db_name
  engine                = "postgres"
  engine_version        = "13.20"
  instance_class        = "db.t3.micro"
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type          = "gp2"
  storage_encrypted     = true

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  publicly_accessible    = false # Keep private for security

  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "mon:04:00-mon:05:00"

  skip_final_snapshot = true
  # Note: Set skip_final_snapshot = false and provide final_snapshot_identifier
  # if you want to create a snapshot before deletion
  deletion_protection = false

  performance_insights_enabled = false
  monitoring_interval          = 0

  tags = {
    Name = var.db_name
  }
}
