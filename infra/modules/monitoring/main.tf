# Data sources
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

# Random ID for workspace name uniqueness
resource "random_id" "workspace_suffix" {
  byte_length = 2
  keepers = {
    workspace_name = var.workspace_name
  }
}

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
  name                     = "${var.workspace_name}-grafana-${substr(random_id.workspace_suffix.hex, 0, 4)}"
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

# Local values for Grafana setup
locals {
  dashboard_file_path = "${path.module}/grafana-provisioning/dashboards/holonote-backend.json"
  admin_emails_json   = jsonencode(var.admin_emails)
}

# --- Grafana Setup (Dashboard Import & User Assignment) ---
resource "null_resource" "setup_grafana" {
  depends_on = [
    aws_grafana_workspace.this,
    aws_iam_role_policy.grafana_amp_read_policy
  ]

  triggers = {
    workspace_id       = aws_grafana_workspace.this.id
    workspace_endpoint = aws_grafana_workspace.this.endpoint
    dashboard_file     = filemd5(local.dashboard_file_path)
    admin_emails       = local.admin_emails_json
    region             = data.aws_region.current.name
  }

  provisioner "local-exec" {
    command = <<-EOT
      bash ${path.module}/scripts/setup-grafana.sh \
        "${aws_grafana_workspace.this.id}" \
        "${aws_grafana_workspace.this.endpoint}" \
        '${local.admin_emails_json}' \
        "${local.dashboard_file_path}" \
        "${data.aws_region.current.name}"
    EOT
  }
}
