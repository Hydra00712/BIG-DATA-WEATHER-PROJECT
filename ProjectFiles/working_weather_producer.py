#!/usr/bin/env python3
"""
Working Kafka Weather Producer using confluent-kafka
Streams weather data from OpenWeather API to Kafka
"""

import time
import json
import requests
import configparser
import os
from confluent_kafka import Producer

# Kafka configuration
KAFKA_BOOTSTRAP_SERVER = 'localhost:9092'
KAFKA_TOPIC = 'openweather'

def config():
    """Read API key from config file"""
    config_parser = configparser.ConfigParser()
    config_file = os.path.join('kafka', 'weather_api_key.ini')
    config_parser.read(config_file)
    return config_parser['openweather']['key']

def kafka_producer():
    """Create Kafka producer with enhanced configuration"""
    conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVER,
        'client.id': 'weather-producer',
        'acks': 'all',  # Wait for all replicas to acknowledge
        'retries': 3,   # Retry failed sends
        'retry.backoff.ms': 1000,  # Wait between retries
        'compression.type': 'snappy',  # Compress messages
        'batch.size': 16384,  # Batch size for efficiency
        'linger.ms': 10  # Wait time to batch messages
    }
    return Producer(conf)

def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result."""
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def get_weather_infos(city_name: str, api_key: str) -> dict:
    """Request weather data from OpenWeather API 2.5"""
    
    openweather_endpoint = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    
    try:
        api_response = requests.get(openweather_endpoint, timeout=10)
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
        
        # Add rain/snow data if available
        if 'rain' in json_data:
            json_msg['rain_1h'] = json_data['rain'].get('1h', 0)
            json_msg['rain_3h'] = json_data['rain'].get('3h', 0)
        else:
            json_msg['rain_1h'] = 0
            json_msg['rain_3h'] = 0
            
        if 'snow' in json_data:
            json_msg['snow_1h'] = json_data['snow'].get('1h', 0)
            json_msg['snow_3h'] = json_data['snow'].get('3h', 0)
        else:
            json_msg['snow_1h'] = 0
            json_msg['snow_3h'] = 0
            
        return json_msg
        
    except Exception as e:
        print(f"Error fetching weather data for {city_name}: {e}")
        return None

def main():
    api_key = config()
    cities = ['London', 'Berlin', 'Paris', 'Barcelona', 'Amsterdam', 'Krakow', 'Vienna']
    
    print("🌤️  Starting Weather Data Kafka Producer")
    print(f"API Key: {api_key[:8]}...")
    print(f"Cities: {cities}")
    print(f"Kafka Topic: {KAFKA_TOPIC}")
    print(f"Kafka Server: {KAFKA_BOOTSTRAP_SERVER}")
    print("=" * 60)
    
    # Create Kafka producer
    producer = kafka_producer()
    
    try:
        cycle = 1
        while True:
            print(f"\n🔄 Cycle {cycle} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 40)
            
            for city_name in cities:
                try:
                    print(f"📡 Fetching {city_name}...", end=" ")
                    json_msg = get_weather_infos(city_name, api_key)
                    
                    if json_msg:
                        # Send to Kafka
                        producer.produce(
                            KAFKA_TOPIC,
                            key=city_name,
                            value=json.dumps(json_msg),
                            callback=delivery_report
                        )
                        
                        print(f"✅ {json_msg['temp']}°C, {json_msg['weather_description']}")
                    else:
                        print("❌ Failed")
                        
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            # Wait for any outstanding messages to be delivered
            producer.flush()
            
            print(f"\n⏰ Waiting 60 seconds before next cycle...")
            time.sleep(60)
            cycle += 1
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping producer...")
    finally:
        producer.flush()
        print("👋 Producer stopped.")

if __name__ == "__main__":
    main()
