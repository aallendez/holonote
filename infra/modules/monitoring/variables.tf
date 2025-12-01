variable "workspace_name" {
  type        = string
  default     = "holonote-monitoring"
  description = "Name prefix for AMP and Grafana workspaces"
}

variable "backend_task_role_arn" {
  type        = string
  description = "ARN of the backend ECS task role (for writing metrics to AMP)"
}

variable "admin_emails" {
  type        = list(string)
  default     = []
  description = "List of SSO user emails to assign as Grafana admins (optional)"
}
