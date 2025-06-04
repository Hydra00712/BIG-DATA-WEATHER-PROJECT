#!/usr/bin/env python3
"""
Simple weather data test without Kafka
This tests the weather API and shows the data structure.
"""

import requests
import json
import configparser
import os
import time

def config():
    """Read API key from config file"""
    config_parser = configparser.ConfigParser()
    config_file = os.path.join('kafka', 'weather_api_key.ini')
    config_parser.read(config_file)
    return config_parser['openweather']['key']

def get_weather_infos(city_name: str, api_key: str) -> dict:
    '''Request the data from OpenWeather Current Weather API 2.5'''
    
    # Current Weather API 2.5 endpoint (free tier)
    openweather_endpoint = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    
    try:
        api_response = requests.get(openweather_endpoint)
        api_response.raise_for_status()
        json_data = api_response.json()
        
        json_msg = {
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': json_data['dt'],
            'city_id': json_data['id'],
            'city_name': json_data['name'],
            'country': json_data['sys']['country'],
            'lat': json_data['coord']['lat'],
            'lon': json_data['coord']['lon'],
            'temp': json_data['main']['temp'],
            'feels_like': json_data['main']['feels_like'],
            'temp_min': json_data['main']['temp_min'],
            'temp_max': json_data['main']['temp_max'],
            'pressure': json_data['main']['pressure'],
            'humidity': json_data['main']['humidity'],
            'visibility': json_data.get('visibility', 0),
            'clouds': json_data['clouds']['all'],
            'wind_speed': json_data.get('wind', {}).get('speed', 0),
            'wind_deg': json_data.get('wind', {}).get('deg', 0),
            'weather_main': json_data['weather'][0]['main'],
            'weather_description': json_data['weather'][0]['description'],
            'weather_icon': json_data['weather'][0]['icon'],
            'sunrise': json_data['sys']['sunrise'],
            'sunset': json_data['sys']['sunset']
        }
        
        return json_msg
        
    except Exception as e:
        print(f"Error fetching weather data for {city_name}: {e}")
        return None

def main():
    api_key = config()
    cities = ['London', 'Berlin', 'Paris']
    
    print("=== Weather Data Test ===")
    print(f"API Key: {api_key[:8]}...")
    print(f"Testing cities: {cities}")
    print("-" * 50)
    
    for city_name in cities:
        print(f"\nFetching weather data for {city_name}...")
        json_msg = get_weather_infos(city_name, api_key)
        
        if json_msg:
            print(f"✓ {city_name}: {json_msg['temp']}°C, {json_msg['weather_description']}")
            print(f"  Humidity: {json_msg['humidity']}%, Wind: {json_msg['wind_speed']} m/s")
            print(f"  Data structure preview:")
            print(f"  {json.dumps(json_msg, indent=2)[:200]}...")
        else:
            print(f"✗ Failed to get weather data for {city_name}")
    
    print("\n" + "=" * 50)
    print("Weather data test complete!")
    print("If this works, we can proceed with Kafka integration.")

if __name__ == "__main__":
    main()
