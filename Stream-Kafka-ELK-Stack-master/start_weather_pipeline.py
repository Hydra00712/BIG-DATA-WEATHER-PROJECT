#!/usr/bin/env python3
"""
Complete Weather Pipeline Starter
This script sends weather data directly to Elasticsearch to build the dashboard
"""

import requests
import json
import time
import configparser
import os
from datetime import datetime

def config():
    """Read API key from config file"""
    config_parser = configparser.ConfigParser()
    config_file = os.path.join('kafka', 'weather_api_key.ini')
    config_parser.read(config_file)
    return config_parser['openweather']['key']

def get_weather_data(city_name: str, api_key: str) -> dict:
    """Get weather data from OpenWeather API"""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return {
            '@timestamp': datetime.utcnow().isoformat(),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': data['dt'],
            'city_name': data['name'],
            'country': data['sys']['country'],
            'lat': data['coord']['lat'],
            'lon': data['coord']['lon'],
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'visibility': data.get('visibility', 0),
            'clouds': data['clouds']['all'],
            'wind_speed': data.get('wind', {}).get('speed', 0),
            'wind_deg': data.get('wind', {}).get('deg', 0),
            'weather_main': data['weather'][0]['main'],
            'weather_description': data['weather'][0]['description'],
            'weather_icon': data['weather'][0]['icon'],
            'sunrise': data['sys']['sunrise'],
            'sunset': data['sys']['sunset']
        }
    except Exception as e:
        print(f"Error fetching {city_name}: {e}")
        return None

def send_to_elasticsearch(data):
    """Send data directly to Elasticsearch"""
    es_url = "http://localhost:9200/openweather/_doc"
    
    try:
        response = requests.post(
            es_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
            timeout=10
        )
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"Error sending to Elasticsearch: {e}")
        return False

def main():
    """Main pipeline function"""
    api_key = config()
    cities = ['London', 'Berlin', 'Paris', 'Barcelona', 'Amsterdam', 'Krakow', 'Vienna']
    
    print("🌤️  Starting Weather Dashboard Data Pipeline")
    print(f"Cities: {cities}")
    print(f"API Key: {api_key[:8]}...")
    print("=" * 60)
    
    cycle = 1
    while True:
        print(f"\n🔄 Cycle {cycle} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 40)
        
        for city in cities:
            print(f"📡 {city}...", end=" ")
            
            # Get weather data
            weather_data = get_weather_data(city, api_key)
            
            if weather_data:
                # Send to Elasticsearch
                if send_to_elasticsearch(weather_data):
                    print(f"✅ {weather_data['temp']}°C, {weather_data['weather_description']}")
                else:
                    print("❌ Failed to send to ES")
            else:
                print("❌ Failed to fetch")
        
        print(f"\n⏰ Waiting 60 seconds... (Cycle {cycle} complete)")
        print("💡 Check Kibana Discover to see new data!")
        
        time.sleep(60)
        cycle += 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Pipeline stopped by user")
    except Exception as e:
        print(f"\n❌ Pipeline error: {e}")
