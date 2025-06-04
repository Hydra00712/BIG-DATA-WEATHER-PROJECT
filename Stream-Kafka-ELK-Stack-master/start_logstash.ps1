# Start Logstash using Docker
Write-Host "Starting Logstash..." -ForegroundColor Green

# Create a bridge network to connect all containers
docker network create weather-pipeline 2>$null

# Start Logstash container
docker run -d `
  --name logstash `
  --network weather-pipeline `
  --network elk_default `
  --network kafka_default `
  -v "${PWD}/elk/logstash/pipeline.conf:/usr/share/logstash/pipeline/logstash.conf:ro" `
  -e "LS_JAVA_OPTS=-Xmx256m -Xms256m" `
  docker.elastic.co/logstash/logstash:7.10.2

Write-Host "Logstash started! Check logs with: docker logs logstash" -ForegroundColor Green
