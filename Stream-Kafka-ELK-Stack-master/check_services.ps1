# Service Health Check Script
Write-Host "=== Checking Service Status ===" -ForegroundColor Cyan
Write-Host ""

# Function to check if a service is responding
function Test-ServiceHealth($url, $serviceName) {
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Host "✓ $serviceName is running at $url" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "✗ $serviceName is not responding at $url" -ForegroundColor Red
        return $false
    }
    return $false
}

# Check Docker containers
Write-Host "Docker Containers:" -ForegroundColor Yellow
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
Write-Host ""

# Check individual services
Write-Host "Service Health Checks:" -ForegroundColor Yellow
$elasticsearch = Test-ServiceHealth "http://localhost:9200" "Elasticsearch"
$kibana = Test-ServiceHealth "http://localhost:5601" "Kibana"
$kafkaManager = Test-ServiceHealth "http://localhost:9000" "Kafka Manager"

Write-Host ""
if ($elasticsearch -and $kibana -and $kafkaManager) {
    Write-Host "🎉 All services are running!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Create Kafka topic at: http://localhost:9000" -ForegroundColor White
    Write-Host "2. Test API: python test_api.py" -ForegroundColor White
    Write-Host "3. Start producer: cd kafka && python weather_kfk_producer.py" -ForegroundColor White
    Write-Host "4. View data in Kibana: http://localhost:5601" -ForegroundColor White
} else {
    Write-Host "⚠️  Some services are not ready yet. Please wait and try again." -ForegroundColor Yellow
    Write-Host "Services may take a few minutes to start up completely." -ForegroundColor Gray
}
