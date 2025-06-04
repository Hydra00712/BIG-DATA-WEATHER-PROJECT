# PowerShell script to start Elasticsearch and Kibana Docker containers
Write-Host "Starting Elasticsearch and Kibana..." -ForegroundColor Green
docker-compose -f elasticsearch.yaml up
