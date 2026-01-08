"""
OpenWeatherMap API Test Script
Tests the API key and shows detailed responses
"""
import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5'

def print_section(title):
    """Print a section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_api_key_status():
    """Test if the API key is valid"""
    print_section("API KEY STATUS")
    print(f"API Key: {API_KEY}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test with a simple city
    test_city = "London"
    url = f"{BASE_URL}/weather"
    params = {
        'q': test_city,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    print(f"\nTesting API endpoint: {url}")
    print(f"City: {test_city}")
    print("\nSending request...\n")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Status: {'✅ SUCCESS' if response.status_code == 200 else '❌ FAILED'}")
        
        if response.status_code == 200:
            print("\nAPI Key is ACTIVE and WORKING!")
        elif response.status_code == 401:
            print("\nAPI Key is NOT YET ACTIVATED")
            print("   Please wait 1-3 hours for OpenWeatherMap to activate it.")
        else:
            print(f"\nUnexpected status code: {response.status_code}")
        
        print("\nFull Response:")
        print(json.dumps(response.json(), indent=2))
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_weather_request(city):
    """Test weather request for a specific city"""
    print_section(f"WEATHER REQUEST FOR: {city.upper()}")
    
    url = f"{BASE_URL}/weather"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        print(f"Request URL: {response.url}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\nSUCCESS - Weather Data Retrieved:")
            print(f"\n Location: {data['name']}, {data['sys']['country']}")
            print(f"Temperature: {data['main']['temp']}°C")
            print(f"Feels Like: {data['main']['feels_like']}°C")
            print(f"Humidity: {data['main']['humidity']}%")
            print(f"Condition: {data['weather'][0]['main']} - {data['weather'][0]['description']}")
            print(f"Wind Speed: {data['wind']['speed']} m/s")
            print(f"Pressure: {data['main']['pressure']} hPa")
            
            # Check for alerts
            temp = data['main']['temp']
            if temp > 35:
                print("\nALERT: High temperature warning!")
            elif temp < 5:
                print("\nALERT: Low temperature warning!")
            
            print("\n📄 Full JSON Response:")
            print(json.dumps(data, indent=2))
            
        else:
            print(f"\n FAILED")
            print(f"Error Response:")
            print(json.dumps(response.json(), indent=2))
        
    except Exception as e:
        print(f" Error: {str(e)}")

def test_forecast_request(city):
    """Test 5-day forecast request for a specific city"""
    print_section(f"5-DAY FORECAST FOR: {city.upper()}")
    
    url = f"{BASE_URL}/forecast"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        print(f"Request URL: {response.url}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\nSUCCESS - Forecast Data Retrieved:")
            print(f"\nLocation: {data['city']['name']}, {data['city']['country']}")
            print(f"Total Forecast Points: {data['cnt']}")
            
            print("\nNext 5 Days Overview:")
            
            # Group by date
            daily_data = {}
            for item in data['list'][:40]:  # First 40 entries (5 days)
                date = item['dt_txt'].split()[0]
                if date not in daily_data:
                    daily_data[date] = {
                        'temps': [],
                        'conditions': []
                    }
                daily_data[date]['temps'].append(item['main']['temp'])
                daily_data[date]['conditions'].append(item['weather'][0]['main'])
            
            for date, info in list(daily_data.items())[:5]:
                day_name = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
                min_temp = min(info['temps'])
                max_temp = max(info['temps'])
                condition = max(set(info['conditions']), key=info['conditions'].count)
                
                print(f"  {day_name} ({date}): {min_temp}°C - {max_temp}°C | {condition}")
            
            print("\nSample Forecast Entry (First):")
            print(json.dumps(data['list'][0], indent=2))
            
        else:
            print(f"\nFAILED")
            print(f"Error Response:")
            print(json.dumps(response.json(), indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    """Main test runner"""
    print("\n" + "🌤️ "*20)
    print("    OPENWEATHERMAP API TEST SUITE")
    print("🌤️ "*20)
    
    # Test 1: Check API key status
    is_active = test_api_key_status()
    
    if not is_active:
        print("\n" + "="*70)
        print(" API KEY NOT ACTIVE - Skipping further tests")
        print("="*70)
        print("\nℹ️  Once your API key is activated, run this script again to see full results.")
        return
    
    # Test 2: Test weather for multiple cities
    cities = ["Kathmandu", "London", "New York", "Tokyo", "Dubai"]
    
    for city in cities:
        test_weather_request(city)
    
    # Test 3: Test forecast
    test_forecast_request("Kathmandu")
    
    print("\n" + "="*70)
    print("  ✅ ALL TESTS COMPLETED")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
