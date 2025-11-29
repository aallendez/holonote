output "website_url" {
  value = "http://${aws_s3_bucket.frontend.bucket}.s3-website-${data.aws_region.current.name}.amazonaws.com"
}

data "aws_region" "current" {}
