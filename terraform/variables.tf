variable "aws_region" {
  default = "us-east-1"
}

variable "ec2_ami" {
  default = "ami-0ecb62995f68bb549"
}

variable "ec2_type" {
  default = "t3.micro"
}

variable "ssh_key_name" {
  description = "SSH key for EC2"
  default     = "weatherv2"
}

variable "backend_ecr_name" {
  default = "weather-backend"
}

variable "account_id" {
  default = "912753427807"

}

variable "frontend_ecr_name" {
  default = "weather-frontend"
}

variable "backend_ecr_url" {
  default = "912753427807.dkr.ecr.us-east-1.amazonaws.com/weather-backend"
}

variable "frontend_ecr_url" {
  default = "912753427807.dkr.ecr.us-east-1.amazonaws.com/weather-frontend"
}

variable "weather_bucket_name" {
  description = "s3 buckert for weather app that does periodic calls"
  default     = "weather-bucket-for-verisk-internship"
}

variable "snapshot_ecr_name" {
  description = "ECR repository name for snapshot service"
  default     = "weather-snapshot"
}