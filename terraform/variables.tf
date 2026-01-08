variable "aws_region" {
  default = "us-east-1"
}

variable "vpc_id" {
  type = string
}

variable "subnet_id" {
  type = string
}

variable "ec2_ami" {
  default = "your_ami"
}

variable "ec2_type" {
  default = "t3.micro"
}

variable "ssh_key_name" {
  type = string
}

variable "security_group_id" {
  type    = string
  default = ""
}

variable "account_id" {
  type = string
}

variable "backend_ecr_name" {
  default = "weather-backend"
}

variable "frontend_ecr_name" {
  default = "weather-frontend"
}

variable "snapshot_ecr_name" {
  default = "weather-snapshot"
}

variable "weather_bucket_name" {
  type = string
}