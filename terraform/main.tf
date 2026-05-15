terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# This tells Terraform which region to build our resources in
provider "aws" {
  region = "eu-central-1" 
}

# 1. Fetch the ID of the latest official Ubuntu 22.04 image
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical's official AWS account ID

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# 2. Upload your public SSH key to AWS
resource "aws_key_pair" "deployer" {
  key_name   = "uptime-monitor-key"
  public_key = file("~/.ssh/uptime_key.pub")
}

# 3. Create a Security Group (Firewall)
resource "aws_security_group" "uptime_sg" {
  name        = "uptime-monitor-sg"
  description = "Allow SSH, API, and Grafana traffic"

  # Allow SSH access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }

  # Allow FastAPI traffic
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow Grafana traffic
  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow the server to access the internet (needed to download Docker)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 4. Create the EC2 Server
resource "aws_instance" "app_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro" # AWS Free Tier eligible
  key_name      = aws_key_pair.deployer.key_name

  # Attach the firewall rules
  vpc_security_group_ids = [aws_security_group.uptime_sg.id]

  tags = {
    Name = "UptimeMonitor-Prod"
  }
}

# 5. Output the public IP address after creation
output "server_public_ip" {
  value       = aws_instance.app_server.public_ip
  description = "The public IP address of the EC2 instance"
}