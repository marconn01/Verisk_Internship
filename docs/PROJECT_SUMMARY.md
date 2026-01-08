# DevOps Internship Project

## Project Info

**Project:** Weather App  
**Company:** Verisk Nepal  
**Role:** DevOps Intern  
**Duration:** 3 Months  
**Deployment:** AWS EC2  

---

## What I Built

Weather web app that shows current weather and alerts for multiple cities. Includes automated hourly data collection.

### Stack

**Backend:**
- Flask (Python 3.9)
- OpenWeatherMap API
- In-memory cache

**Frontend:**
- HTML/CSS/JavaScript
- Nginx server

**DevOps:**
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Terraform (AWS setup)

**AWS:**
- EC2 (Ubuntu t3.micro)
- ECR (container registry)
- S3 (file storage)
- SQS (message queue)
- DynamoDB (database)
- CloudWatch (logs)
- IAM (permissions)

---

## What It Does

### 1. Web API
- Get weather for any city
- Show temperature alerts (hot/cold)
- Cache results for 10 minutes
- Health check endpoint

### 2. User Interface
- Search cities
- View current weather
- See 5-day forecast
- Alert warnings
- Search history

### 3. Data Collection
- Cron job runs every hour
- Fetches weather for tracked cities
- Sends to SQS queue
- Consumer processes messages
- Saves to S3 (raw) and DynamoDB (structured)

---

## How I Built It

### Phase 1: Development
- Built Flask API with weather data fetching
- Added caching for faster responses
- Made HTML/CSS/JS frontend
- Tested locally

### Phase 2: CI/CD Setup
- GitHub Actions for auto-deploy
- Builds Docker images on push
- Tests and deploys to EC2

### Phase 3: Docker
- Created 4 Dockerfiles (frontend, backend, producer, consumer)
- Set up docker-compose
- Added health checks

### Phase 4: AWS Setup
- Created ECR for images
- Set up S3 bucket for snapshots
- Created SQS queue
- Created DynamoDB table
- Set up CloudWatch logs

### Phase 5: Terraform
- Wrote .tf files for all AWS resources
- EC2, security groups, IAM roles
- Run `terraform apply` to create everything

### Phase 6: Data Pipeline
- Producer fetches weather hourly (cron)
- Sends to SQS
- Consumer reads from SQS, saves to DynamoDB

### Phase 7: Deployment
- Pushed images to ECR
- SSH'd to EC2
- Ran docker-compose
- Set up cron job

### Phase 8: Monitoring
- CloudWatch logs for all services
- Alarms for errors

### Phase 9: Documentation
- README, architecture docs
- Deployment guides

---

## Challenges

**Challenge:** Docker containers wouldn't start on EC2  
**Solution:** Fixed port conflicts in docker-compose

**Challenge:** SQS messages not processing  
**Solution:** Added IAM permissions for EC2 role

**Challenge:** DynamoDB write errors  
**Solution:** Used Decimal type instead of float

**Challenge:** Terraform state conflicts  
**Solution:** Used remote state in S3 (optional)

---

## What I Learned

- How to deploy apps to AWS
- Docker multi-container setup
- Terraform for infrastructure
- CI/CD with GitHub Actions
- Message queues (SQS)
- IAM roles and permissions
- Cron jobs for scheduled tasks

---

## Links

**GitHub:** https://github.com/marconn01/  
**LinkedIn:** https://www.linkedin.com/in/navin-nepal/
