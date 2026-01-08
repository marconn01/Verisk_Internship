# 🌤️ Weather Alert Web Application

> A production-ready, cloud-native weather monitoring application demonstrating modern DevOps practices, containerization, and AWS infrastructure automation.

[![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20ECR%20%7C%20S3-orange)](https://aws.amazon.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue)](https://www.docker.com/)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-purple)](https://www.terraform.io/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green)](https://www.python.org/)

## 📖 Overview

This project is a comprehensive weather alert system built as part of a DevOps internship at **Verisk Analytics**. It demonstrates end-to-end DevOps practices including containerization, infrastructure as code, CI/CD pipelines, and cloud deployment on AWS EC2.

### Key Features

**Backend (Python/Flask)**
- Real-time weather data from OpenWeatherMap API
- 5-day weather forecasting with 3-hour intervals
- Temperature-based alerting system (high/low thresholds)
- In-memory caching with TTL for performance optimization
- RESTful API serving weather snapshots and alerts
- Health check endpoints for monitoring
- CloudWatch integration for centralized logging

**Frontend (HTML/CSS/JavaScript)**
- Modern, responsive UI design
- Multi-city weather display support
- Real-time alert notifications for extreme temperatures
- City search history with localStorage
- Mobile-friendly responsive interface

**Data Processing Pipeline**
- Hourly cron job for automated weather data collection
- Producer: Fetches weather data and publishes to SQS
- Consumer: Asynchronously processes SQS messages
- S3 storage for raw weather snapshots (per city, per hour)
- DynamoDB for structured metadata and metrics storage
- SQS for decoupled, scalable message processing

**DevOps & Infrastructure**
- Multi-container Docker architecture (Frontend, Backend, Producer, Consumer)
- Docker Compose orchestration for easy deployment
- AWS ECR for private container registry
- Terraform for Infrastructure as Code (IaC)
- EC2 deployment with IAM role-based access control
- CI/CD pipeline with automated build, test, and deployment
- Blue-Green deployment strategy support
- CloudWatch metrics and log monitoring
- Automated error handling and retry logic

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│                          AWS Cloud                                 │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                       EC2 Instance                           │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │  │
│  │  │   Frontend   │  │   Backend    │  │   Cron Job       │  │  │
│  │  │   (Nginx)    │  │   (Flask)    │  │   (Hourly)       │  │  │
│  │  │   Port 80    │  │  Port 5000   │  │      ▼           │  │  │
│  │  └──────┬───────┘  └──────┬───────┘  │   Producer       │  │  │
│  │         │                  │          └─────────┬────────┘  │  │
│  └─────────┼──────────────────┼────────────────────┼──────────┘  │
│            │                  │                    │              │
│  ┌─────────▼──────────────────▼────────────────────▼──────────┐  │
│  │                    AWS Services Layer                       │  │
│  │  ┌────────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │  │
│  │  │    ECR     │  │    SQS   │  │    S3    │  │ DynamoDB │ │  │
│  │  │  Container │  │  Message │  │  Raw     │  │ Metadata │ │  │
│  │  │  Registry  │  │  Queue   │  │ Snapshots│  │ & Metrics│ │  │
│  │  └────────────┘  └────┬─────┘  └──────────┘  └──────────┘ │  │
│  │                       │                                     │  │
│  │                  ┌────▼─────────┐                          │  │
│  │                  │   Consumer   │                          │  │
│  │                  │  (Processes  │                          │  │
│  │                  │  SQS Queue)  │                          │  │
│  │                  └──────────────┘                          │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    CloudWatch                               │  │
│  │        Logs  │  Metrics  │  Alarms  │  Dashboards          │  │
│  └─────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │  OpenWeatherMap    │
                    │      API           │
                    └────────────────────┘
```

## 📁 Project Structure

```
.
├── backend/                    # Flask backend application
│   ├── app.py                 # Main application entry point
│   ├── weather_service.py     # Weather API integration
│   ├── cache_layer.py         # Caching mechanism
│   ├── snapshot/              # Snapshot service components
│   │   ├── snapshot_producer.py   # S3 snapshot producer
│   │   ├── snapshot_consumer.py   # S3 snapshot consumer
│   │   ├── Dockerfile.snapshot.producer
│   │   └── Dockerfile.snapshot.consumer
│   ├── utils.py               # Helper utilities
│   ├── Dockerfile             # Backend container image
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # Frontend web application
│   ├── index.html             # Main HTML file
│   ├── script.js              # JavaScript logic
│   ├── style.css              # Styling
│   └── Dockerfile             # Frontend container image
│
├── terraform/                  # Infrastructure as Code
│   ├── main.tf                # Main Terraform configuration
│   ├── variables.tf           # Variable definitions
│   └── outputs.tf             # Output definitions
│
├── scripts/                    # Deployment and utility scripts
│   ├── project.sh             # Main deployment script
│   ├── version2.sh            # Alternative deployment
│   └── test.sh                # Testing script
│
├── docs/                       # Documentation
│   ├── ARCHITECTURE.md        # System architecture details
│   ├── DEPLOYMENT.md          # Deployment guide
│   └── API.md                 # API documentation
│
├── .github/workflows/          # CI/CD pipelines
│   └── deploy.yml             # GitHub Actions workflow
│
├── docker-compose.yml          # Multi-container orchestration
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- AWS Account with CLI configured
- OpenWeatherMap API key ([Get free key](https://openweathermap.org/api))
- Terraform (for infrastructure provisioning)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/marconn01/Weather_App.git
   cd Weather_App
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenWeatherMap API key
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:80
   - Backend API: http://localhost:5000
   - Health check: http://localhost:5000/health

### Production Deployment on AWS

**Component Deployment Guides:**
- [Terraform Infrastructure](terraform/DEPLOY.md) - Provision AWS resources
- [Backend API](backend/DEPLOY.md) - Deploy Flask backend
- [Frontend](frontend/DEPLOY.md) - Deploy Nginx frontend
- [Snapshot Services](backend/snapshot/DEPLOY.md) - Deploy data pipeline

**Quick deploy:**
```bash
cd scripts
chmod +x project.sh
./project.sh
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# OpenWeatherMap API
OPENWEATHER_API_KEY=your_api_key_here

# Temperature Thresholds (Celsius)
HIGH_TEMP_THRESHOLD=35
LOW_TEMP_THRESHOLD=5

# Server Ports
BACKEND_PORT=5000
FRONTEND_PORT=80

# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=your_account_id
ECR_REGISTRY=your_account_id.dkr.ecr.us-east-1.amazonaws.com

# S3 Configuration
WEATHER_BUCKET_NAME=your-weather-snapshots-bucket

# SQS Configuration
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/your-account/weather-queue

# DynamoDB Configuration
DYNAMODB_TABLE_NAME=weather-data
```

## 📊 API Endpoints

### Weather Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/health` | Health check | None |
| GET | `/weather` | Get current weather | `city` (required) |
| GET | `/forecast` | Get 5-day forecast | `city` (required) |
| GET | `/logs` | Get recent logs | `limit` (optional) |

### Example Request

```bash
curl "http://localhost:5000/weather?city=London"
```

### Example Response

```json
{
  "city": "London",
  "temperature": 15.5,
  "feels_like": 14.2,
  "description": "Partly cloudy",
  "humidity": 72,
  "wind_speed": 5.2,
  "alert": null,
  "timestamp": "2026-01-08T10:30:00Z"
}
```

See [docs/API.md](docs/API.md) for complete API documentation.

## 🐳 Docker Setup

### Build Images Locally

```bash
# Backend
cd backend
docker build -t weather-backend .

# Frontend
cd frontend
docker build -t weather-frontend .
```

### Push to ECR

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin ${ECR_REGISTRY}

# Tag and push
docker tag weather-backend:latest ${ECR_REGISTRY}/weather-backend:latest
docker push ${ECR_REGISTRY}/weather-backend:latest
```

## 🏗️ Infrastructure

### Terraform Resources

The project provisions the following AWS resources:

- **EC2 Instance**: t3.micro instance running Docker containers with IAM role
- **IAM Role & Policies**: For EC2 access to S3, SQS, DynamoDB, CloudWatch
- **Security Group**: Configured for HTTP (80), API (5000), and SSH (22)
- **S3 Bucket**: For raw weather data snapshots with 30-day lifecycle
- **SQS Queue**: For decoupled producer-consumer message processing
- **DynamoDB Table**: For structured weather metadata and metrics storage
- **ECR Repositories**: For storing Docker images
- **CloudWatch Log Groups**: For centralized logging and monitoring

### Deploy Infrastructure

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
python test_api.py
```

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test weather endpoint
curl "http://localhost:5000/weather?city=London"

# Test forecast endpoint
curl "http://localhost:5000/forecast?city=Paris"
```

## 📈 Monitoring & Logging

- **CloudWatch Logs**: Centralized logging for all containers
- **CloudWatch Metrics**: CPU, memory, disk, network metrics
- **Application Logs**: Stored in `backend/logs/app.log` and CloudWatch
- **Health Checks**: Available at `/health` endpoint
- **Container Health**: Docker health checks configured in docker-compose.yml
- **SQS Metrics**: Queue depth, message age, processing time
- **DynamoDB Metrics**: Read/write capacity, throttling events
- **Custom Alerts**: Temperature threshold alerts stored in DynamoDB

## 🔐 Security

- API keys stored in environment variables (not committed)
- Security groups restrict access appropriately
- HTTPS ready (configure with SSL/TLS certificates)
- Regular dependency updates
- Sensitive files excluded via .gitignore

## 🚧 Future Enhancements


- [ ] Implement Redis for distributed caching
- [ ] Add Prometheus and Grafana for advanced metrics
- [ ] Implement API Gateway with Lambda for serverless backend
- [ ] Add automated testing in CI/CD (unit, integration, e2e)
- [ ] Configure custom domain with Route 53 and SSL/TLS
- [ ] Implement API authentication and rate limiting

## 📚 Documentation

- [Architecture Documentation](docs/ARCHITECTURE.md) - System design and diagrams
- [Project Summary](docs/PROJECT_SUMMARY.md) - Internship project overview

**Deployment Guides:**
- [Terraform](terraform/DEPLOY.md)
- [Backend](backend/DEPLOY.md)
- [Frontend](frontend/DEPLOY.md)
- [Snapshots](backend/snapshot/DEPLOY.md)


## 👨‍💻 Author

**Marco** - nocram

- GitHub: [@marconn01](https://github.com/marconn01)
- Project: [Weather_App](https://github.com/marconn01/Weather_App)


