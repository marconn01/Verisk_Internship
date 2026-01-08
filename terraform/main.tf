provider "aws" {
  region = var.aws_region
}

data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "weather_sg" {
  name        = "weather-app-sg"
  description = "Security group for weather application"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "weather-app-sg"
  }
}

resource "aws_instance" "weather_ec2" {
  ami                    = var.ec2_ami
  instance_type          = var.ec2_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [var.security_group_id != "" ? var.security_group_id : aws_security_group.weather_sg.id]
  key_name               = var.ssh_key_name

  tags = {
    Name = "weather-app"
  }
}

resource "aws_s3_bucket" "weather_bucket" {
  bucket = var.weather_bucket_name

  tags = {
    Name = var.weather_bucket_name
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "weather_bucket_lifecycle" {
  bucket = aws_s3_bucket.weather_bucket.id
  
  rule {
    id     = "delete-old-snapshots"
    status = "Enabled"

    expiration {
      days = 30
    }
  }
}

resource "aws_ecr_repository" "weather_backend" {
  name = var.backend_ecr_name

  tags = {
    Name = "weather-backend"
  }
}

resource "aws_ecr_repository" "weather_frontend" {
  name = var.frontend_ecr_name

  tags = {
    Name = "weather-frontend"
  }
}

resource "aws_ecr_repository" "weather_snapshot" {
  name = var.snapshot_ecr_name

  tags = {
    Name = "weather-snapshot"
  }
}