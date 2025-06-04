#!/usr/bin/env python3
"""
🎯 Kibana Dashboard Setup Helper
Automates the creation of index patterns and basic visualizations
"""

import requests
import json
import time
from datetime import datetime

# Configuration
KIBANA_URL = "http://localhost:5601"
ELASTICSEARCH_URL = "http://localhost:9200"
INDEX_PATTERN = "openweather*"
CITIES = ["London", "Berlin", "Paris", "Barcelona", "Amsterdam", "Krakow", "Vienna"]

def check_elasticsearch():
    """Check if Elasticsearch is running and has data"""
    try:
        response = requests.get(f"{ELASTICSEARCH_URL}/_cluster/health")
        if response.status_code == 200:
            print("✅ Elasticsearch is running")
            
            # Check for data
            data_response = requests.get(f"{ELASTICSEARCH_URL}/openweather/_count")
            if data_response.status_code == 200:
                count = data_response.json().get('count', 0)
                print(f"✅ Found {count} weather records")
                return count > 0
            else:
                print("❌ No weather data found")
                return False
        else:
            print("❌ Elasticsearch not responding")
            return False
    except Exception as e:
        print(f"❌ Error connecting to Elasticsearch: {e}")
        return False

def check_kibana():
    """Check if Kibana is running"""
    try:
        response = requests.get(f"{KIBANA_URL}/api/status")
        if response.status_code == 200:
            print("✅ Kibana is running")
            return True
        else:
            print("❌ Kibana not responding")
            return False
    except Exception as e:
        print(f"❌ Error connecting to Kibana: {e}")
        return False

def create_index_pattern():
    """Create the openweather index pattern in Kibana"""
    try:
        # First, check if index pattern already exists
        check_url = f"{KIBANA_URL}/api/saved_objects/index-pattern/openweather*"
        check_response = requests.get(check_url)
        
        if check_response.status_code == 200:
            print("✅ Index pattern 'openweather*' already exists")
            return True
        
        # Create new index pattern
        headers = {
            'Content-Type': 'application/json',
            'kbn-xsrf': 'true'
        }
        
        payload = {
            "attributes": {
                "title": "openweather*",
                "timeFieldName": "created_at"
            }
        }
        
        url = f"{KIBANA_URL}/api/saved_objects/index-pattern/openweather*"
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            print("✅ Successfully created index pattern 'openweather*'")
            return True
        else:
            print(f"❌ Failed to create index pattern: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating index pattern: {e}")
        return False

def get_sample_data():
    """Get sample data to understand the structure"""
    try:
        response = requests.get(f"{ELASTICSEARCH_URL}/openweather/_search?size=1")
        if response.status_code == 200:
            data = response.json()
            if data['hits']['total']['value'] > 0:
                sample = data['hits']['hits'][0]['_source']
                print("\n📊 Sample data structure:")
                for key, value in sample.items():
                    print(f"  {key}: {value}")
                return sample
        return None
    except Exception as e:
        print(f"❌ Error getting sample data: {e}")
        return None

def print_dashboard_instructions():
    """Print step-by-step dashboard creation instructions"""
    print("\n" + "="*60)
    print("🎯 NEXT STEPS: Create Your Dashboard in Kibana")
    print("="*60)
    
    print(f"\n1. 🌐 Open Kibana: {KIBANA_URL}")
    print("\n2. 📊 Go to 'Visualize' → 'Create visualization'")
    
    print("\n3. 🏗️ Create these visualizations for each city:")
    print("   📈 Temperature Line Chart:")
    print("      - Chart type: Line")
    print("      - Y-axis: Average of 'temp'")
    print("      - X-axis: Date Histogram of 'created_at'")
    print("      - Filter: city_name.keyword = 'CityName'")
    
    print("\n   🌡️ Feels Like Metric:")
    print("      - Chart type: Metric")
    print("      - Metric: Top Hit of 'feels_like'")
    print("      - Filter: city_name.keyword = 'CityName'")
    
    print("\n   💧 Humidity Metric:")
    print("      - Chart type: Metric")
    print("      - Metric: Top Hit of 'humidity'")
    print("      - Filter: city_name.keyword = 'CityName'")
    
    print(f"\n4. 🎨 Create dashboard with {len(CITIES)} cities:")
    for i, city in enumerate(CITIES, 1):
        print(f"   {i}. {city}")
    
    print("\n5. 📐 Layout: 4 columns × 6 rows grid")
    print("6. 🔄 Set auto-refresh: 1 minute")
    print("7. ⏰ Time range: Last 24 hours")
    
    print(f"\n📖 For detailed guide, see: KIBANA_DASHBOARD_GUIDE.md")

def main():
    print("🚀 Kibana Dashboard Setup Helper")
    print("="*50)
    
    # Check services
    if not check_elasticsearch():
        print("\n❌ Please ensure Elasticsearch is running and has weather data")
        print("💡 Run the weather producer first: python working_weather_producer.py")
        return
    
    if not check_kibana():
        print("\n❌ Please ensure Kibana is running")
        print("💡 Check if Kibana container is up: docker ps")
        return
    
    # Wait a moment for services to be ready
    print("\n⏳ Waiting for services to be ready...")
    time.sleep(3)
    
    # Create index pattern
    if create_index_pattern():
        print("\n✅ Setup complete!")
        
        # Show sample data
        get_sample_data()
        
        # Print instructions
        print_dashboard_instructions()
        
        print("\n🎉 You're ready to create your dashboard!")
        print(f"🌐 Go to: {KIBANA_URL}")
        
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()
