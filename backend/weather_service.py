"""
Weather Service Module
Handles communication with OpenWeatherMap API and data processing
"""
import requests
from datetime import datetime
from cache_layer import WeatherCache


class WeatherService:
    """Service class for weather data operations"""
    
    BASE_URL = 'https://api.openweathermap.org/data/2.5'
    
    def __init__(self, api_key, high_temp_threshold=35, low_temp_threshold=5):
        """
        Initialize weather service
        
        Args:
            api_key: OpenWeatherMap API key
            high_temp_threshold: Temperature threshold for high temp alerts
            low_temp_threshold: Temperature threshold for low temp alerts
        """
        if not api_key:
            raise ValueError('OpenWeatherMap API key is required')
        
        self.api_key = api_key
        self.high_temp_threshold = high_temp_threshold
        self.low_temp_threshold = low_temp_threshold
        self.cache = WeatherCache()
    
    def _check_temperature_alert(self, temp):
        """
        Check if temperature triggers an alert
        
        Args:
            temp: Temperature in Celsius
            
        Returns:
            Alert message or None
        """
        if temp > self.high_temp_threshold:
            return 'High temperature warning!'
        elif temp < self.low_temp_threshold:
            return 'Low temperature warning!'
        return None
    
    def get_current_weather(self, city):
        """
        Get current weather for a city
        
        Args:
            city: City name
            
        Returns:
            Dictionary with weather data
        """
        # Check cache first
        cache_key = f'weather_{city.lower()}'
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # Fetch from API
        url = f'{self.BASE_URL}/weather'
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'  # Get temperature in Celsius
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Process the data
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'humidity': data['main']['humidity'],
                'condition': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'wind_speed': round(data['wind']['speed'], 1),
                'pressure': data['main']['pressure'],
                'timestamp': datetime.utcnow().isoformat(),
                'alert': self._check_temperature_alert(data['main']['temp'])
            }
            
            # Cache the result
            self.cache.set(cache_key, weather_data)
            
            return weather_data
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(f'City "{city}" not found')
            raise Exception(f'API error: {e.response.status_code}')
        
        except requests.exceptions.RequestException as e:
            raise Exception(f'Network error: {str(e)}')
    
    def get_forecast(self, city):
        """
        Get 5-day forecast for a city
        
        Args:
            city: City name
            
        Returns:
            Dictionary with current weather and forecast data
        """
        # Check cache first
        cache_key = f'forecast_{city.lower()}'
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # Fetch from API
        url = f'{self.BASE_URL}/forecast'
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Get current weather first
            current_weather = self.get_current_weather(city)
            
            # Process forecast data (group by day)
            daily_forecasts = {}
            
            for item in data['list']:
                # Get date from timestamp
                date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                
                if date not in daily_forecasts:
                    daily_forecasts[date] = {
                        'temps': [],
                        'conditions': [],
                        'icons': []
                    }
                
                daily_forecasts[date]['temps'].append(item['main']['temp'])
                daily_forecasts[date]['conditions'].append(item['weather'][0]['main'])
                daily_forecasts[date]['icons'].append(item['weather'][0]['icon'])
            
            # Create 5-day summary
            forecast_array = []
            for date in sorted(daily_forecasts.keys())[:5]:
                day_data = daily_forecasts[date]
                
                # Get most common condition
                condition = max(set(day_data['conditions']), key=day_data['conditions'].count)
                
                # Get most common icon (prefer day icons)
                icon = max(set(day_data['icons']), key=day_data['icons'].count)
                
                forecast_array.append({
                    'date': date,
                    'day_name': datetime.strptime(date, '%Y-%m-%d').strftime('%A'),
                    'min_temp': round(min(day_data['temps']), 1),
                    'max_temp': round(max(day_data['temps']), 1),
                    'condition': condition,
                    'icon': icon
                })
            
            forecast_data = {
                'city': data['city']['name'],
                'country': data['city']['country'],
                'current': current_weather,
                'forecast': forecast_array,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Cache the result
            self.cache.set(cache_key, forecast_data)
            
            return forecast_data
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ValueError(f'City "{city}" not found')
            raise Exception(f'API error: {e.response.status_code}')
        
        except requests.exceptions.RequestException as e:
            raise Exception(f'Network error: {str(e)}')
