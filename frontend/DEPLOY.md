# Frontend Deployment

## Build Docker Image

```bash
cd frontend
docker build -t weather-frontend .
```

## Push to ECR

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag weather-frontend:latest ${ECR_REGISTRY}/weather-frontend:latest
docker push ${ECR_REGISTRY}/weather-frontend:latest
```

## Local Testing

```bash
# Serve with any web server
python -m http.server 8080

# Or use nginx
docker run -p 80:80 weather-frontend:latest
```

## Configuration

Update API endpoint in `script.js`:
```javascript
const API_URL = 'http://localhost:5000';  // For local
const API_URL = 'http://your-ec2-ip:5000';  // For production
```

## Troubleshooting

**API connection issues:**
- Check CORS is enabled on backend
- Verify backend URL is correct
- Check browser console for errors

**Port 80 requires sudo:**
```bash
# Use different port
docker run -p 8080:80 weather-frontend:latest
```
