variable "github_repo" {
  description = "GitHub repository in format 'owner/repo' (e.g., 'juanalonso-allende/holonote')"
  type        = string
}

variable "frontend_bucket_name" {
  description = "Name of the S3 bucket for frontend deployment"
  type        = string
}

variable "create_oidc_provider" {
  description = "Whether to create the GitHub Actions OIDC provider (set to false if it already exists)"
  type        = bool
  default     = false
}
