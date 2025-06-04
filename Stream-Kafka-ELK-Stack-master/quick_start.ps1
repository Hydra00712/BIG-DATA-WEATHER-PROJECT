# Quick Start Script for Kafka + ELK Weather Pipeline
# Run this script to check prerequisites and start the pipeline

Write-Host "=== Kafka + ELK Weather Pipeline Quick Start ===" -ForegroundColor Cyan
Write-Host ""

# Check Docker
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker not found. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.7+ first." -ForegroundColor Red
    exit 1
}

# Check API key
Write-Host "Checking API key configuration..." -ForegroundColor Yellow
if (Test-Path "kafka/weather_api_key.ini") {
    $apiKeyContent = Get-Content "kafka/weather_api_key.ini"
    if ($apiKeyContent -match "YOUR_API_KEY_HERE") {
        Write-Host "✗ Please update your API key in kafka/weather_api_key.ini" -ForegroundColor Red
        Write-Host "  Get your key from: https://openweathermap.org/api" -ForegroundColor Yellow
        exit 1
    } else {
        Write-Host "✓ API key configuration found" -ForegroundColor Green
    }
} else {
    Write-Host "✗ API key file not found. Please create kafka/weather_api_key.ini" -ForegroundColor Red
    exit 1
}

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "✓ Python dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to install Python dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Prerequisites Check Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Start Elasticsearch & Kibana: cd elk && .\start_elastic_docker.ps1" -ForegroundColor White
Write-Host "2. Start Kafka: cd kafka && .\start_kafka_docker.ps1" -ForegroundColor White
Write-Host "3. Create Kafka topic at: http://localhost:9000" -ForegroundColor White
Write-Host "4. Start Logstash with the pipeline configuration" -ForegroundColor White
Write-Host "5. Start weather producer: cd kafka && python weather_kfk_producer.py" -ForegroundColor White
Write-Host "6. Access Kibana at: http://localhost:5601" -ForegroundColor White
Write-Host ""
Write-Host "See SETUP_GUIDE.md for detailed instructions!" -ForegroundColor Yellow
