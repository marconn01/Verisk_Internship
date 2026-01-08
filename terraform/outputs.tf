output "ec2_public_ip" {
  value = aws_instance.weather_ec2.public_ip
}

output "security_group_id" {
  value = aws_security_group.weather_sg.id
}

output "weather_bucket_name" {
  value = aws_s3_bucket.weather_bucket.bucket
}

output "backend_ecr_url" {
  value = aws_ecr_repository.weather_backend.repository_url
}

output "frontend_ecr_url" {
  value = aws_ecr_repository.weather_frontend.repository_url
}

output "snapshot_ecr_url" {
  value = aws_ecr_repository.weather_snapshot.repository_url
}