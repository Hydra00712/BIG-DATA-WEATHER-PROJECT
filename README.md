
@"
# 🌤️ Real-Time Weather Monitoring Dashboard

A production-grade real-time data pipeline for weather monitoring using Apache Kafka, Elasticsearch, and modern web technologies.

## 🎯 Project Overview

This project demonstrates a complete enterprise-grade real-time data pipeline that:
- 🌍 Monitors weather from 6 European cities in real-time
- 🚚 Streams data reliably using Apache Kafka
- 🔍 Stores data efficiently in Elasticsearch
- 📊 Visualizes beautifully with dual dashboards (Kibana + Custom HTML)
- 🐳 Deploys easily with Docker containers

## 🚀 Quick Start

1. Clone the repository
2. Set up your OpenWeather API key in \`kafka/weather_api_key.ini\`
3. Run \`python start_project.py\` to start all services
4. Start data collection with \`python working_weather_producer.py\`

## 📊 Access Points

- Kibana Dashboard: http://localhost:5601
- Elasticsearch: http://localhost:9200
- HTML Dashboard: weather_dashboard.html

## 📄 Documentation

See the full documentation in [PROJECT_REPORT.md](PROJECT_REPORT.md)
"@ | Out-File -FilePath "README.md" -Encoding utf8
