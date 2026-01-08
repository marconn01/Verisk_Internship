import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from weather_service import WeatherService
from utils import setup_logging, get_recent_logs

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes and origins

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize weather service
weather_service = WeatherService(
    api_key=os.getenv('OPENWEATHER_API_KEY'),
    high_temp_threshold=float(os.getenv('HIGH_TEMP_THRESHOLD', 35)),
    low_temp_threshold=float(os.getenv('LOW_TEMP_THRESHOLD', 5))
)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    logger.info('Health check endpoint accessed')
    return jsonify({'status': 'ok'}), 200


@app.route('/weather', methods=['GET'])
def get_weather():
    """
    Get current weather for a city
    Query params: city (required)
    """
    city = request.args.get('city')
    
    if not city:
        logger.warning('Weather request without city parameter')
        return jsonify({'error': 'City parameter is required'}), 400
    
    try:
        logger.info(f'Weather request for city: {city}')
        weather_data = weather_service.get_current_weather(city)
        
        # Log any alerts
        if weather_data.get('alert'):
            logger.warning(f'Alert for {city}: {weather_data["alert"]}')
        
        logger.info(f'Weather request successful for {city} - Status: 200')
        return jsonify(weather_data), 200
        
    except ValueError as e:
        logger.error(f'Invalid city error for {city}: {str(e)}')
        return jsonify({'error': str(e)}), 404
        
    except Exception as e:
        logger.error(f'Error fetching weather for {city}: {str(e)}')
        return jsonify({'error': 'Failed to fetch weather data'}), 500


@app.route('/forecast', methods=['GET'])
def get_forecast():

    city = request.args.get('city')
    
    if not city:
        logger.warning('Forecast request without city parameter')
        return jsonify({'error': 'City parameter is required'}), 400
    
    try:
        logger.info(f'Forecast request for city: {city}')
        forecast_data = weather_service.get_forecast(city)
        
        # Log any alerts in current conditions
        if forecast_data.get('current', {}).get('alert'):
            logger.warning(f'Alert for {city}: {forecast_data["current"]["alert"]}')
        
        logger.info(f'Forecast request successful for {city} - Status: 200')
        return jsonify(forecast_data), 200
        
    except ValueError as e:
        logger.error(f'Invalid city error for {city}: {str(e)}')
        return jsonify({'error': str(e)}), 404
        
    except Exception as e:
        logger.error(f'Error fetching forecast for {city}: {str(e)}')
        return jsonify({'error': 'Failed to fetch forecast data'}), 500


@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Get last 10 log entries
    """
    try:
        logs = get_recent_logs(count=10)
        return jsonify({'logs': logs}), 200
    except Exception as e:
        logger.error(f'Error fetching logs: {str(e)}')
        return jsonify({'error': 'Failed to fetch logs'}), 500
    


@app.route('/health')
def health():
    return {"status": "healthy"}, 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f'Internal server error: {str(error)}')
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f'Starting Flask application on port {port}')
    app.run(host='0.0.0.0', port=port, debug=debug)
