#!/usr/bin/env python3
"""
🎯 Automatic Weather Dashboard Creator
Creates the complete weather dashboard automatically using Kibana API
"""

import requests
import json
import time
from datetime import datetime

# Configuration
KIBANA_URL = "http://localhost:5601"
ELASTICSEARCH_URL = "http://localhost:9200"
INDEX_PATTERN = "openweather*"
CITIES = ["Krakow", "Paris", "Berlin", "Amsterdam", "Barcelona", "Vienna"]

def create_index_pattern():
    """Create index pattern without time field"""
    headers = {
        'Content-Type': 'application/json',
        'kbn-xsrf': 'true'
    }
    
    payload = {
        "attributes": {
            "title": "openweather*"
        }
    }
    
    url = f"{KIBANA_URL}/api/saved_objects/index-pattern/openweather-pattern"
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code in [200, 201]:
        print("✅ Index pattern created")
        return "openweather-pattern"
    else:
        print(f"⚠️ Index pattern might already exist: {response.status_code}")
        return "openweather-pattern"

def create_temperature_metric(city):
    """Create temperature metric visualization for a city"""
    headers = {
        'Content-Type': 'application/json',
        'kbn-xsrf': 'true'
    }
    
    vis_state = {
        "title": f"Temperature - {city}",
        "type": "metric",
        "params": {
            "metric": {
                "percentageMode": False,
                "useRanges": False,
                "colorSchema": "Green to Red",
                "metricColorMode": "None",
                "colorsRange": [{"from": 0, "to": 50}],
                "labels": {"show": True},
                "invertColors": False,
                "style": {
                    "bgFill": "#000",
                    "bgColor": False,
                    "labelColor": False,
                    "subText": "",
                    "fontSize": 60
                }
            }
        },
        "aggs": [
            {
                "id": "1",
                "enabled": True,
                "type": "top_hits",
                "schema": "metric",
                "params": {
                    "field": "temp",
                    "aggregate": "concat",
                    "size": 1,
                    "sortField": "timestamp",
                    "sortOrder": "desc"
                }
            }
        ]
    }
    
    payload = {
        "attributes": {
            "title": f"Temperature - {city}",
            "visState": json.dumps(vis_state),
            "uiStateJSON": "{}",
            "description": "",
            "version": 1,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps({
                    "index": "openweather-pattern",
                    "filter": [
                        {
                            "meta": {
                                "alias": None,
                                "disabled": False,
                                "key": "city_name.keyword",
                                "negate": False,
                                "params": {"query": city},
                                "type": "phrase"
                            },
                            "query": {"match_phrase": {"city_name.keyword": city}}
                        }
                    ],
                    "query": {"query": "", "language": "kuery"}
                })
            }
        }
    }
    
    url = f"{KIBANA_URL}/api/saved_objects/visualization/temp-{city.lower()}"
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code in [200, 201]:
        print(f"✅ Temperature metric created for {city}")
        return f"temp-{city.lower()}"
    else:
        print(f"❌ Failed to create temperature metric for {city}: {response.status_code}")
        return None

def create_humidity_metric(city):
    """Create humidity metric visualization for a city"""
    headers = {
        'Content-Type': 'application/json',
        'kbn-xsrf': 'true'
    }
    
    vis_state = {
        "title": f"Humidity - {city}",
        "type": "metric",
        "params": {
            "metric": {
                "percentageMode": False,
                "useRanges": False,
                "colorSchema": "Green to Red",
                "metricColorMode": "None",
                "colorsRange": [{"from": 0, "to": 100}],
                "labels": {"show": True},
                "invertColors": False,
                "style": {
                    "bgFill": "#000",
                    "bgColor": False,
                    "labelColor": False,
                    "subText": "",
                    "fontSize": 60
                }
            }
        },
        "aggs": [
            {
                "id": "1",
                "enabled": True,
                "type": "top_hits",
                "schema": "metric",
                "params": {
                    "field": "humidity",
                    "aggregate": "concat",
                    "size": 1,
                    "sortField": "timestamp",
                    "sortOrder": "desc"
                }
            }
        ]
    }
    
    payload = {
        "attributes": {
            "title": f"Humidity - {city}",
            "visState": json.dumps(vis_state),
            "uiStateJSON": "{}",
            "description": "",
            "version": 1,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps({
                    "index": "openweather-pattern",
                    "filter": [
                        {
                            "meta": {
                                "alias": None,
                                "disabled": False,
                                "key": "city_name.keyword",
                                "negate": False,
                                "params": {"query": city},
                                "type": "phrase"
                            },
                            "query": {"match_phrase": {"city_name.keyword": city}}
                        }
                    ],
                    "query": {"query": "", "language": "kuery"}
                })
            }
        }
    }
    
    url = f"{KIBANA_URL}/api/saved_objects/visualization/humidity-{city.lower()}"
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code in [200, 201]:
        print(f"✅ Humidity metric created for {city}")
        return f"humidity-{city.lower()}"
    else:
        print(f"❌ Failed to create humidity metric for {city}: {response.status_code}")
        return None

def create_temperature_line(city):
    """Create temperature line chart for a city"""
    headers = {
        'Content-Type': 'application/json',
        'kbn-xsrf': 'true'
    }
    
    vis_state = {
        "title": f"Temperature Trend - {city}",
        "type": "line",
        "params": {
            "grid": {"categoryLines": False, "style": {"color": "#eee"}},
            "categoryAxes": [
                {
                    "id": "CategoryAxis-1",
                    "type": "category",
                    "position": "bottom",
                    "show": True,
                    "style": {},
                    "scale": {"type": "linear"},
                    "labels": {"show": True, "truncate": 100},
                    "title": {}
                }
            ],
            "valueAxes": [
                {
                    "id": "ValueAxis-1",
                    "name": "LeftAxis-1",
                    "type": "value",
                    "position": "left",
                    "show": True,
                    "style": {},
                    "scale": {"type": "linear", "mode": "normal"},
                    "labels": {"show": True, "rotate": 0, "filter": False, "truncate": 100},
                    "title": {"text": "Temperature"}
                }
            ],
            "seriesParams": [
                {
                    "show": "true",
                    "type": "line",
                    "mode": "normal",
                    "data": {"label": "Average temp", "id": "1"},
                    "valueAxis": "ValueAxis-1",
                    "drawLinesBetweenPoints": True,
                    "showCircles": True
                }
            ],
            "addTooltip": True,
            "addLegend": True,
            "legendPosition": "right",
            "times": [],
            "addTimeMarker": False
        },
        "aggs": [
            {
                "id": "1",
                "enabled": True,
                "type": "avg",
                "schema": "metric",
                "params": {"field": "temp"}
            },
            {
                "id": "2",
                "enabled": True,
                "type": "terms",
                "schema": "segment",
                "params": {
                    "field": "timestamp",
                    "size": 20,
                    "order": "asc",
                    "orderBy": "_key"
                }
            }
        ]
    }
    
    payload = {
        "attributes": {
            "title": f"Temperature Trend - {city}",
            "visState": json.dumps(vis_state),
            "uiStateJSON": "{}",
            "description": "",
            "version": 1,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps({
                    "index": "openweather-pattern",
                    "filter": [
                        {
                            "meta": {
                                "alias": None,
                                "disabled": False,
                                "key": "city_name.keyword",
                                "negate": False,
                                "params": {"query": city},
                                "type": "phrase"
                            },
                            "query": {"match_phrase": {"city_name.keyword": city}}
                        }
                    ],
                    "query": {"query": "", "language": "kuery"}
                })
            }
        }
    }
    
    url = f"{KIBANA_URL}/api/saved_objects/visualization/temp-line-{city.lower()}"
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code in [200, 201]:
        print(f"✅ Temperature line chart created for {city}")
        return f"temp-line-{city.lower()}"
    else:
        print(f"❌ Failed to create temperature line for {city}: {response.status_code}")
        return None

def main():
    print("🎯 Automatic Weather Dashboard Creator")
    print("=" * 50)
    
    # Step 1: Create index pattern
    print("\n📋 Step 1: Creating index pattern...")
    index_pattern_id = create_index_pattern()
    
    # Step 2: Create visualizations
    print(f"\n📊 Step 2: Creating visualizations for {len(CITIES)} cities...")
    
    created_visualizations = []
    
    for city in CITIES:
        print(f"\n🏙️ Creating visualizations for {city}...")
        
        # Create temperature metric
        temp_metric_id = create_temperature_metric(city)
        if temp_metric_id:
            created_visualizations.append(temp_metric_id)
        
        # Create humidity metric
        humidity_metric_id = create_humidity_metric(city)
        if humidity_metric_id:
            created_visualizations.append(humidity_metric_id)
        
        # Create temperature line chart
        temp_line_id = create_temperature_line(city)
        if temp_line_id:
            created_visualizations.append(temp_line_id)
    
    print(f"\n✅ Created {len(created_visualizations)} visualizations!")
    
    print("\n🎉 Dashboard creation complete!")
    print(f"🌐 Go to Kibana: {KIBANA_URL}")
    print("📊 Create a new dashboard and add your visualizations!")
    
    print(f"\n📋 Created visualizations:")
    for viz_id in created_visualizations:
        print(f"  - {viz_id}")

if __name__ == "__main__":
    main()
