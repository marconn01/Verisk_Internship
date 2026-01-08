# Terraform Deployment

## Setup

```bash
cd terraform
terraform init
```

## Review Changes

```bash
terraform plan
```

## Deploy Infrastructure

```bash
terraform apply
```

Type `yes` when prompted.

## Get Outputs

```bash
# EC2 IP address
terraform output ec2_public_ip

# S3 bucket name
terraform output s3_bucket_name
```

## Resources Created

- EC2 instance (t3.micro)
- Security group
- S3 bucket
- SQS queue
- DynamoDB table
- IAM role and policies
- CloudWatch log groups

## Update Infrastructure

After changing `.tf` files:
```bash
terraform plan
terraform apply
```

## Destroy Everything

**Warning: This deletes all resources**
```bash
terraform destroy
```

## Common Issues

**State lock error:**
```bash
terraform force-unlock <LOCK_ID>
```

**Resource already exists:**
```bash
terraform import aws_security_group.weather_sg sg-xxxxx
```

**Permission denied:**
- Check AWS credentials: `aws sts get-caller-identity`
- Verify IAM permissions
