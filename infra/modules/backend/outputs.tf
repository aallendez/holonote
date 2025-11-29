output "alb_dns" {
  value = aws_lb.this.dns_name
}

output "cluster_id" {
  value = aws_ecs_cluster.this.id
}
