# GitHub Actions OIDC Provider
# Create the OIDC provider if it doesn't exist
# Note: If the provider already exists in your AWS account, set create_oidc_provider = false
resource "aws_iam_openid_connect_provider" "github" {
  count = var.create_oidc_provider ? 1 : 0
  url   = "https://token.actions.githubusercontent.com"

  client_id_list = ["sts.amazonaws.com"]

  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1",
    "1c58a3a8518e8759bf075b76b750d4f2df264fcd"
  ]

  tags = {
    Name = "GitHubActionsOIDC"
  }
}

# Use data source to reference the provider only if we're NOT creating it
# (i.e., if it already exists in the account)
data "aws_iam_openid_connect_provider" "github" {
  count = var.create_oidc_provider ? 0 : 1
  url   = "https://token.actions.githubusercontent.com"
}

# Local to get the provider ARN (either from created resource or data source)
locals {
  oidc_provider_arn = var.create_oidc_provider ? aws_iam_openid_connect_provider.github[0].arn : data.aws_iam_openid_connect_provider.github[0].arn
}

# IAM Role for GitHub Actions
resource "aws_iam_role" "github_actions" {
  name = "holonote-github-actions-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = local.oidc_provider_arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:${var.github_repo}:*"
          }
        }
      }
    ]
  })

  tags = {
    Name        = "holonote-github-actions-role"
    Environment = "production"
  }
}

# Policy for S3 operations (frontend deployment)
resource "aws_iam_role_policy" "s3_policy" {
  name = "holonote-github-actions-s3-policy"
  role = aws_iam_role.github_actions.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject",
          "s3:ListBucket",
          "s3:PutObjectAcl"
        ]
        Resource = [
          "arn:aws:s3:::${var.frontend_bucket_name}",
          "arn:aws:s3:::${var.frontend_bucket_name}/*"
        ]
      }
    ]
  })
}

# Policy for ECS operations
resource "aws_iam_role_policy" "ecs_policy" {
  name = "holonote-github-actions-ecs-policy"
  role = aws_iam_role.github_actions.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecs:UpdateService",
          "ecs:DescribeServices",
          "ecs:DescribeTaskDefinition",
          "ecs:RegisterTaskDefinition",
          "ecs:ListTasks",
          "ecs:DescribeTasks"
        ]
        Resource = "*"
      }
    ]
  })
}

# Policy for Terraform operations (EC2, RDS, ECS, IAM, etc.)
resource "aws_iam_role_policy" "terraform_policy" {
  name = "holonote-github-actions-terraform-policy"
  role = aws_iam_role.github_actions.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ec2:*",
          "rds:*",
          "ecs:*",
          "iam:*",
          "logs:*",
          "s3:*",
          "secretsmanager:*",
          "application-autoscaling:*",
          "elasticloadbalancing:*",
          "cloudwatch:*",
          "aps:*",
          "grafana:*"
        ]
        Resource = "*"
      }
    ]
  })
}
