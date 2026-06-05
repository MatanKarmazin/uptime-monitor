terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.0"
}

provider "aws" {
  region = "eu-central-1"
}

# -----------------------------
# Security Group
# -----------------------------

resource "aws_security_group" "uptime_monitor_sg" {
  name        = "uptime-monitor-sg"
  description = "Security group for uptime monitor project"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "FastAPI"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Grafana"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Prometheus"
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "uptime-monitor-sg"
  }
}

# -----------------------------
# SSH Key Pair
# -----------------------------

resource "aws_key_pair" "uptime_monitor_key" {
  key_name   = "uptime-monitor-key"
  public_key = file("${path.module}/uptime-monitor-key.pub")
}

# -----------------------------
# EC2 Instance
# -----------------------------

resource "aws_instance" "uptime_monitor" {
  ami                    = "ami-04e601abe3e1a910f"
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.uptime_monitor_sg.id]
  key_name               = aws_key_pair.uptime_monitor_key.key_name

  tags = {
    Name = "uptime-monitor"
  }
}

# -----------------------------
# Elastic IP
# -----------------------------

resource "aws_eip" "uptime_monitor_eip" {
  instance = aws_instance.uptime_monitor.id

  tags = {
    Name = "uptime-monitor-eip"
  }
}

# -----------------------------
# Outputs
# -----------------------------

output "public_ip" {
  value = aws_eip.uptime_monitor_eip.public_ip
}