output "alb_dns" {
  value = aws_lb.this.dns_name
}

output "cluster_id" {
  value = aws_ecs_cluster.this.id
}

output "ecs_security_group_id" {
  value = aws_security_group.ecs_sg.id
}
