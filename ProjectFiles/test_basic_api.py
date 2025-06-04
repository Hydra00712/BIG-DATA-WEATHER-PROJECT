#!/usr/bin/env python3
"""
Test script for basic OpenWeather API 2.5
This tests if your API key works with the basic current weather API.
"""

import requests
import configparser
import os

def config():
    """Read API key from config file"""
    config_parser = configparser.ConfigParser()
    config_file = os.path.join('kafka', 'weather_api_key.ini')
    config_parser.read(config_file)
    return config_parser['openweather']['key']

def test_basic_api():
    """Test the basic current weather API 2.5 (free tier)"""
    
    try:
        # Get API key
        api_key = config()
        print(f"Using API key: {api_key[:8]}...")
        
        # Test with London using basic API 2.5
        city = "London"
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        
        print(f"Testing basic API with: {url[:80]}...")
        
        # Make request
        response = requests.get(url, timeout=10)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n✅ Basic API Test Successful!")
            print(f"City: {data['name']}, {data['sys']['country']}")
            print(f"Temperature: {data['main']['temp']}°C")
            print(f"Feels like: {data['main']['feels_like']}°C")
            print(f"Humidity: {data['main']['humidity']}%")
            print(f"Weather: {data['weather'][0]['description']}")
            
            return True
            
        elif response.status_code == 401:
            print("\n❌ API Test Failed!")
            print("Error: Invalid API key or key not activated yet")
            print("- Wait a few minutes for the key to activate")
            print("- Check your API key in kafka/weather_api_key.ini")
            return False
            
        else:
            print(f"\n❌ API Test Failed!")
            print(f"HTTP Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=== OpenWeather Basic API 2.5 Test ===")
    print()
    
    success = test_basic_api()
    
    if success:
        print("\n🎉 Your API key works with the basic API!")
        print("Note: One Call API 3.0 may require a subscription.")
    else:
        print("\n💡 Please check your API key and try again.")
