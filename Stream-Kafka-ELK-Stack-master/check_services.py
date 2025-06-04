#!/usr/bin/env python3
"""
🔍 Service Health Check Script
Verifies all components are running correctly
"""

import requests
import subprocess
import json
import time
from datetime import datetime

def check_elasticsearch():
    """Check Elasticsearch health"""
    try:
        # Check cluster health
        response = requests.get('http://localhost:9200/_cluster/health', timeout=5)
        if response.status_code == 200:
            health = response.json()
            status = health.get('status', 'unknown')
            
            if status == 'green':
                print("✅ Elasticsearch: Healthy (Green)")
            elif status == 'yellow':
                print("⚠️ Elasticsearch: Warning (Yellow)")
            else:
                print("❌ Elasticsearch: Unhealthy (Red)")
            
            # Check indices
            indices_response = requests.get('http://localhost:9200/_cat/indices?format=json', timeout=5)
            if indices_response.status_code == 200:
                indices = indices_response.json()
                weather_indices = [idx for idx in indices if 'weather' in idx.get('index', '')]
                print(f"📊 Weather indices: {len(weather_indices)}")
                
                # Check document count
                if weather_indices:
                    count_response = requests.get('http://localhost:9200/weather-data-*/_count', timeout=5)
                    if count_response.status_code == 200:
                        count = count_response.json().get('count', 0)
                        print(f"📄 Total weather documents: {count}")
            
            return True
        else:
            print(f"❌ Elasticsearch: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Elasticsearch: Connection failed - {e}")
        return False

def check_kibana():
    """Check Kibana health"""
    try:
        response = requests.get('http://localhost:5601/api/status', timeout=10)
        if response.status_code == 200:
            status = response.json()
            overall_status = status.get('status', {}).get('overall', {}).get('state', 'unknown')
            
            if overall_status == 'green':
                print("✅ Kibana: Healthy")
            else:
                print(f"⚠️ Kibana: Status {overall_status}")
            
            return True
        else:
            print(f"❌ Kibana: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Kibana: Connection failed - {e}")
        return False

def check_kafka():
    """Check Kafka health"""
    try:
        # Check if Kafka container is running
        result = subprocess.run(['docker', 'ps', '--filter', 'name=kafka', '--format', '{{.Status}}'], 
                              capture_output=True, text=True, timeout=10)
        
        if 'Up' in result.stdout:
            print("✅ Kafka: Container running")
            
            # Check topics
            topics_result = subprocess.run([
                'docker', 'exec', 'kafka', 
                'kafka-topics', '--bootstrap-server', 'localhost:9092', '--list'
            ], capture_output=True, text=True, timeout=15)
            
            if topics_result.returncode == 0:
                topics = topics_result.stdout.strip().split('\n')
                print(f"📋 Kafka topics: {len(topics)}")
                
                if 'openweather' in topics:
                    print("✅ Weather topic exists")
                    
                    # Check topic details
                    describe_result = subprocess.run([
                        'docker', 'exec', 'kafka',
                        'kafka-topics', '--bootstrap-server', 'localhost:9092',
                        '--describe', '--topic', 'openweather'
                    ], capture_output=True, text=True, timeout=10)
                    
                    if describe_result.returncode == 0:
                        lines = describe_result.stdout.strip().split('\n')
                        for line in lines:
                            if 'PartitionCount' in line:
                                print(f"📊 {line.strip()}")
                else:
                    print("⚠️ Weather topic not found")
                
                return True
            else:
                print("❌ Kafka: Cannot list topics")
                return False
        else:
            print("❌ Kafka: Container not running")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Kafka: Command timeout")
        return False
    except Exception as e:
        print(f"❌ Kafka: Error - {e}")
        return False

def check_logstash():
    """Check Logstash health"""
    try:
        # Check if Logstash container is running
        result = subprocess.run(['docker', 'ps', '--filter', 'name=logstash', '--format', '{{.Status}}'], 
                              capture_output=True, text=True, timeout=10)
        
        if 'Up' in result.stdout:
            print("✅ Logstash: Container running")
            
            # Try to check Logstash API (if available)
            try:
                response = requests.get('http://localhost:9600', timeout=5)
                if response.status_code == 200:
                    print("✅ Logstash: API responding")
                else:
                    print("⚠️ Logstash: API not responding")
            except:
                print("⚠️ Logstash: API check failed (normal for some versions)")
            
            return True
        else:
            print("❌ Logstash: Container not running")
            return False
            
    except Exception as e:
        print(f"❌ Logstash: Error - {e}")
        return False

def check_docker_containers():
    """Check all Docker containers"""
    try:
        result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("\n🐳 Docker Containers:")
            print(result.stdout)
            return True
        else:
            print("❌ Cannot list Docker containers")
            return False
            
    except Exception as e:
        print(f"❌ Docker: Error - {e}")
        return False

def check_weather_data_flow():
    """Check if weather data is flowing"""
    try:
        # Check recent data in Elasticsearch
        query = {
            "query": {
                "range": {
                    "@timestamp": {
                        "gte": "now-5m"
                    }
                }
            },
            "size": 1,
            "sort": [{"@timestamp": {"order": "desc"}}]
        }
        
        response = requests.post(
            'http://localhost:9200/weather-data-*/_search',
            json=query,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            hits = data.get('hits', {}).get('hits', [])
            
            if hits:
                latest = hits[0]['_source']
                timestamp = latest.get('@timestamp', 'unknown')
                city = latest.get('city_name', 'unknown')
                temp = latest.get('temp', 'unknown')
                
                print(f"✅ Latest weather data: {city} - {temp}°C at {timestamp}")
                return True
            else:
                print("⚠️ No recent weather data found")
                return False
        else:
            print(f"❌ Cannot query weather data: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"⚠️ Weather data check failed: {e}")
        return False

def main():
    """Main health check"""
    print("🔍 Weather Dashboard Health Check")
    print("=" * 50)
    print(f"⏰ Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check all services
    services = [
        ("Elasticsearch", check_elasticsearch),
        ("Kibana", check_kibana),
        ("Kafka", check_kafka),
        ("Logstash", check_logstash),
    ]
    
    results = {}
    for name, check_func in services:
        print(f"\n🔍 Checking {name}...")
        results[name] = check_func()
    
    # Check Docker containers
    print(f"\n🔍 Checking Docker Containers...")
    check_docker_containers()
    
    # Check data flow
    print(f"\n🔍 Checking Data Flow...")
    results["Data Flow"] = check_weather_data_flow()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Health Check Summary:")
    
    healthy_count = 0
    total_count = len(results)
    
    for service, status in results.items():
        icon = "✅" if status else "❌"
        print(f"   {icon} {service}")
        if status:
            healthy_count += 1
    
    print(f"\n🎯 Overall Health: {healthy_count}/{total_count} services healthy")
    
    if healthy_count == total_count:
        print("🎉 All systems operational!")
    elif healthy_count >= total_count * 0.8:
        print("⚠️ Most systems operational, some issues detected")
    else:
        print("🚨 Multiple system issues detected")
    
    print("\n🔧 Troubleshooting:")
    print("   • Restart services: docker-compose restart")
    print("   • View logs: docker-compose logs -f")
    print("   • Full restart: docker-compose down && docker-compose up -d")

if __name__ == "__main__":
    main()
