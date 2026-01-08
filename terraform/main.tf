provider "aws" {
  region = var.aws_region
}

data "aws_vpc" "default" {
  default = true
}


# Security Group (import your existing one or create new if needed)
resource "aws_security_group" "weather_sg" {
  name        = "launch-wizard-1"
  description = "launch-wizard-1 created by AWS console"
  vpc_id      = "vpc-0b93efe777cf56dc2"

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
    from_port   = 5500
    to_port     = 5500
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

  lifecycle {
    prevent_destroy = true
    ignore_changes = [
      description,
      tags,
      name
    ]
  }
}


resource "aws_instance" "weather_ec2" {
  ami                    = "ami-0ecb62995f68bb549"
  instance_type          = "t3.micro"
  subnet_id              = "subnet-0a74c826b6eca9d19"
  vpc_security_group_ids = ["sg-0ffcafc669785d7cf"]
  key_name               = "weatherv2"

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
    id    = "Delete 30 days old objects"
    status = "Enabled"

    expiration {
      days = 30
    }
  }
}

# ECR repositories (import existing ones)
resource "aws_ecr_repository" "weather_backend" {
  name = var.backend_ecr_name
}

resource "aws_ecr_repository" "weather_frontend" {
  name = var.frontend_ecr_name
}

resource "aws_ecr_repository" "weather_snapshot" {
  name = var.snapshot_ecr_name
}

