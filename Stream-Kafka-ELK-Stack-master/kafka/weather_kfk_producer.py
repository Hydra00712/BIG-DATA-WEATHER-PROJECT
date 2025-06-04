'''Kafka Producer

Extract weather data from OpenWeather One Call API 3.0 (https://openweathermap.org/api/one-call-3) to kafka.
'''

import time
import json
import requests
from config import config
from kafka import KafkaProducer

#kfk_bootstrap_server = 'localhost:9092'
kfk_bootstrap_server = '127.0.0.1:9092'

def kafka_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=[kfk_bootstrap_server],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

# City coordinates for One Call API
CITIES = {
    'London': {'lat': 51.5074, 'lon': -0.1278},
    'Berlin': {'lat': 52.5200, 'lon': 13.4050},
    'Paris': {'lat': 48.8566, 'lon': 2.3522},
    'Barcelona': {'lat': 41.3851, 'lon': 2.1734},
    'Amsterdam': {'lat': 52.3676, 'lon': 4.9041},
    'Krakow': {'lat': 50.0647, 'lon': 19.9450},
    'Vienna': {'lat': 48.2082, 'lon': 16.3738}
}

def get_weather_infos(city_name: str, api_key: str) -> dict:
    '''Request the data from OpenWeather Current Weather API 2.5

    Params:
    -------
        city_name - str: Name of the city
        api_key - str: OpenWeather API key

    Return:
    -------
        json_msg: return the message to be send to kafka.
    '''
    # Current Weather API 2.5 endpoint (free tier)
    openweather_endpoint = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'

    try:
        api_response = requests.get(openweather_endpoint)
        api_response.raise_for_status()  # Raise an exception for bad status codes
        json_data = api_response.json()

        json_msg = {
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': json_data['dt'],
            'city_id': json_data['id'],
            'city_name': json_data['name'],
            'country': json_data['sys']['country'],
            'lat': json_data['coord']['lat'],
            'lon': json_data['coord']['lon'],
            'timezone': json_data.get('timezone', 0),
            # Current weather
            'temp': json_data['main']['temp'],
            'feels_like': json_data['main']['feels_like'],
            'temp_min': json_data['main']['temp_min'],
            'temp_max': json_data['main']['temp_max'],
            'pressure': json_data['main']['pressure'],
            'humidity': json_data['main']['humidity'],
            'sea_level': json_data['main'].get('sea_level', 0),
            'grnd_level': json_data['main'].get('grnd_level', 0),
            'visibility': json_data.get('visibility', 0),
            'clouds': json_data['clouds']['all'],
            'wind_speed': json_data.get('wind', {}).get('speed', 0),
            'wind_deg': json_data.get('wind', {}).get('deg', 0),
            'wind_gust': json_data.get('wind', {}).get('gust', 0),
            'weather_main': json_data['weather'][0]['main'],
            'weather_description': json_data['weather'][0]['description'],
            'weather_icon': json_data['weather'][0]['icon'],
            'sunrise': json_data['sys']['sunrise'],
            'sunset': json_data['sys']['sunset']
        }

        # Add rain data if available
        if 'rain' in json_data:
            json_msg['rain_1h'] = json_data['rain'].get('1h', 0)
            json_msg['rain_3h'] = json_data['rain'].get('3h', 0)
        else:
            json_msg['rain_1h'] = 0
            json_msg['rain_3h'] = 0

        # Add snow data if available
        if 'snow' in json_data:
            json_msg['snow_1h'] = json_data['snow'].get('1h', 0)
            json_msg['snow_3h'] = json_data['snow'].get('3h', 0)
        else:
            json_msg['snow_1h'] = 0
            json_msg['snow_3h'] = 0

        return json_msg

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data for {city_name}: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing weather data for {city_name}: {e}")
        return None

def main():
    kfk_topic = 'openweather'
    api_key = config()
    cities = ['London', 'Berlin', 'Paris', 'Barcelona', 'Amsterdam', 'Krakow', 'Vienna']

    print("Starting OpenWeather Current Weather API 2.5 Kafka Producer...")
    print(f"API Key: {api_key[:8]}..." if api_key else "No API key found!")
    print(f"Cities to monitor: {cities}")
    print(f"Kafka topic: {kfk_topic}")
    print(f"Kafka server: {kfk_bootstrap_server}")
    print("-" * 50)

    while True:
        for city_name in cities:
            try:
                print(f"Fetching weather data for {city_name}...")
                json_msg = get_weather_infos(city_name, api_key)

                if json_msg:
                    producer = kafka_producer()
                    if isinstance(producer, KafkaProducer):
                        producer.send(kfk_topic, json_msg)
                        producer.flush()  # Ensure message is sent
                        print(f'✓ Published {city_name}: {json_msg["temp"]}°C, {json_msg["weather_description"]}')
                    else:
                        print(f'✗ Failed to create Kafka producer for {city_name}')
                else:
                    print(f'✗ Failed to get weather data for {city_name}')

            except Exception as e:
                print(f'✗ Error processing {city_name}: {e}')

        sleep = 60
        print(f'Waiting {sleep} seconds before next cycle...')
        print("-" * 50)
        time.sleep(sleep)

if __name__=="__main__":
    main()
