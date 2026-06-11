"""
Utility functions for CoolBlock AI
"""

import requests
import json
from datetime import datetime
import math

COOLING_CENTERS = {
    "new_york": [
        {
            "name": "NY Public Library - Main Branch",
            "address": "476 5th Ave, New York, NY 10018",
            "lat": 40.7532,
            "lon": -73.9822,
            "type": "library",
            "hours": "Mon-Thu: 10am-6pm, Fri-Sat: 10am-5pm, Sun: 1pm-5pm",
            "phone": "(917) 275-6975",
            "ac": True
        },
        {
            "name": "NYC Community Center - Midtown",
            "address": "301 Park Ave S, New York, NY 10010",
            "lat": 40.7432,
            "lon": -73.9864,
            "type": "community_center",
            "hours": "Daily: 6am-10pm",
            "phone": "(212) 555-0147",
            "ac": True
        },
        {
            "name": "Mount Sinai Hospital - ER",
            "address": "1 Gustave L. Levy Pl, New York, NY 10029",
            "lat": 40.7831,
            "lon": -73.9712,
            "type": "hospital",
            "hours": "24/7",
            "phone": "911",
            "ac": True
        },
        {
            "name": "Central Park Water Fountains",
            "address": "Central Park, New York, NY",
            "lat": 40.7829,
            "lon": -73.9654,
            "type": "park",
            "hours": "6am-1am",
            "phone": "N/A",
            "ac": False
        },
        {
            "name": "Whole Foods Market - AC",
            "address": "10 Columbus Circle, New York, NY 10019",
            "lat": 40.7680,
            "lon": -73.9776,
            "type": "retail",
            "hours": "Daily: 8am-10pm",
            "phone": "(212) 823-9060",
            "ac": True
        }
    ]
}


def get_weather_data(latitude, longitude):
    """
    Fetch weather data from Open-Meteo API
    
    Args:
        latitude: Location latitude
        longitude: Location longitude
    
    Returns:
        dict: Weather data including temperature, humidity, etc.
    """
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature",
                "temperature_unit": "fahrenheit",
                "timezone": "auto"
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "temperature": data["current"]["temperature_2m"],
                "humidity": data["current"]["relative_humidity_2m"],
                "apparent_temperature": data["current"]["apparent_temperature"],
                "timestamp": data["current"]["time"]
            }
    except:
        pass
    
    # Return mock data if API fails
    return {
        "success": False,
        "temperature": 85.0,
        "humidity": 65,
        "apparent_temperature": 92.0,
        "timestamp": datetime.now().isoformat()
    }


def get_cooling_centers_for_location(latitude, longitude, radius_miles=1.0):
    """
    Get cooling centers near a location
    """
    if 40 <= latitude <= 41 and -75 <= longitude <= -73:
        centers = COOLING_CENTERS.get("new_york", [])
    else:
        centers = []
    
    centers_with_distance = []
    for center in centers:
        distance = calculate_distance(latitude, longitude, center["lat"], center["lon"])
        
        if distance <= radius_miles:
            centers_with_distance.append({
                **center,
                "distance_miles": round(distance, 2)
            })
    
    centers_with_distance.sort(key=lambda x: x["distance_miles"])
    return centers_with_distance


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using Haversine formula
    """
    R = 3959  # Earth's radius in miles
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def calculate_heat_index(temperature_f, humidity):
    """
    Calculate heat index (feels-like temperature)
    """
    if temperature_f < 68:
        return temperature_f
    
    c1 = -42.379
    c2 = 2.04901523
    c3 = 10.14333127
    c4 = -0.22475541
    c5 = -0.00683783
    c6 = -0.05481717
    c7 = 0.00122874
    c8 = 0.00085282
    c9 = -0.00000199
    
    T = temperature_f
    RH = humidity
    
    HI = (c1 + c2*T + c3*RH + c4*T*RH + c5*T**2 + c6*RH**2 +
          c7*T**2*RH + c8*T*RH**2 + c9*T**2*RH**2)
    
    return round(HI, 1)


def categorize_heat_risk(temperature_f, humidity):
    """
    Categorize heat risk level
    """
    heat_index = calculate_heat_index(temperature_f, humidity)
    
    if temperature_f >= 103 or heat_index >= 125:
        risk = "EXTREME"
        color = "#8B0000"
        recommendations = [
            "🚨 STAY INDOORS - Seek air conditioning immediately",
            "🚑 Be alert for signs of heat illness",
            "💧 Drink water constantly",
            "☎️ Call 911 if experiencing severe symptoms"
        ]
    elif temperature_f >= 95 or heat_index >= 103:
        risk = "HIGH"
        color = "#FF0000"
        recommendations = [
            "⚠️ Stay in air conditioning as much as possible",
            "💧 Drink plenty of water throughout the day",
            "🏃 Reduce strenuous outdoor activities",
            "👴 Check on elderly neighbors"
        ]
    elif temperature_f >= 85 or heat_index >= 90:
        risk = "MODERATE"
        color = "#FFA500"
        recommendations = [
            "⚡ Be cautious during peak heat hours",
            "💧 Drink water regularly",
            "🧢 Wear light-colored, loose-fitting clothing",
            "🌳 Seek shade when outdoors"
        ]
    else:
        risk = "LOW"
        color = "#00AA00"
        recommendations = [
            "✅ Standard precautions sufficient",
            "💧 Stay hydrated",
            "☀️ Use sunscreen (SPF 30+)",
            "👨‍👩‍👧‍👦 Regular outdoor activity is fine"
        ]
    
    return {
        "risk_level": risk,
        "color": color,
        "heat_index": heat_index,
        "recommendations": recommendations
    }
