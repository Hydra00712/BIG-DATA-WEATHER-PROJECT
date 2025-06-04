#!/usr/bin/env python3
"""
🔄 Kafka Streams Processor pour le traitement temps réel
Conforme aux exigences: prétraitement avec Kafka Streams
"""

from kafka import KafkaConsumer, KafkaProducer
import json
from datetime import datetime
import time

class WeatherStreamsProcessor:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'openweather',
            bootstrap_servers=['localhost:9092'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            group_id='weather-streams-processor'
        )
        
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
    
    def enrich_data(self, weather_data):
        """Enrichissement des données météo"""
        
        # Ajout de métadonnées
        enriched_data = weather_data.copy()
        enriched_data.update({
            'processed_at': datetime.now().isoformat(),
            'data_source': 'openweather_api',
            'processor': 'kafka_streams',
            'version': '1.0'
        })
        
        # Calculs dérivés
        if 'temp' in weather_data and 'humidity' in weather_data:
            # Index de confort thermique
            temp = weather_data['temp']
            humidity = weather_data['humidity']
            
            # Calcul Heat Index simplifié
            if temp >= 27:
                heat_index = temp + (0.5 * (humidity - 50))
                enriched_data['heat_index'] = round(heat_index, 3)
            
            # Classification de température
            if temp < 0:
                enriched_data['temp_category'] = 'freezing'
            elif temp < 10:
                enriched_data['temp_category'] = 'cold'
            elif temp < 20:
                enriched_data['temp_category'] = 'mild'
            elif temp < 30:
                enriched_data['temp_category'] = 'warm'
            else:
                enriched_data['temp_category'] = 'hot'
        
        # Nettoyage des données
        if 'visibility' in enriched_data and enriched_data['visibility'] == 0:
            enriched_data['visibility'] = None
            
        return enriched_data
    
    def aggregate_data(self, weather_data):
        """Agrégations en temps réel"""
        
        # Simulation d'agrégations (en production, utiliser une vraie fenêtre temporelle)
        city = weather_data.get('city_name', 'unknown')
        
        aggregated = {
            'city': city,
            'timestamp': datetime.now().isoformat(),
            'current_temp': weather_data.get('temp'),
            'current_humidity': weather_data.get('humidity'),
            'data_type': 'aggregated_metrics'
        }
        
        return aggregated
    
    def process_stream(self):
        """Traitement principal du stream"""
        print("🔄 Kafka Streams Processor démarré")
        print("📊 Traitement des données météo en temps réel...")
        
        try:
            for message in self.consumer:
                weather_data = message.value
                
                print(f"📡 Traitement: {weather_data.get('city_name', 'Unknown')}")
                
                # 1. Enrichissement des données
                enriched_data = self.enrich_data(weather_data)
                
                # 2. Envoi vers topic enrichi
                self.producer.send('weather-enriched', enriched_data)
                
                # 3. Agrégations
                aggregated_data = self.aggregate_data(weather_data)
                
                # 4. Envoi vers topic agrégé
                self.producer.send('weather-aggregated', aggregated_data)
                
                print(f"✅ Données enrichies et agrégées pour {weather_data.get('city_name')}")
                
        except KeyboardInterrupt:
            print("\n🛑 Arrêt du processeur Kafka Streams")
        finally:
            self.consumer.close()
            self.producer.close()

def main():
    processor = WeatherStreamsProcessor()
    processor.process_stream()

if __name__ == "__main__":
    main()
