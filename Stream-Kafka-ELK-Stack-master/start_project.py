#!/usr/bin/env python3
"""
🚀 Complete Weather Dashboard Project Startup Script
Starts all Docker services and verifies the complete pipeline
"""

import subprocess
import time
import requests
import json
import sys
import os

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"🎯 {title}")
    print("=" * 60)

def print_step(step, description):
    """Print formatted step"""
    print(f"\n📋 Step {step}: {description}")
    print("-" * 40)

def run_command(command, description, check=True):
    """Run shell command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"❌ {description} - Failed")
            print(f"Error: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed with error: {e}")
        return False

def check_service(url, service_name, timeout=60):
    """Check if service is responding"""
    print(f"🔍 Checking {service_name}...")
    
    for i in range(timeout):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name} is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if i % 10 == 0:
            print(f"⏳ Waiting for {service_name}... ({i}/{timeout}s)")
        time.sleep(1)
    
    print(f"❌ {service_name} failed to start within {timeout} seconds")
    return False

def check_kafka_topics():
    """Check if Kafka topics exist"""
    print("🔍 Checking Kafka topics...")
    try:
        result = subprocess.run([
            'docker', 'exec', 'kafka', 
            'kafka-topics', '--bootstrap-server', 'localhost:9092', '--list'
        ], capture_output=True, text=True, timeout=30)
        
        if 'openweather' in result.stdout:
            print("✅ Kafka topic 'openweather' exists")
            return True
        else:
            print("⚠️ Creating Kafka topic 'openweather'...")
            create_result = subprocess.run([
                'docker', 'exec', 'kafka',
                'kafka-topics', '--create', '--topic', 'openweather',
                '--bootstrap-server', 'localhost:9092',
                '--partitions', '3', '--replication-factor', '1'
            ], capture_output=True, text=True)
            
            if create_result.returncode == 0:
                print("✅ Kafka topic 'openweather' created")
                return True
            else:
                print("❌ Failed to create Kafka topic")
                return False
                
    except subprocess.TimeoutExpired:
        print("❌ Timeout checking Kafka topics")
        return False
    except Exception as e:
        print(f"❌ Error checking Kafka topics: {e}")
        return False

def verify_api_key():
    """Verify API key exists"""
    print("🔍 Checking API key configuration...")
    
    api_key_file = os.path.join('kafka', 'weather_api_key.ini')
    if not os.path.exists(api_key_file):
        print("❌ API key file not found!")
        print("📝 Please create kafka/weather_api_key.ini with your OpenWeather API key")
        print("   Format:")
        print("   [openweather]")
        print("   key=YOUR_API_KEY_HERE")
        print("\n🌐 Get free API key from: https://openweathermap.org/api")
        return False
    
    try:
        with open(api_key_file, 'r') as f:
            content = f.read()
            if 'YOUR_API_KEY_HERE' in content:
                print("❌ Please replace YOUR_API_KEY_HERE with your actual API key")
                return False
            elif len(content.strip()) < 20:
                print("❌ API key file seems incomplete")
                return False
            else:
                print("✅ API key configuration found")
                return True
    except Exception as e:
        print(f"❌ Error reading API key file: {e}")
        return False

def main():
    """Main startup sequence"""
    print_header("Weather Dashboard Project Startup")
    
    # Step 1: Verify prerequisites
    print_step(1, "Verify Prerequisites")
    
    if not verify_api_key():
        print("\n🛑 Cannot continue without valid API key")
        sys.exit(1)
    
    # Check Docker
    if not run_command("docker --version", "Check Docker installation"):
        print("🛑 Docker is required. Please install Docker Desktop")
        sys.exit(1)
    
    # Step 2: Start Docker services
    print_step(2, "Start Docker Services")
    
    # Stop any existing containers
    run_command("docker-compose down", "Stop existing containers", check=False)
    
    # Start all services
    if not run_command("docker-compose up -d", "Start all Docker services"):
        print("🛑 Failed to start Docker services")
        sys.exit(1)
    
    # Step 3: Wait for services to be ready
    print_step(3, "Wait for Services to Start")
    
    services = [
        ("http://localhost:9200/_cluster/health", "Elasticsearch"),
        ("http://localhost:5601/api/status", "Kibana"),
    ]
    
    all_ready = True
    for url, name in services:
        if not check_service(url, name):
            all_ready = False
    
    if not all_ready:
        print("🛑 Some services failed to start")
        sys.exit(1)
    
    # Step 4: Verify Kafka
    print_step(4, "Verify Kafka Configuration")
    
    if not check_kafka_topics():
        print("🛑 Kafka configuration failed")
        sys.exit(1)
    
    # Step 5: Create HTML Dashboard
    print_step(5, "Generate HTML Dashboard")
    
    if not run_command("python create_html_dashboard.py", "Generate HTML dashboard"):
        print("⚠️ HTML dashboard generation failed, but continuing...")
    
    # Step 6: Display access information
    print_step(6, "Project Ready!")
    
    print("\n🎉 Weather Dashboard Project is now running!")
    print("\n🌐 Access Points:")
    print("   📊 Kibana Dashboard:     http://localhost:5601")
    print("   🔍 Elasticsearch:        http://localhost:9200")
    print("   📱 HTML Dashboard:       weather_dashboard.html")
    print("   🐳 Docker Containers:    docker ps")
    
    print("\n🚀 Next Steps:")
    print("   1. Start weather data collection:")
    print("      python working_weather_producer.py")
    print("\n   2. Open HTML dashboard:")
    print("      Double-click weather_dashboard.html")
    print("\n   3. Setup Kibana dashboard:")
    print("      python setup_kibana_dashboard.py")
    
    print("\n⏹️  To stop all services:")
    print("      docker-compose down")
    
    print("\n📊 Monitor logs:")
    print("      docker-compose logs -f")

if __name__ == "__main__":
    main()
