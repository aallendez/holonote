# Data sources for AWS region and account
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

# Secrets Manager data sources (uncomment after secrets are created)
# data "aws_secretsmanager_secret" "db_user" {
#   name = "holonote_db_user"
# }
#
# data "aws_secretsmanager_secret" "db_password" {
#   name = "holonote_db_password"
# }

resource "aws_ecs_cluster" "this" {
  name = "holonote-cluster"
}

# IAM roles for ECS
resource "aws_iam_role" "task_execution_role" {
  name = "holonote-task-exec"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Task role for application-level permissions (S3 access for nginx)
resource "aws_iam_role" "task_role" {
  name = "holonote-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

# IAM policy for S3 access (nginx container needs to sync frontend files from S3)
resource "aws_iam_role_policy" "s3_read_policy" {
  name = "holonote-s3-read-policy"
  role = aws_iam_role.task_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:ListBucket"
      ]
      Resource = [
        "arn:aws:s3:::${var.frontend_s3_bucket}",
        "arn:aws:s3:::${var.frontend_s3_bucket}/*"
      ]
    }]
  })
}

# IAM policy for Secrets Manager access (uncomment after secrets are created)
# resource "aws_iam_role_policy" "secrets_manager_policy" {
#   name = "holonote-secrets-manager-policy"
#   role = aws_iam_role.task_execution_role.id
#
#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [{
#       Effect = "Allow"
#       Action = [
#         "secretsmanager:GetSecretValue",
#         "secretsmanager:DescribeSecret"
#       ]
#       Resource = [
#         data.aws_secretsmanager_secret.db_user.arn,
#         data.aws_secretsmanager_secret.db_password.arn
#       ]
#     }]
#   })
# }

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "nginx" {
  name              = "/ecs/holonote/nginx"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_group" "backend" {
  name              = "/ecs/holonote/backend"
  retention_in_days = 7
}

# Task definition: nginx + backend
resource "aws_ecs_task_definition" "this" {
  family                   = "holonote-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.task_execution_role.arn
  task_role_arn            = aws_iam_role.task_role.arn

  container_definitions = jsonencode([
    {
      name      = "nginx"
      image     = "${var.ecr_nginx_repo}:${var.prod_version}"
      essential = true
      portMappings = [
        { containerPort = 80 }
      ]
      environment = [
        { name = "S3_BUCKET", value = var.frontend_s3_bucket }
      ]
      dependsOn = [{
        containerName = "backend"
        condition     = "START"
      }]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.nginx.name
          "awslogs-region"        = data.aws_region.current.name
          "awslogs-stream-prefix" = "ecs"
        }
      }
    },
    {
      name      = "backend"
      image     = "${var.ecr_backend_repo}:${var.prod_version}"
      essential = true
      environment = [
        { name = "DB_HOST", value = var.db_endpoint },
        { name = "DB_PORT", value = var.db_port },
        { name = "DB_NAME", value = var.db_name },
        { name = "DB_USER", value = var.db_username },
        { name = "DB_PASSWORD", value = var.db_password }
      ]
      # Use secrets instead of environment variables after secrets are created:
      # secrets = [
      #   {
      #     name      = "DB_USER"
      #     valueFrom = data.aws_secretsmanager_secret.db_user.arn
      #   },
      #   {
      #     name      = "DB_PASSWORD"
      #     valueFrom = data.aws_secretsmanager_secret.db_password.arn
      #   }
      # ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.backend.name
          "awslogs-region"        = data.aws_region.current.name
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}

# Security group for ALB
resource "aws_security_group" "alb_sg" {
  name        = "holonote-alb-sg"
  description = "Allow HTTP traffic to ALB"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP from internet"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "holonote-alb-sg"
  }
}

# Security group for ECS tasks
resource "aws_security_group" "ecs_sg" {
  name        = "holonote-ecs-sg"
  description = "Allow ALB to reach ECS"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
    description     = "Allow traffic from ALB"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "holonote-ecs-sg"
  }
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Load balancer
resource "aws_lb" "this" {
  name               = "holonote-alb"
  load_balancer_type = "application"
  subnets            = data.aws_subnets.default.ids
  security_groups    = [aws_security_group.alb_sg.id]

  enable_deletion_protection = false

  tags = {
    Name = "holonote-alb"
  }
}

resource "aws_lb_target_group" "this" {
  name        = "holonote-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = data.aws_vpc.default.id
  target_type = "ip" # Required for ECS Fargate with awsvpc network mode

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    path                = "/nginx-health"
    protocol            = "HTTP"
    matcher             = "200"
  }

  deregistration_delay = 30

  tags = {
    Name = "holonote-tg"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.this.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this.arn
  }
}

# ECS service
resource "aws_ecs_service" "this" {
  name            = "holonote-service"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.this.arn
    container_name   = "nginx"
    container_port   = 80
  }
}
