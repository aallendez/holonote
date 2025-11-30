output "amp_workspace_id" {
  value       = aws_prometheus_workspace.this.id
  description = "AMP workspace ID"
}

output "amp_endpoint" {
  value       = aws_prometheus_workspace.this.prometheus_endpoint
  description = "AMP remote write endpoint URL"
  sensitive   = true
}

output "amp_workspace_arn" {
  value       = aws_prometheus_workspace.this.arn
  description = "AMP workspace ARN"
}

output "grafana_workspace_id" {
  value       = aws_grafana_workspace.this.id
  description = "Grafana workspace ID"
}

output "grafana_endpoint" {
  value       = aws_grafana_workspace.this.endpoint
  description = "Grafana workspace endpoint URL"
}

output "grafana_workspace_arn" {
  value       = aws_grafana_workspace.this.arn
  description = "Grafana workspace ARN"
}
