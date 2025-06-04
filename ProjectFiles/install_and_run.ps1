# Complete Installation and Setup Script for Kafka + ELK Weather Pipeline
# This script automates the entire setup process

param(
    [string]$ApiKey = "",
    [switch]$SkipDockerPull = $false
)

Write-Host "=== Kafka + ELK Weather Pipeline Installer ===" -ForegroundColor Cyan
Write-Host ""

# Function to check if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Function to wait for service to be ready
function Wait-ForService($url, $serviceName, $maxWaitSeconds = 120) {
    Write-Host "Waiting for $serviceName to be ready at $url..." -ForegroundColor Yellow
    $elapsed = 0
    while ($elapsed -lt $maxWaitSeconds) {
        try {
            $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-Host "✓ $serviceName is ready!" -ForegroundColor Green
                return $true
            }
        } catch {
            # Service not ready yet
        }
        Start-Sleep -Seconds 5
        $elapsed += 5
        Write-Host "  Still waiting... ($elapsed/$maxWaitSeconds seconds)" -ForegroundColor Gray
    }
    Write-Host "✗ $serviceName failed to start within $maxWaitSeconds seconds" -ForegroundColor Red
    return $false
}

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

if (-not (Test-Command "docker")) {
    Write-Host "✗ Docker not found. Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "  Download from: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Docker found" -ForegroundColor Green

if (-not (Test-Command "python")) {
    Write-Host "✗ Python not found. Please install Python 3.7+ first." -ForegroundColor Red
    Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Python found" -ForegroundColor Green

# Get API key if not provided
if ([string]::IsNullOrEmpty($ApiKey)) {
    Write-Host ""
    Write-Host "You need an OpenWeather API key to continue." -ForegroundColor Yellow
    Write-Host "Get one free at: https://openweathermap.org/api" -ForegroundColor Cyan
    $ApiKey = Read-Host "Enter your OpenWeather API key"
    
    if ([string]::IsNullOrEmpty($ApiKey)) {
        Write-Host "✗ API key is required to continue." -ForegroundColor Red
        exit 1
    }
}

# Create API key file
Write-Host "Configuring API key..." -ForegroundColor Yellow
$apiKeyContent = "[openweather]`nkey:$ApiKey"
$apiKeyContent | Out-File -FilePath "kafka/weather_api_key.ini" -Encoding UTF8
Write-Host "✓ API key configured" -ForegroundColor Green

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt | Out-Null
    Write-Host "✓ Python dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to install Python dependencies" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Starting Infrastructure ===" -ForegroundColor Cyan

# Start Elasticsearch and Kibana
Write-Host "Starting Elasticsearch and Kibana..." -ForegroundColor Yellow
Set-Location "elk"
if (-not $SkipDockerPull) {
    docker-compose -f elasticsearch.yaml up -d
} else {
    docker-compose -f elasticsearch.yaml up -d --no-deps
}
Set-Location ".."

# Start Kafka
Write-Host "Starting Kafka and Zookeeper..." -ForegroundColor Yellow
Set-Location "kafka"
if (-not $SkipDockerPull) {
    docker-compose -f kafka.yaml up -d
} else {
    docker-compose -f kafka.yaml up -d --no-deps
}
Set-Location ".."

Write-Host ""
Write-Host "=== Waiting for Services ===" -ForegroundColor Cyan

# Wait for services to be ready
$elasticsearchReady = Wait-ForService "http://localhost:9200" "Elasticsearch" 180
$kibanaReady = Wait-ForService "http://localhost:5601" "Kibana" 180
$kafkaManagerReady = Wait-ForService "http://localhost:9000" "Kafka Manager" 120

if (-not ($elasticsearchReady -and $kibanaReady -and $kafkaManagerReady)) {
    Write-Host ""
    Write-Host "Some services failed to start. Please check Docker logs:" -ForegroundColor Red
    Write-Host "  docker-compose -f elk/elasticsearch.yaml logs" -ForegroundColor Yellow
    Write-Host "  docker-compose -f kafka/kafka.yaml logs" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Create Kafka topic:" -ForegroundColor White
Write-Host "   - Open: http://localhost:9000" -ForegroundColor Yellow
Write-Host "   - Add cluster: name='local-kafka', zookeeper='zookeeper:2181'" -ForegroundColor Yellow
Write-Host "   - Create topic: name='openweather', partitions=1, replication=1" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Start the weather producer:" -ForegroundColor White
Write-Host "   cd kafka && python weather_kfk_producer.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Access Kibana dashboard:" -ForegroundColor White
Write-Host "   http://localhost:5601" -ForegroundColor Yellow
Write-Host ""
Write-Host "Services running:" -ForegroundColor Cyan
Write-Host "  - Elasticsearch: http://localhost:9200" -ForegroundColor White
Write-Host "  - Kibana: http://localhost:5601" -ForegroundColor White
Write-Host "  - Kafka Manager: http://localhost:9000" -ForegroundColor White
Write-Host "  - Kafka: localhost:9092" -ForegroundColor White
