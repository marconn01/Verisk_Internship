# System Architecture

## Overview

Weather app with frontend (Nginx), backend (Flask), and data pipeline. Runs on AWS EC2 using Docker containers.

## How It Works

```
User → Frontend → Backend → OpenWeather API
                     ↓
                   Cache (10 min)

Hourly Cron → Producer → SQS Queue → Consumer → DynamoDB
                  ↓                              
                 S3                            
```

## Components

### Frontend
- HTML/CSS/JavaScript
- Nginx server
- Port 80

### Backend
- Flask API
- Python 3.9
- Port 5000
- In-memory cache

### Data Pipeline
- **Producer**: Fetches weather data every hour (cron)
- **SQS**: Message queue
- **Consumer**: Processes messages, saves to DynamoDB
- **S3**: Raw JSON snapshots
- **DynamoDB**: Structured data with alert levels

## AWS Resources

- **EC2**: t3.micro Ubuntu, hosts all containers
- **ECR**: Docker image registry
- **S3**: Snapshot storage
- **SQS**: Message queue
- **DynamoDB**: Database
- **CloudWatch**: Logs
- **IAM**: EC2 role with permissions

## Docker Setup

Four containers:
1. `weather-frontend` - Nginx
2. `weather-backend` - Flask API
3. `snapshot-producer` - Data collector (cron triggered)
4. `snapshot-consumer` - Message processor (always running)

## File Structure

**Backend (Python):**
- `app.py` - Flask routes, CORS, health checks
- `weather_service.py` - API calls, alert logic
- `cache_layer.py` - In-memory cache with TTL
- `utils.py` - Logging, helpers

**Snapshot Services:**
- `snapshot_producer.py` - Fetches weather, sends to SQS, saves to S3
- `snapshot_consumer.py` - Polls SQS, processes messages, writes to DynamoDB
- `snapshot.py` - Shared utilities

**Frontend:**
- `index.html` - Page structure
- `script.js` - API calls, UI logic
- `style.css` - Styling
- `cities.js` - City list

**Infrastructure:**
- `terraform/` - AWS resource definitions
- `docker-compose.yml` - Container orchestration
- `.github/workflows/deploy.yml` - CI/CD pipeline

## Caching

**Type:** In-memory Python dict  
**TTL:** 10 minutes  
**Key Format:** `{city}:{endpoint}`

Reduces API calls and improves response time (50ms cached vs 300ms API).

## Security

- API keys in `.env` file (not in git)
- EC2 IAM role (no hardcoded credentials)
- Security group limits ports 22, 80, 5000
- Non-root users in Docker containers

---

## Nginx Reverse Proxy & Blue-Green Deployment

```
┌───────────────────────────────────────────────────────────────────────┐
│                         INTERNET / USERS                               │
└──────────────────────────────┬────────────────────────────────────────┘
                               │
                               │ HTTP/HTTPS (Port 80/443)
                               │
                ┌──────────────▼─────────────────┐
                │      AWS Security Group        │
                │      (Ports: 22, 80, 443)      │
                └──────────────┬─────────────────┘
                               │
                               │
        ┌──────────────────────▼──────────────────────┐
        │           AWS EC2 Instance                  │
        │                                             │
        │  ┌────────────────────────────────────┐    │
        │  │   NGINX REVERSE PROXY (Port 80)    │    │
        │  │                                    │    │
        │  │  ┌──────────────────────────────┐  │    │
        │  │  │   Routing Configuration      │  │    │
        │  │  │                              │  │    │
        │  │  │  / (root)    → Frontend      │  │    │
        │  │  │  /static/*   → Frontend      │  │    │
        │  │  │  /api/*      → Backend       │  │    │
        │  │  │  /health     → Backend       │  │    │
        │  │  └──────────────────────────────┘  │    │
        │  │                                    │    │
        │  │  ┌──────────────────────────────┐  │    │
        │  │  │   Zero downtime Deployment   │  │    │
        │  │  │   (Blue-Green Switch)        │  │    │
        │  │  │                              │  │    │
        │  │  │   upstream backend {         │  │    │
        │  │  │     server blue:5000;   ◄────┼──┼────── Currently Active
        │  │  │     # server green:5001;     │  │    │
        │  │  │   }                          │  │    │
        │  │  └──────────────────────────────┘  │    │
        │  └────────────┬───────────────────┬───┘    │
        │               │                   │         │
        │               │                   │         │
        │  ┌────────────▼─────────┐    ┌───▼──────────────────┐
        │  │  BLUE ENVIRONMENT    │    │  GREEN ENVIRONMENT   │
        │  │  (Current/Active)    │    │  (Standby/Testing)   │
        │  │                      │    │                      │
        │  │  ┌────────────────┐  │    │  ┌────────────────┐ │
        │  │  │ Frontend:80    │  │    │  │ Frontend:8080  │ │
        │  │  │ (Nginx)        │  │    │  │ (Nginx)        │ │
        │  │  └────────────────┘  │    │  └────────────────┘ │
        │  │                      │    │                      │
        │  │  ┌────────────────┐  │    │  ┌────────────────┐ │
        │  │  │ Backend:5000   │  │    │  │ Backend:5001   │ │
        │  │  │ (Flask)        │  │    │  │ (Flask)        │ │
        │  │  │                │  │    │  │                │ │
        │  │  │ ┌──────────┐   │  │    │  │ ┌──────────┐   │ │
        │  │  │ │  Cache   │   │  │    │  │ │  Cache   │   │ │
        │  │  │ └──────────┘   │  │    │  │ └──────────┘   │ │
        │  │  └────────────────┘  │    │  └────────────────┘ │
        │  │                      │    │                      │
        │  │  ┌────────────────┐  │    │  ┌────────────────┐ │
        │  │  │ Consumer       │  │    │  │ Consumer       │ │
        │  │  │ (Running)      │  │    │  │ (Running)      │ │
        │  │  └────────────────┘  │    │  └────────────────┘ │
        │  └──────────────────────┘    └──────────────────────┘
        │                                                      │
        │  ┌────────────────────────────────────────────────┐ │
        │  │       Snapshot Producer (Cron - Shared)        │ │
        │  │       Runs every hour, independent of env      │ │
        │  └────────────────────────────────────────────────┘ │
        └───────────────────────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ OpenWeather  │      │   AWS ECR    │      │   AWS S3     │
│     API      │      │              │      │              │
│              │      │ Blue Images  │      │ Snapshots    │
│ Weather Data │      │ Green Images │      │              │
└──────────────┘      └──────────────┘      └──────────────┘
                                                    │
                      ┌─────────────────────────────┼───────────┐
                      │                             │           │
                      ▼                             ▼           ▼
              ┌──────────────┐            ┌──────────────┐     │
              │   AWS SQS    │            │  DynamoDB    │     │
              │              │            │              │     │
              │ Message      │◄───────────│ Structured   │     │
              │ Queue        │   Polls    │ Weather Data │     │
              └──────────────┘            └──────────────┘     │
                                                               │
                                          ┌────────────────────▼────┐
                                          │   AWS CloudWatch        │
                                          │   Logs & Metrics        │
                                          └─────────────────────────┘


BLUE-GREEN DEPLOYMENT PROCESS:
STEP 1: Current State (Blue Active)

Nginx -> Blue (v1.0) [ACTIVE - Serving 100% traffic]
     -> Green (empty) [STANDBY]


STEP 2: Deploy New Version to Green

1. Pull new images (v2.0) from ECR
2. Start Green containers on different ports
3. Green ports:
   - Frontend: 8080
   - Backend: 5001
4. Run health checks on Green
5. Test Green internally

Nginx -> Blue (v1.0) [ACTIVE - Serving 100% traffic]
     -> Green (v2.0) [TESTING - Not live]


STEP 3: Switch Traffic (Update Nginx Config)

Update nginx.conf:

upstream backend {
  # server blue:5000;   # Blue disabled
  server green:5001;   # Green active
}

Reload Nginx:
nginx -s reload

Nginx -> Blue (v1.0) [STANDBY - Rollback ready]
     -> Green (v2.0) [ACTIVE - Serving 100% traffic]


STEP 4: Monitor & Validate

- Monitor CloudWatch logs
- Check health endpoints
- Verify traffic flow
- Monitor response times and error rates

If OK: Keep Green, remove Blue
If issues: Roll back to Blue


STEP 5: Cleanup

1. Stop Blue containers
2. Remove old Blue images
3. Green becomes the new Blue

Nginx -> Green (v2.0) [ACTIVE]
     -> Blue (empty) [STANDBY]


NGINX CONFIGURATION EXAMPLE:

upstream frontend {
    server blue-frontend:80;        # Blue environment
    # server green-frontend:8080;   # Green environment (activate on deploy)
}

upstream backend {
    server blue-backend:5000;       # Blue environment
    # server green-backend:5001;    # Green environment (activate on deploy)
}

server {
    listen 80;
    
    # Frontend routing
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Backend API routing
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Health check endpoint
    location /health {
        proxy_pass http://backend;
    }
}

BENEFITS:
✓ Zero downtime deployments
✓ Instant rollback capability (just switch Nginx config back)
✓ Test new version in production environment before switching
✓ No user impact during deployment
✓ Easy A/B testing (send % of traffic to each)
✓ Reduces deployment risk
```

---

## Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          INTERNET / USERS                            │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         │ HTTP/HTTPS
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│                      AWS SECURITY GROUP                              │
│                   (Ports: 22, 80, 5000)                             │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         │
        ┌────────────────▼─────────────────┐
        │      AWS EC2 Instance            │
        │      (t3.micro Ubuntu)           │
        │    ┌──────────────────────┐      │
        │    │   IAM Role Attached  │      │
        │    │  - S3 Access         │      │
        │    │  - SQS Access        │      │
        │    │  - DynamoDB Access   │      │
        │    │  - CloudWatch Access │      │
        │    │  - ECR Pull Access   │      │
        │    └──────────────────────┘      │
        │                                   │
        │  ┌─────────────────────────────┐ │
        │  │   DOCKER CONTAINERS         │ │
        │  │                             │ │
        │  │  ┌────────────────────┐    │ │
        │  │  │  weather-frontend  │    │ │
        │  │  │  (Nginx:80)        │    │ │
        │  │  │  HTML/CSS/JS       │    │ │
        │  │  └──────┬─────────────┘    │ │
        │  │         │                   │ │
        │  │         │ API Calls         │ │
        │  │         │                   │ │
        │  │  ┌──────▼─────────────┐    │ │
        │  │  │  weather-backend   │    │ │
        │  │  │  (Flask:5000)      │    │ │
        │  │  │                    │    │ │
        │  │  │  ┌──────────────┐  │    │ │
        │  │  │  │   Cache      │  │    │ │
        │  │  │  │  (10 min)    │  │    │ │
        │  │  │  └──────────────┘  │    │ │
        │  │  └──────┬─────────────┘    │ │
        │  │         │                   │ │
        │  │         │                   │ │
        │  │  ┌──────▼─────────────┐    │ │
        │  │  │ snapshot-consumer  │    │ │
        │  │  │ (Always Running)   │    │ │
        │  │  │ - Polls SQS        │    │ │
        │  │  │ - Writes DynamoDB  │    │ │
        │  │  └────────────────────┘    │ │
        │  │                             │ │
        │  └─────────────────────────────┘ │
        │                                   │
        │  ┌─────────────────────────────┐ │
        │  │   CRON JOB (Hourly)         │ │
        │  │                             │ │
        │  │  0 * * * *                  │ │
        │  │  docker run ...             │ │
        │  │  snapshot-producer          │ │
        │  │                             │ │
        │  └─────────────────────────────┘ │
        └───────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   AWS ECR    │  │ OpenWeather  │  │  AWS S3      │
│              │  │     API      │  │  Bucket      │
│ - frontend   │  │              │  │              │
│ - backend    │  │ Weather Data │  │ Raw JSON     │
│ - producer   │  │              │  │ Snapshots    │
│ - consumer   │  │              │  │              │
└──────────────┘  └──────────────┘  └──────┬───────┘
                                            │
                                            │
                  ┌─────────────────────────┼──────────┐
                  │                         │          │
                  ▼                         ▼          ▼
          ┌──────────────┐         ┌──────────────┐   │
          │   AWS SQS    │         │  DynamoDB    │   │
          │              │         │              │   │
          │ Message      │         │ Structured   │   │
          │ Queue        │◄────────│ Weather Data │   │
          │              │  Polls  │              │   │
          │ - Messages   │         │ - city       │   │
          │ - DLQ        │         │ - timestamp  │   │
          └──────────────┘         │ - temp       │   │
                                   │ - alerts     │   │
                                   └──────────────┘   │
                                                      │
                                                      │
                                   ┌──────────────────▼───┐
                                   │   AWS CloudWatch     │
                                   │                      │
                                   │ - Logs (all services)│
                                   │ - Metrics            │
                                   │ - Alarms             │
                                   └──────────────────────┘


┌──────────────────────────────────────────────────────────────┐
│                        DATA FLOW                              │
└──────────────────────────────────────────────────────────────┘

USER REQUEST FLOW:
1. User opens browser → Frontend (Nginx)
2. User searches city → Frontend sends API request → Backend
3. Backend checks cache → Cache hit (return) | Cache miss (→ step 4)
4. Backend calls OpenWeather API → Gets weather data
5. Backend processes data, checks alerts → Updates cache
6. Backend returns JSON → Frontend displays weather

SNAPSHOT FLOW (Every Hour):
1. Cron triggers → snapshot-producer container starts
2. Producer fetches weather for all cities → OpenWeather API
3. Producer saves raw JSON → S3 bucket (city/timestamp.json)
4. Producer sends message → SQS queue
5. Consumer (always running) polls SQS → Receives message
6. Consumer validates & processes → Extracts temp, alerts, etc.
7. Consumer writes structured data → DynamoDB
8. Consumer deletes message from SQS
9. All components log → CloudWatch

CI/CD FLOW:
1. Git push to main → GitHub Actions triggered
2. Actions builds Docker images → Pushes to ECR
3. Actions SSH to EC2 → Pulls latest images
4. Restarts containers → Deployment complete
5. Health checks verify → App running



```

