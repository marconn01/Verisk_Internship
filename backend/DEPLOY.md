# Backend Deployment

## Build Docker Image

```bash
cd backend
docker build -t weather-backend .
```

## Push to ECR

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag weather-backend:latest ${ECR_REGISTRY}/weather-backend:latest
docker push ${ECR_REGISTRY}/weather-backend:latest
```

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENWEATHER_API_KEY=your_key_here

# Run locally
python app.py
```

## Environment Variables

- `OPENWEATHER_API_KEY` - Weather API key (required)
- `HIGH_TEMP_THRESHOLD` - Alert threshold (default: 35°C)
- `LOW_TEMP_THRESHOLD` - Alert threshold (default: 5°C)

## Health Check

```bash
curl http://localhost:5000/health
```

## Troubleshooting

**Port already in use:**
```bash
# Change port
export FLASK_PORT=5001
```

**API key issues:**
```bash
# Verify key is set
echo $OPENWEATHER_API_KEY

# Test API directly
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=${OPENWEATHER_API_KEY}"
```
