resource "aws_s3_bucket" "frontend" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_public_access_block" "public" {
  bucket = aws_s3_bucket.frontend.id

  block_public_acls       = false
  block_public_policy     = false
  restrict_public_buckets = false
  ignore_public_acls      = false
}

resource "aws_s3_bucket_policy" "public_policy" {
  bucket = aws_s3_bucket.frontend.id

  # Explicitly depend on public access block to ensure it's created first
  depends_on = [aws_s3_bucket_public_access_block.public]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = "*"
      Action    = ["s3:GetObject"]
      Resource  = "${aws_s3_bucket.frontend.arn}/*"
    }]
  })
}

resource "aws_s3_bucket_website_configuration" "hosting" {
  bucket = aws_s3_bucket.frontend.bucket

  index_document {
    suffix = "index.html"
  }
}
