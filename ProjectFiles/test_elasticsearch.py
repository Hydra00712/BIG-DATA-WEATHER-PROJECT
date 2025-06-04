#!/usr/bin/env python3
"""
Test script to send sample data directly to Elasticsearch
This bypasses Kafka and Logstash to test if Elasticsearch is working
"""

import requests
import json
from datetime import datetime

def test_elasticsearch():
    """Send sample weather data directly to Elasticsearch"""
    
    # Sample weather data
    sample_data = {
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "timestamp": int(datetime.now().timestamp()),
        "city_name": "London",
        "country": "GB",
        "temp": 15.5,
        "humidity": 65,
        "weather_description": "partly cloudy",
        "test_data": True
    }
    
    # Elasticsearch URL
    es_url = "http://localhost:9200/openweather/_doc"
    
    try:
        # Send data to Elasticsearch
        response = requests.post(
            es_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(sample_data),
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print("✅ Successfully sent test data to Elasticsearch!")
            print(f"Response: {response.json()}")
            print("\nNow go back to Kibana and try creating the index pattern again.")
            print("You should see 'openweather*' matches 1 index.")
            return True
        else:
            print(f"❌ Failed to send data. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Elasticsearch: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Elasticsearch Connection ===")
    test_elasticsearch()
