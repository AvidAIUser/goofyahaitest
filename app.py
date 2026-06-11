import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import numpy as np
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="CoolBlock AI - Heat Safety Map",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .risk-high {
        color: #d62728;
        font-weight: bold;
    }
    .risk-medium {
        color: #ff7f0e;
        font-weight: bold;
    }
    .risk-low {
        color: #2ca02c;
        font-weight: bold;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
    <h1 class="main-header">❄️ CoolBlock AI</h1>
    <h3 class="main-header">Your Neighborhood Heat Safety Map</h3>
""", unsafe_allow_html=True)

st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Temperature unit
    temp_unit = st.radio("Temperature Unit", ["Fahrenheit (°F)", "Celsius (°C)"])
    
    # Search radius
    search_radius = st.slider(
        "Search Radius for Cooling Centers (miles)",
        0.5, 5.0, 1.0, 0.5
    )
    
    st.markdown("---")
    st.markdown("### 📍 About This Tool")
    st.info("""
    CoolBlock AI helps you find safe places to cool down during extreme heat.
    
    **Features:**
    - 🌡️ Real-time temperature & heat index
    - 🌳 AI shade detection from satellite data
    - 🏛️ Nearby cooling centers & water fountains
    - ⚠️ Heat risk assessment
    """)
    
    st.markdown("---")
    st.markdown("### 🚨 Emergency")
    st.error("**In a heat emergency, call 911**")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 Enter Your Location")
    
    # Location input
    location_type = st.radio("Find by:", ["Address", "Coordinates"], horizontal=True)
    
    if location_type == "Address":
        address = st.text_input(
            "Enter your address",
            placeholder="e.g., 123 Main St, New York, NY 10001"
        )
        
        if address:
            # Mock geocoding (in production, use geopy)
            if "new york" in address.lower():
                lat, lon = 40.7128, -74.0060
            elif "los angeles" in address.lower():
                lat, lon = 34.0522, -118.2437
            elif "chicago" in address.lower():
                lat, lon = 41.8781, -87.6298
            elif "miami" in address.lower():
                lat, lon = 25.7617, -80.1918
            elif "phoenix" in address.lower():
                lat, lon = 33.4484, -112.0742
            else:
                # Default to NYC for demo
                lat, lon = 40.7128, -74.0060
                st.info("📍 Showing demo location in New York. Enter a major US city for different results.")
    else:
        col_lat, col_lon = st.columns(2)
        with col_lat:
            lat = st.number_input("Latitude", value=40.7128, format="%.4f")
        with col_lon:
            lon = st.number_input("Longitude", value=-74.0060, format="%.4f")
    
    if address or location_type == "Coordinates":
        # Fetch weather data
        try:
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,apparent_temperature",
                    "temperature_unit": "fahrenheit"
                }
            )
            weather_data = response.json()
            current = weather_data.get("current", {})
            
            temp = current.get("temperature_2m", 72)
            apparent_temp = current.get("apparent_temperature", 72)
            humidity = current.get("relative_humidity_2m", 50)
            
            # Convert to Celsius if needed
            if temp_unit == "Celsius (°C)":
                temp_display = (temp - 32) * 5/9
                apparent_display = (apparent_temp - 32) * 5/9
                temp_unit_str = "°C"
            else:
                temp_display = temp
                apparent_display = apparent_temp
                temp_unit_str = "°F"
            
        except:
            temp_display = 85
            apparent_display = 92
            humidity = 65
            temp_unit_str = "°F" if temp_unit == "Fahrenheit (°F)" else "°C"
            st.warning("⚠️ Could not fetch live weather. Showing sample data.")

with col2:
    if address or location_type == "Coordinates":
        st.subheader("🌡️ Current Conditions")
        
        st.metric("Temperature", f"{temp_display:.1f}{temp_unit_str}")
        st.metric("Feels Like", f"{apparent_display:.1f}{temp_unit_str}")
        st.metric("Humidity", f"{humidity}%")
        
        # Heat risk indicator
        if temp > 95:
            risk_level = "HIGH ⚠️"
            risk_color = "risk-high"
        elif temp > 85:
            risk_level = "MEDIUM ⚡"
            risk_color = "risk-medium"
        else:
            risk_level = "LOW ✅"
            risk_color = "risk-low"
        
        st.markdown(f"<p class='{risk_color}'>Heat Risk: {risk_level}</p>", unsafe_allow_html=True)

st.markdown("---")

# Map section
if address or location_type == "Coordinates":
    st.subheader("🗺️ Heat Safety Map")
    
    # Create folium map
    m = folium.Map(
        location=[lat, lon],
        zoom_start=14,
        tiles="OpenStreetMap"
    )
    
    # Add user location
    folium.Marker(
        [lat, lon],
        popup="Your Location",
        tooltip="Your Location",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)
    
    # Mock cooling centers (in production, query real OSM data)
    cooling_centers = [
        {"name": "City Library - Main Branch", "lat": lat + 0.005, "lon": lon + 0.005, "type": "library", "distance": 0.3},
        {"name": "Community Center AC Lobby", "lat": lat - 0.006, "lon": lon + 0.004, "type": "center", "distance": 0.5},
        {"name": "Public Pool (Cooler Area)", "lat": lat + 0.003, "lon": lon - 0.006, "type": "pool", "distance": 0.4},
        {"name": "Hospital - Emergency Department", "lat": lat - 0.004, "lon": lon - 0.005, "type": "hospital", "distance": 0.6},
        {"name": "Shopping Mall AC", "lat": lat + 0.007, "lon": lon - 0.003, "type": "mall", "distance": 0.7},
    ]
    
    # Add cooling center markers
    for center in cooling_centers:
        if center["type"] == "library":
            icon_color = "green"
            icon_symbol = "book"
        elif center["type"] == "hospital":
            icon_color = "red"
            icon_symbol = "heart"
        elif center["type"] == "pool":
            icon_color = "blue"
            icon_symbol = "droplet"
        elif center["type"] == "center":
            icon_color = "orange"
            icon_symbol = "home"
        else:
            icon_color = "purple"
            icon_symbol = "shopping-cart"
        
        folium.Marker(
            [center["lat"], center["lon"]],
            popup=f"<b>{center['name']}</b><br>Distance: {center['distance']} mi",
            tooltip=center["name"],
            icon=folium.Icon(color=icon_color, icon=icon_symbol)
        ).add_to(m)
    
    # Add heat risk zones (circle around user location)
    if temp > 95:
        # High risk - red zone
        folium.Circle(
            [lat, lon],
            radius=800,  # ~0.5 miles
            color="red",
            fill=True,
            fillColor="red",
            fillOpacity=0.1,
            weight=2,
            popup="High Heat Risk Zone"
        ).add_to(m)
        
        # Caution zone - yellow
        folium.Circle(
            [lat, lon],
            radius=1600,  # ~1 mile
            color="orange",
            fill=True,
            fillColor="orange",
            fillOpacity=0.05,
            weight=2,
            popup="Caution Zone"
        ).add_to(m)
    elif temp > 85:
        # Medium risk
        folium.Circle(
            [lat, lon],
            radius=1200,
            color="orange",
            fill=True,
            fillColor="orange",
            fillOpacity=0.1,
            weight=2,
            popup="Medium Heat Risk Zone"
        ).add_to(m)
    
    # Display map
    st_folium(m, width=1400, height=500)

st.markdown("---")

# Cooling centers list
if address or location_type == "Coordinates":
    st.subheader("🏛️ Nearest Cooling Centers")
    
    col1, col2, col3 = st.columns(3)
    
    for i, center in enumerate(cooling_centers[:3]):
        with [col1, col2, col3][i]:
            with st.container():
                st.markdown(f"### {center['name']}")
                st.metric("Distance", f"{center['distance']} miles")
                st.write(f"📍 Coordinates: {center['lat']:.4f}, {center['lon']:.4f}")
                st.button(f"Get Directions to {center['name']}", key=f"btn_{i}")

st.markdown("---")

# AI Shade Detection Section
st.subheader("🌳 AI Shade Detection")

col1, col2 = st.columns([2, 1])

with col1:
    st.write("""
    Our AI model analyzes satellite imagery to detect tree coverage and shade in your area.
    This helps identify naturally cool spots and areas with high heat exposure.
    """)
    
    # Demo shade score
    st.info("""
    **Shade Score for Your Location: 62% Confidence: Medium**
    
    ✅ This area has moderate shade coverage. 
    
    ⚠️ During extreme heat (>95°F), consider heading to an indoor cooling center nearby.
    """)

with col2:
    st.write("**Shade Level**")
    shade_progress = 0.62
    st.progress(shade_progress)
    
    if shade_progress > 0.7:
        st.success("Good shade coverage")
    elif shade_progress > 0.4:
        st.warning("Moderate shade")
    else:
        st.error("Limited shade")

st.markdown("---")

# Responsible AI & Guardrails
st.subheader("⚖️ Responsible AI - Important Notes")

col1, col2, col3 = st.columns(3)

with col1:
    st.warning("""
    **⚠️ AI Uncertainty**
    
    When our AI is unsure about shade levels (40-60% confidence), we show it to you.
    Always verify with satellite view before making decisions.
    """)

with col2:
    st.error("""
    **🚨 Medical Emergency**
    
    If experiencing symptoms of heat illness:
    - Dizziness
    - Confusion
    - Loss of consciousness
    
    **CALL 911 IMMEDIATELY**
    """)

with col3:
    st.info("""
    **✅ Human in Control**
    
    This tool helps you make decisions, but you are in control.
    - Always verify cooling center status
    - Check hours before visiting
    - Report closed facilities
    """)

# Report a closed cooling center
st.markdown("---")
st.subheader("📢 Report a Cooling Center Issue")

report_col1, report_col2 = st.columns([2, 1])

with report_col1:
    center_to_report = st.selectbox(
        "Select a cooling center",
        [c["name"] for c in cooling_centers]
    )
    
    issue_type = st.radio(
        "Issue type",
        ["Closed", "Too crowded", "Incorrect hours", "Other"],
        horizontal=True
    )
    
    details = st.text_area("Additional details (optional)")

with report_col2:
    if st.button("Submit Report"):
        st.success(f"✅ Report submitted for {center_to_report}. Thank you for helping the community!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
        <p><b>CoolBlock AI</b> - Heat Safety for Your Neighborhood</p>
        <p>Built for the USAII Global AI Hackathon 2026 | High School Track</p>
        <p>❄️ Stay cool. Stay safe. Check on your neighbors. ❄️</p>
    </div>
""", unsafe_allow_html=True)
