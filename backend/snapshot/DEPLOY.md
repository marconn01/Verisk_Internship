# Snapshot Services Deployment

## Producer (Data Collection)

### Build
```bash
cd backend
docker build -f snapshot/Dockerfile.snapshot.producer -t weather-snapshot:producer .
```

### Push to ECR
```bash
docker tag weather-snapshot:producer ${ECR_REGISTRY}/weather-snapshot:producer
docker push ${ECR_REGISTRY}/weather-snapshot:producer
```

### Set up Cron Job
On EC2:
```bash
# Edit crontab
crontab -e

# Add hourly job
0 * * * * docker run --env-file /home/ubuntu/weather-app/.env ${ECR_REGISTRY}/weather-snapshot:producer
```

## Consumer (Data Processing)

### Build
```bash
cd backend
docker build -f snapshot/Dockerfile.snapshot.consumer -t weather-snapshot:consumer .
```

### Push to ECR
```bash
docker tag weather-snapshot:consumer ${ECR_REGISTRY}/weather-snapshot:consumer
docker push ${ECR_REGISTRY}/weather-snapshot:consumer
```

### Run Continuously
Included in docker-compose.yml - starts automatically.

## Environment Variables

Required:
- `OPENWEATHER_API_KEY`
- `AWS_REGION`
- `WEATHER_BUCKET_NAME` (S3)
- `SQS_QUEUE_URL`
- `DYNAMODB_TABLE_NAME`

## Testing

### Test Producer
```bash
python snapshot/snapshot_producer.py
```

Check:
- S3 bucket for new files
- SQS queue for messages

### Test Consumer
```bash
python snapshot/snapshot_consumer.py
```

Check:
- SQS messages being consumed
- DynamoDB for new records
- CloudWatch logs

## Troubleshooting

**IAM permission errors:**
- Ensure EC2 has IAM role attached
- Check role has S3, SQS, DynamoDB permissions

**SQS message not processing:**
```bash
# Check queue
aws sqs get-queue-attributes --queue-url $SQS_QUEUE_URL

# View messages
aws sqs receive-message --queue-url $SQS_QUEUE_URL
```

**DynamoDB write errors:**
- Check table exists
- Verify partition key format (city name)
- Ensure using Decimal for numbers
