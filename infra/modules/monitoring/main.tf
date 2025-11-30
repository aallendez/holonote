# Data sources
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

# --- Amazon Managed Service for Prometheus (AMP) ---
resource "aws_prometheus_workspace" "this" {
  alias = "${var.workspace_name}-amp"

  tags = {
    Name        = "${var.workspace_name}-amp"
    Environment = "production"
  }
}

# IAM policy for backend to write metrics to AMP
# Extract role name from ARN (format: arn:aws:iam::ACCOUNT:role/ROLE_NAME)
locals {
  backend_role_name = split("/", var.backend_task_role_arn)[length(split("/", var.backend_task_role_arn)) - 1]
}

resource "aws_iam_role_policy" "amp_write_policy" {
  name = "holonote-amp-write-policy"
  role = local.backend_role_name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "aps:RemoteWrite",
          "aps:QueryMetrics",
          "aps:GetSeries",
          "aps:GetLabels",
          "aps:GetMetricMetadata"
        ]
        Resource = aws_prometheus_workspace.this.arn
      }
    ]
  })
}

# --- Amazon Managed Grafana ---
resource "aws_grafana_workspace" "this" {
  name                     = "${var.workspace_name}-grafana"
  account_access_type      = "CURRENT_ACCOUNT"
  authentication_providers = ["AWS_SSO"]
  permission_type          = "SERVICE_MANAGED"
  role_arn                 = aws_iam_role.grafana_service_role.arn

  data_sources = ["PROMETHEUS"]

  tags = {
    Name        = "${var.workspace_name}-grafana"
    Environment = "production"
  }
}

# IAM role for Grafana service
resource "aws_iam_role" "grafana_service_role" {
  name = "holonote-grafana-service-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "grafana.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# IAM policy for Grafana to read from AMP
resource "aws_iam_role_policy" "grafana_amp_read_policy" {
  name = "holonote-grafana-amp-read-policy"
  role = aws_iam_role.grafana_service_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "aps:ListWorkspaces",
          "aps:DescribeWorkspace",
          "aps:QueryMetrics",
          "aps:GetSeries",
          "aps:GetLabels",
          "aps:GetMetricMetadata"
        ]
        Resource = aws_prometheus_workspace.this.arn
      }
    ]
  })
}

# Attach AWS managed policy for Grafana
resource "aws_iam_role_policy_attachment" "grafana_cloudwatch" {
  role       = aws_iam_role.grafana_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchReadOnlyAccess"
}

# --- Grafana API Key for programmatic access (optional, for automation) ---
# Note: API keys are created via Grafana UI or API, not Terraform
# This is just a placeholder for documentation
