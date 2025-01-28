import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import logging
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import logging



# Streamlit App Layout
st.set_page_config(page_title="Aquaponics AI Assistant", layout="wide")

# Sidebar Configuration
st.sidebar.title("Aquaponics AI Dashboard")
option = st.sidebar.radio(
    "Choose an Operation:",
    ("Dashboard", "AI Assistant")
)


# Dashboard View
if option == "Dashboard":
    st.title("System Performance Metrics")
    
    
    
    # Display real-time metrics and historical data for energy and water quality csv files
    energy_data = "./data/energy_data.csv"
    water_quality_data = "./data/sensor_data.csv"
    # Convert csv files to dataframes
    energy_df = pd.read_csv(energy_data)
    water_quality_df = pd.read_csv(water_quality_data)
    # Energy Metrics    
    st.dataframe(energy_df)

    # Energy Metrics Plot
    st.subheader("Energy Usage")
    chart_data = pd.DataFrame(energy_df, columns=["solar", "biogas", "wind"])

    st.line_chart(chart_data)

    

    # Water Quality Metrics
    st.subheader("Water Quality Parameters")
    st.dataframe(water_quality_df)
    chart_data1 = pd.DataFrame(water_quality_df, columns=["temperature", "humidity"])
    st.area_chart(chart_data1)

    

# Assistant View
elif option == "AI Assistant":
    st.title("Ask the AI Assistant everything on your Aquaponics System energy and climate control -Co2 emmissions")
    
    # Embed the iframe
    components.html(
        """
        <iframe 
            
            src="https://www.stack-ai.com/chat-assistant/ac72067d-4aef-4716-a438-e7ecdf656bda/5f094b2c-790b-4cad-8dba-1aa4c964932b/6782ed152ac8e84e2db9ac15"
            style="width: 100vw; height: 100vh;" 
            title="Form" 
            allow="clipboard-read; clipboard-write">
        </iframe>
        """,
        height=600,  # Adjust the height to ensure the iframe is fully visible
    )
