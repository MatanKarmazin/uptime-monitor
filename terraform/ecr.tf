# Create an ECR repository for the FastAPI image
resource "aws_ecr_repository" "uptime_api" {
  name                 = "uptime-monitor-api"
  image_tag_mutability = "MUTABLE"
  
  # This ensures we can cleanly destroy the portfolio project later
  # even if it contains Docker images
  force_delete         = true 

  tags = {
    Name = "UptimeMonitor-API-Repo"
  }
}

# Output the URL so we can use it in our CI/CD pipeline later
output "ecr_repository_url" {
  value = aws_ecr_repository.uptime_api.repository_url
}