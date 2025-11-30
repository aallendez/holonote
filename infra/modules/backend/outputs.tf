output "alb_dns" {
  value = aws_lb.this.dns_name
}

output "cluster_id" {
  value = aws_ecs_cluster.this.id
}

output "task_role_arn" {
  value       = aws_iam_role.task_role.arn
  description = "ARN of the ECS task role (for application-level permissions)"
}
