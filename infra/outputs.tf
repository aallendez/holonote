output "frontend_url" {
  value = module.frontend.website_url
}

output "alb_dns" {
  value = module.backend.alb_dns
}

output "db_endpoint" {
  value = module.db.endpoint
}

output "ecs_cluster_id" {
  value = module.backend.cluster_id
}

# Monitoring outputs (AWS Managed Services)
output "grafana_endpoint" {
  value       = module.monitoring.grafana_endpoint
  description = "Amazon Managed Grafana workspace endpoint URL"
}

output "grafana_workspace_id" {
  value       = module.monitoring.grafana_workspace_id
  description = "Grafana workspace ID"
}

output "amp_workspace_id" {
  value       = module.monitoring.amp_workspace_id
  description = "Amazon Managed Service for Prometheus workspace ID"
}

output "monitoring_setup_instructions" {
  value = <<-EOT
    AWS Managed Monitoring Setup:

    1. Access Grafana:
       - URL: ${module.monitoring.grafana_endpoint}
       - Login with: AWS IAM Identity Center (AWS SSO)
       - Assign users via AWS Console: Amazon Managed Grafana > Workspace > Users and groups

    2. Configure Grafana Data Source:
       - Go to Configuration > Data Sources
       - Add Prometheus data source
       - Select "Amazon Managed Service for Prometheus"
       - Choose the workspace: ${module.monitoring.amp_workspace_id}
       - Enable SigV4 authentication
       - Save & Test

    3. Backend Metrics:
       - Backend exposes metrics at /metrics endpoint
       - Configure backend to write to AMP using remote write
       - AMP endpoint: (check AWS Console or use terraform output amp_endpoint)

    4. Import Dashboards:
       - Go to Dashboards > Import
       - Use dashboard ID 6417 for Kubernetes (or search for FastAPI dashboards)
       - Or create custom dashboards for your application
  EOT
}

output "github_actions_role_arn" {
  value       = module.github_actions.role_arn
  description = "ARN of the IAM role for GitHub Actions OIDC. Add this as AWS_ROLE_ARN secret in GitHub."
}
