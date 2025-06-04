#!/usr/bin/env python3
"""
Test script for OpenWeather One Call API 3.0
This script tests if your API key works with the new API endpoint.
"""

import requests
import json
import configparser
import os

def config():
    """Read API key from config file"""
    config_parser = configparser.ConfigParser()
    config_file = os.path.join('kafka', 'weather_api_key.ini')
    config_parser.read(config_file)
    return config_parser['openweather']['key']

def test_onecall_api():
    """Test the One Call API 3.0 with a sample location (London)"""
    
    try:
        # Get API key
        api_key = config()
        print(f"Using API key: {api_key[:8]}...")
        
        # Test coordinates (London)
        lat = 51.5074
        lon = -0.1278
        
        # One Call API 3.0 endpoint
        url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric'
        
        print(f"Testing URL: {url[:80]}...")
        
        # Make request
        response = requests.get(url, timeout=10)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract current weather
            current = data['current']
            
            print("\n✅ API Test Successful!")
            print(f"Location: London ({lat}, {lon})")
            print(f"Timezone: {data['timezone']}")
            print(f"Temperature: {current['temp']}°C")
            print(f"Feels like: {current['feels_like']}°C")
            print(f"Humidity: {current['humidity']}%")
            print(f"Weather: {current['weather'][0]['description']}")
            print(f"Wind speed: {current['wind_speed']} m/s")
            print(f"UV Index: {current['uvi']}")
            
            # Show available data fields
            print(f"\nAvailable current weather fields:")
            for key in sorted(current.keys()):
                print(f"  - {key}")
                
            return True
            
        elif response.status_code == 401:
            print("\n❌ API Test Failed!")
            print("Error: Invalid API key")
            print("Please check your API key in kafka/weather_api_key.ini")
            print("Get a free API key at: https://openweathermap.org/api")
            return False
            
        elif response.status_code == 403:
            print("\n❌ API Test Failed!")
            print("Error: API key doesn't have access to One Call API 3.0")
            print("You may need to subscribe to the One Call API 3.0 plan")
            print("Check: https://openweathermap.org/api/one-call-3")
            return False
            
        else:
            print(f"\n❌ API Test Failed!")
            print(f"HTTP Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Network Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=== OpenWeather One Call API 3.0 Test ===")
    print()
    
    success = test_onecall_api()
    
    if success:
        print("\n🎉 Your API is ready for the weather pipeline!")
    else:
        print("\n💡 Please fix the API issue before running the weather producer.")
        
    print("\nNext steps:")
    print("1. If API test passed, run: python kafka/weather_kfk_producer.py")
    print("2. If API test failed, check your API key and subscription")
