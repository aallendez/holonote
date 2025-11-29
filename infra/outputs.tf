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
