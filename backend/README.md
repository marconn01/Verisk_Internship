# Weather Alert Backend API

Flask-based REST API for weather alerts with caching and logging.

## Features

- Current weather data
- 5-day weather forecast
- Temperature-based alerts
- In-memory caching (10-minute TTL)
- Request logging
- Health check endpoint
- CORS enabled

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Edit the `.env` file and add your OpenWeatherMap API key:

```env
OPENWEATHER_API_KEY=your_actual_api_key_here
```

Get a free API key from: https://openweathermap.org/api

### 3. Run the Application

```bash
python app.py
```

The API will start on `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /health
```
Returns: `{"status": "ok"}`

### Current Weather
```
GET /weather?city=<city_name>
```
Example: `http://localhost:5000/weather?city=London`

Response:
```json
{
  "city": "London",
  "country": "GB",
  "temperature": 15.2,
  "humidity": 72,
  "condition": "Clouds",
  "description": "broken clouds",
  "wind_speed": 4.5,
  "timestamp": "2025-11-12T10:30:00",
  "alert": null
}
```

### 5-Day Forecast
```
GET /forecast?city=<city_name>
```
Example: `http://localhost:5000/forecast?city=Paris`

Response:
```json
{
  "city": "Paris",
  "current": { /* current weather data */ },
  "forecast": [
    {
      "date": "2025-11-12",
      "day_name": "Tuesday",
      "min_temp": 10.5,
      "max_temp": 18.2,
      "condition": "Clear",
      "icon": "01d"
    }
  ]
}
```

### Logs
```
GET /logs
```
Returns last 10 log entries.

## Temperature Alerts

- **High Temperature**: Alert when temp > 35°C (configurable)
- **Low Temperature**: Alert when temp < 5°C (configurable)

## Project Structure

```
backend/
├── app.py              # Main Flask application
├── weather_service.py  # Weather API service
├── cache_layer.py      # Caching implementation
├── utils.py            # Utility functions
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
├── logs/
│   └── app.log        # Application logs
└── README.md          # This file
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | Required |
| `HIGH_TEMP_THRESHOLD` | High temp alert threshold (°C) | 35 |
| `LOW_TEMP_THRESHOLD` | Low temp alert threshold (°C) | 5 |
| `CACHE_TTL_SECONDS` | Cache expiry time | 600 |
| `PORT` | Server port | 5000 |
| `FLASK_ENV` | Environment (development/production) | development |

## Error Handling

- **400**: Missing required parameters
- **404**: City not found
- **500**: Server/API errors

## Caching

- Weather data is cached for 10 minutes (configurable)
- Reduces API calls and improves response time
- Thread-safe implementation

## Logging

All requests are logged to `logs/app.log` with:
- Timestamp
- City name
- Response status
- Any alerts triggered

## Production Deployment

For production:
1. Set `FLASK_ENV=production` in `.env`
2. Use a production WSGI server (e.g., Gunicorn)
3. Set up proper environment variable management
4. Configure log rotation
5. Use external caching (Redis) for scalability

## License

MIT
