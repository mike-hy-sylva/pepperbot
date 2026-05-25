import streamlit as st
import ee
import geemap.foliumap as geemap
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from streamlit_folium import folium_static

st.set_page_config(page_title="Pepper Agriculture Dashboard - Espirito Santo", layout="wide")

st.title("🌶️ Pepper Agriculture Dashboard - Espirito Santo, Brazil")
st.markdown("Monitor agricultural parcels, NDVI trends, and harvest quality metrics.")

# Initialize Earth Engine
try:
    ee.Initialize(project='centinela')
except Exception as e:
    st.warning("Please authenticate Earth Engine: `earthengine authenticate`")

# 1. Map Section
st.header("1. Agricultural Parcels Delineation")
st.markdown("Displays regions filtered by WDPA, Dynamic World agricultural land, and segmented parcels.")

# Center on Espirito Santo
Map = geemap.Map(center=[-19.18, -40.30], zoom=7)

try:
    # Dummy representation for Earth Engine layers
    # ES Boundary
    es = ee.FeatureCollection("FAO/GAUL/2015/level1").filter(ee.Filter.eq('ADM1_NAME', 'Espirito Santo'))
    Map.addLayer(es, {'color': 'red'}, 'Espirito Santo Boundary')
    
    # Dynamic World - Crop Land (class 4)
    dw = ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1").filterBounds(es).filterDate('2023-01-01', '2024-01-01').mode()
    crops = dw.select('label').eq(4)
    Map.addLayer(crops.selfMask(), {'palette': ['green']}, 'Dynamic World - Crop Land')
    
except Exception as e:
    st.error(f"Earth Engine data error: {e}")

folium_static(Map)

# 2. Data Analysis: DOY NDVI
st.header("2. Historical vs. Current NDVI")

# Generate mock data for demonstration
days = np.arange(1, 366)
hist_ndvi = 0.5 + 0.3 * np.sin(2 * np.pi * days / 365)
curr_ndvi = hist_ndvi + np.random.normal(0, 0.05, 365)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(days, hist_ndvi, label="5-Year Historical Average", color="blue")
ax.plot(days, curr_ndvi, label="Current Year", color="orange", alpha=0.7)
ax.set_xlabel("Day of Year (DOY)")
ax.set_ylabel("NDVI")
ax.set_title("NDVI Trends over DOY")
ax.legend()
st.pyplot(fig)

# 3. Harvest Quality Metrics
st.header("3. Harvest Quality Metrics")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Current NDVI Anomaly", value="+0.02", delta="Good Quality")
    st.markdown("Cumulative Rainfall: **450 mm**")

with col2:
    st.metric(label="Expected Harvest Date", value="Oct 2026", delta="On Track")
    
# 4. Action Button
st.header("4. Procurement")
st.markdown("Ready to purchase the intake?")
contact_email = "your.email@example.com"
st.markdown(f'<a href="mailto:{contact_email}?subject=Pepper%20Intake%20Purchase"><button style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;">Buy Pepper Intake</button></a>', unsafe_allow_html=True)
