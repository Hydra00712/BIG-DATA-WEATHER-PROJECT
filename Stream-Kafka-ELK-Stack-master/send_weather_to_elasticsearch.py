#!/usr/bin/env python3
"""
🌤️ Direct Weather to Elasticsearch Sender
Bypasses Kafka and sends weather data directly to Elasticsearch
"""

import requests
import json
import time
from datetime import datetime
import configparser

def get_api_key():
    """Get API key from config file"""
    config = configparser.ConfigParser()
    config.read('kafka/weather_api_key.ini')
    return config['openweather']['key']

def get_weather_data(city_name: str, api_key: str) -> dict:
    """Get weather data from OpenWeather API 2.5"""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            # Create structured weather data
            weather_data = {
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'timestamp': int(time.time()),
                'city_id': data['id'],
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
                'sunrise': data['sys']['sunrise'],
                'sunset': data['sys']['sunset']
            }
            
            return weather_data
        else:
            print(f"❌ Error fetching {city_name}: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception fetching {city_name}: {e}")
        return None

def send_to_elasticsearch(data: dict, index: str = "openweather"):
    """Send data directly to Elasticsearch"""
    url = f"http://localhost:9200/{index}/_doc"
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            return True
        else:
            print(f"❌ Elasticsearch error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Elasticsearch exception: {e}")
        return False

def main():
    print("🌤️ Direct Weather to Elasticsearch Sender")
    print("=" * 50)
    
    # Configuration
    cities = ["London", "Berlin", "Paris", "Barcelona", "Amsterdam", "Krakow", "Vienna"]
    api_key = get_api_key()
    
    print(f"API Key: {api_key[:8]}...")
    print(f"Cities: {cities}")
    print(f"Target: Elasticsearch (http://localhost:9200/openweather)")
    print("=" * 50)
    
    cycle = 1
    
    try:
        while True:
            print(f"\n🔄 Cycle {cycle} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 40)
            
            success_count = 0
            
            for city in cities:
                print(f"📡 Fetching {city}...", end=" ")
                
                # Get weather data
                weather_data = get_weather_data(city, api_key)
                
                if weather_data:
                    # Send to Elasticsearch
                    if send_to_elasticsearch(weather_data):
                        print(f"✅ {weather_data['temp']}°C, {weather_data['weather_description']}")
                        success_count += 1
                    else:
                        print(f"❌ Failed to send to Elasticsearch")
                else:
                    print(f"❌ Failed to fetch data")
            
            print(f"\n📊 Successfully processed {success_count}/{len(cities)} cities")
            
            if cycle >= 3:  # Just send a few cycles for testing
                print("\n✅ Sample data sent! Check Kibana for the new fields.")
                break
            
            cycle += 1
            print("\n⏰ Waiting 10 seconds before next cycle...")
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping sender...")
        print("👋 Sender stopped.")

if __name__ == "__main__":
    main()
