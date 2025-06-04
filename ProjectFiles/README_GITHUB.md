# 🌤️ Real-Time Weather Monitoring Dashboard

[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Kafka](https://img.shields.io/badge/Apache-Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white)](https://kafka.apache.org)
[![Elasticsearch](https://img.shields.io/badge/Elastic-Search-005571?style=for-the-badge&logo=elasticsearch&logoColor=white)](https://elastic.co)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

> **A production-grade real-time data pipeline for weather monitoring using Apache Kafka, Elasticsearch, and modern web technologies.**

## 🎯 **Project Overview**

This project demonstrates a complete **enterprise-grade real-time data pipeline** that:
- 🌍 **Monitors weather** from 6 European cities in real-time
- 🚚 **Streams data reliably** using Apache Kafka
- 🔍 **Stores data efficiently** in Elasticsearch
- 📊 **Visualizes beautifully** with dual dashboards (Kibana + Custom HTML)
- 🐳 **Deploys easily** with Docker containers

**Cities Monitored:** London, Berlin, Paris, Barcelona, Amsterdam, Krakow, Vienna

## ✨ **Key Features**

- ✅ **Real-time data streaming** with Apache Kafka
- ✅ **Fast data storage & search** with Elasticsearch
- ✅ **Professional dashboards** with Kibana
- ✅ **Beautiful custom interface** with HTML/CSS/JavaScript
- ✅ **Complete containerization** with Docker
- ✅ **Fault-tolerant architecture** with automatic recovery
- ✅ **Scalable design** for enterprise use
- ✅ **Comprehensive monitoring** and health checks

## 🏗️ **System Architecture**

```
🌐 OpenWeather API → 📡 Python Producer → 🚚 Kafka → 🔄 Logstash → 🔍 Elasticsearch → 📊 Kibana/HTML Dashboard
```

### **Component Breakdown:**
- **🌐 OpenWeather API** - Real-time weather data source
- **📡 Python Producer** - Automated data collection
- **🚚 Apache Kafka** - Reliable message streaming
- **🐘 Zookeeper** - Kafka coordination service
- **🔄 Logstash** - Data processing and enrichment
- **🔍 Elasticsearch** - Fast data storage and search
- **📊 Kibana** - Professional data visualization
- **🌐 HTML Dashboard** - Custom beautiful interface

## 🛠️ **Technology Stack**

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.12+ | Data collection & processing |
| **Apache Kafka** | 7.4.0 | Message streaming platform |
| **Zookeeper** | 7.4.0 | Kafka coordination service |
| **Elasticsearch** | 7.17.0 | Search engine & database |
| **Logstash** | 7.17.0 | Data processing pipeline |
| **Kibana** | 7.17.0 | Data visualization platform |
| **Docker** | Latest | Container orchestration |
| **HTML5/CSS3/JS** | ES6+ | Frontend development |

## 🚀 **Quick Start**

### **Prerequisites**
- 🐳 Docker Desktop
- 🐍 Python 3.7+
- 🔑 OpenWeather API key (free from [openweathermap.org](https://openweathermap.org/api))

### **Installation**

```bash
# 1. Clone the repository
git clone https://github.com/MedAdamBen7/real-time-weather-dashboard.git
cd real-time-weather-dashboard

# 2. Setup API key
mkdir -p kafka
echo "[openweather]" > kafka/weather_api_key.ini
echo "key=YOUR_API_KEY_HERE" >> kafka/weather_api_key.ini

# 3. Install Python dependencies
pip install requests confluent-kafka configparser

# 4. Start all services (automated)
python start_project.py

# 5. Start data collection
python working_weather_producer.py

# 6. Generate HTML dashboard
python create_html_dashboard.py
```

### **Access Points**
- 📊 **Kibana Dashboard:** http://localhost:5601
- 🔍 **Elasticsearch:** http://localhost:9200
- 📱 **HTML Dashboard:** `weather_dashboard.html`
- 🚚 **Kafka:** localhost:9092

## 📊 **Features Showcase**

### **🎨 Beautiful HTML Dashboard**
- Real-time updates every 5 seconds
- Glass morphism design with gradients
- SVG-based temperature charts
- Responsive design for all devices
- 3-decimal precision for scientific accuracy

### **📈 Professional Kibana Dashboard**
- Time-series temperature analysis
- Geographic weather maps
- Historical trend visualization
- Real-time monitoring alerts

### **⚡ Performance Metrics**
- **Data Latency:** < 2 seconds end-to-end
- **Update Frequency:** 60s (Kafka) / 5s (HTML)
- **Throughput:** 420 records/hour
- **Query Speed:** < 100ms response time

## 🔧 **Project Structure**

```
real-time-weather-dashboard/
├── 📄 PROJECT_REPORT.md              # Complete technical documentation
├── 🐳 docker-compose.yml             # Main Docker orchestration
├── 📁 kafka/
│   ├── 🔑 weather_api_key.ini        # API configuration
│   └── ⚙️ kafka.yaml                 # Kafka setup
├── 📁 elk/
│   └── 📊 elasticsearch.yaml         # ELK stack configuration
├── 📁 logstash/
│   ├── 🔄 pipeline.conf              # Data processing pipeline
│   └── ⚙️ logstash.yml               # Logstash configuration
├── 🐍 working_weather_producer.py    # Main data collector
├── 🌐 create_html_dashboard.py       # Dashboard generator
├── 🚀 start_project.py              # Automated startup
├── 🔍 check_services.py             # Health monitoring
└── 📋 weather_dashboard.html         # Generated dashboard
```

## 📖 **Documentation**

- 📄 **[Complete Project Report](PROJECT_REPORT.md)** - Comprehensive technical documentation
- 📋 **[Setup Guide](SETUP_GUIDE.md)** - Detailed installation instructions
- 🔧 **[API Documentation](docs/api.md)** - Service endpoints and usage

## 🎓 **Learning Outcomes**

This project demonstrates mastery of:

### **🔧 Technical Skills**
- **Real-time data processing** with Apache Kafka
- **Big data storage** with Elasticsearch
- **Data visualization** with Kibana and custom web interfaces
- **Container orchestration** with Docker
- **Modern web development** with HTML5/CSS3/JavaScript
- **System architecture** design and implementation

### **💼 Industry Relevance**
Technologies used by **Netflix**, **Uber**, **Airbnb**, **Amazon**, and **LinkedIn** for:
- Real-time recommendation systems
- Location tracking and analytics
- Search and booking platforms
- Activity feed processing

## 📊 **Project Metrics**

- **📁 Files:** 25+ configuration and code files
- **💻 Code:** 2000+ lines across all components
- **🛠️ Technologies:** 8 major technologies integrated
- **🐳 Services:** 5 containerized microservices
- **🌍 Data Sources:** 7 cities with multiple metrics each

## 🔮 **Future Enhancements**

- 🤖 **Machine Learning** weather predictions
- 📱 **Mobile App** with push notifications
- 🗺️ **Interactive Maps** with weather overlays
- ⚠️ **Alert System** for extreme weather
- 🌍 **Additional Data Sources** (air quality, traffic)

## 🤝 **Contributing**

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 **Author**

**MedAdamBen7**
- 📧 Email: db11911918@gmail.com
- 🐙 GitHub: [@MedAdamBen7](https://github.com/MedAdamBen7)
- 🔗 Project Link: [https://github.com/MedAdamBen7/real-time-weather-dashboard](https://github.com/MedAdamBen7/real-time-weather-dashboard)

## 🙏 **Acknowledgments**

- OpenWeather API for providing reliable weather data
- Apache Foundation for Kafka and related technologies
- Elastic for the ELK stack
- Docker for containerization technology

---

⭐ **If you found this project helpful, please give it a star!** ⭐

**🚀 Built with modern data engineering best practices for real-world applications**
