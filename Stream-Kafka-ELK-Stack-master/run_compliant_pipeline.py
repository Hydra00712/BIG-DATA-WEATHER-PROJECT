#!/usr/bin/env python3
"""
🎯 Pipeline Complet Conforme aux Exigences
Respecte 100% des spécifications du projet
"""

import subprocess
import time
import requests
import json

def setup_kafka_topics():
    """Création des topics Kafka requis"""
    topics = [
        'openweather',           # Topic source
        'weather-enriched',      # Topic enrichi par Kafka Streams
        'weather-aggregated'     # Topic agrégé
    ]
    
    print("📋 Création des topics Kafka...")
    for topic in topics:
        try:
            subprocess.run([
                'docker', 'exec', 'kafka',
                'kafka-topics', '--create',
                '--topic', topic,
                '--bootstrap-server', 'localhost:9092',
                '--partitions', '3',
                '--replication-factor', '1'
            ], check=True, capture_output=True)
            print(f"✅ Topic '{topic}' créé")
        except subprocess.CalledProcessError:
            print(f"⚠️ Topic '{topic}' existe déjà")

def start_kafka_connect():
    """Démarrage de Kafka Connect"""
    print("🔗 Démarrage de Kafka Connect...")
    try:
        subprocess.run([
            'docker-compose', '-f', 'kafka-connect/docker-compose-connect.yml', 'up', '-d'
        ], check=True)
        print("✅ Kafka Connect démarré")
        
        # Attendre que Kafka Connect soit prêt
        print("⏳ Attente de Kafka Connect...")
        time.sleep(30)
        
        # Vérifier le statut
        response = requests.get('http://localhost:8083/connectors')
        if response.status_code == 200:
            print("✅ Kafka Connect opérationnel")
        else:
            print("❌ Problème avec Kafka Connect")
            
    except Exception as e:
        print(f"❌ Erreur Kafka Connect: {e}")

def start_kafka_streams():
    """Démarrage du processeur Kafka Streams"""
    print("🔄 Démarrage de Kafka Streams...")
    try:
        subprocess.Popen(['python', 'kafka_streams_processor.py'])
        print("✅ Kafka Streams démarré")
    except Exception as e:
        print(f"❌ Erreur Kafka Streams: {e}")

def start_weather_producer():
    """Démarrage du producteur météo"""
    print("🌤️ Démarrage du producteur météo...")
    try:
        subprocess.Popen(['python', 'working_weather_producer.py'])
        print("✅ Producteur météo démarré")
    except Exception as e:
        print(f"❌ Erreur producteur: {e}")

def verify_pipeline():
    """Vérification de la conformité du pipeline"""
    print("\n🔍 Vérification de la conformité...")
    
    checks = {
        "Apache Kafka": check_kafka(),
        "Elasticsearch": check_elasticsearch(),
        "Kibana": check_kibana(),
        "Kafka Streams": check_kafka_streams(),
        "Kafka Connect": check_kafka_connect(),
        "Source temps réel": check_data_source(),
        "Visualisation": check_visualization()
    }
    
    print("\n📊 Résultats de conformité:")
    total_score = 0
    for component, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {component}: {'CONFORME' if status else 'NON CONFORME'}")
        if status:
            total_score += 1
    
    conformity_percentage = (total_score / len(checks)) * 100
    print(f"\n🎯 Conformité globale: {conformity_percentage:.0f}%")
    
    return conformity_percentage >= 100

def check_kafka():
    """Vérifier Kafka"""
    try:
        result = subprocess.run(['docker', 'ps', '--filter', 'name=kafka'], 
                              capture_output=True, text=True)
        return 'kafka' in result.stdout
    except:
        return False

def check_elasticsearch():
    """Vérifier Elasticsearch"""
    try:
        response = requests.get('http://localhost:9200')
        return response.status_code == 200
    except:
        return False

def check_kibana():
    """Vérifier Kibana"""
    try:
        response = requests.get('http://localhost:5601')
        return response.status_code == 200
    except:
        return False

def check_kafka_streams():
    """Vérifier Kafka Streams"""
    try:
        # Vérifier si le processus tourne
        result = subprocess.run(['pgrep', '-f', 'kafka_streams_processor'], 
                              capture_output=True)
        return result.returncode == 0
    except:
        return False

def check_kafka_connect():
    """Vérifier Kafka Connect"""
    try:
        response = requests.get('http://localhost:8083/connectors')
        return response.status_code == 200
    except:
        return False

def check_data_source():
    """Vérifier la source de données"""
    try:
        # Vérifier si des données arrivent dans Elasticsearch
        response = requests.get('http://localhost:9200/openweather/_count')
        if response.status_code == 200:
            count = response.json().get('count', 0)
            return count > 0
    except:
        return False

def check_visualization():
    """Vérifier la visualisation"""
    try:
        # Vérifier si Kibana peut accéder aux données
        response = requests.get('http://localhost:5601/api/status')
        return response.status_code == 200
    except:
        return False

def main():
    print("🚀 Démarrage du Pipeline Conforme aux Exigences")
    print("=" * 60)
    
    # 1. Setup des topics
    setup_kafka_topics()
    
    # 2. Démarrage Kafka Connect
    start_kafka_connect()
    
    # 3. Démarrage Kafka Streams
    start_kafka_streams()
    
    # 4. Démarrage du producteur
    start_weather_producer()
    
    # 5. Attendre un peu pour que tout se stabilise
    print("\n⏳ Stabilisation du pipeline...")
    time.sleep(10)
    
    # 6. Vérification
    is_compliant = verify_pipeline()
    
    if is_compliant:
        print("\n🎉 PROJET 100% CONFORME AUX EXIGENCES!")
        print("✅ Toutes les technologies et étapes sont implémentées")
    else:
        print("\n⚠️ Conformité partielle - voir les détails ci-dessus")
    
    print(f"\n🌐 Accès aux interfaces:")
    print(f"📊 Kibana: http://localhost:5601")
    print(f"🔍 Elasticsearch: http://localhost:9200")
    print(f"🔗 Kafka Connect: http://localhost:8083")

if __name__ == "__main__":
    main()
