import streamlit as st
import requests
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, timedelta
import os
from sklearn.ensemble import IsolationForest
from io import StringIO

# API Configuration (Replace with your AlienVault OTX API key)
API_KEY = os.getenv("OTX_API_KEY", "6ce8f39aeae56d40d4736b98249f4306da4407c069fb463bee2e420a59173a60")  # Get from https://otx.alienvault.com/
API_URL = "https://otx.alienvault.com/api/v1/pulses/subscribed"

# Database setup
DB_NAME = "threat_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS threats (
            indicator TEXT PRIMARY KEY,
            type TEXT,
            description TEXT,
            created_at TEXT,
            country_code TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_threat_data():
    if not API_KEY:
        st.error("API key not set. Please configure OTX_API_KEY as an environment variable.")
        return []

    headers = {
        'X-OTX-API-KEY': API_KEY,
        'Accept': 'application/json'
    }
    try:
        response = requests.get(API_URL, headers=headers, params={'limit': 100})
        response.raise_for_status()
        pulses = response.json().get('results', [])
        indicators = []
        for pulse in pulses:
            for indicator in pulse.get('indicators', []):
                indicators.append({
                    'indicator': indicator['indicator'],
                    'type': indicator['type'],
                    'description': indicator.get('description', 'No description'),
                    'created_at': pulse.get('created', ''),
                    'country_code': indicator.get('country_code', 'Unknown')
                })
        return indicators
    except requests.RequestException as e:
        st.error(f"Error fetching data from OTX: {e}")
        return []

def store_data(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    for entry in data:
        c.execute('''
            INSERT OR REPLACE INTO threats (indicator, type, description, created_at, country_code)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            entry['indicator'],
            entry['type'],
            entry['description'],
            entry['created_at'],
            entry['country_code']
        ))
    conn.commit()
    conn.close()

def load_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM threats", conn)
    conn.close()
    return df

def analyze_data(df, run_anomaly=True):
    # Top indicators by frequency
    top_indicators = df['indicator'].value_counts().head(10).reset_index()
    top_indicators.columns = ['indicator', 'count']

    # Threat count by country
    country_counts = df['country_code'].value_counts().reset_index()
    country_counts.columns = ['country_code', 'count']

    # Indicator type distribution
    type_counts = df['type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']

    # Convert created_at to datetime
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

    # Threats over time (last 7 days for trends)
    last_week = datetime.now() - timedelta(days=7)
    recent_threats = df[df['created_at'] >= last_week]
    time_trend = recent_threats.groupby(recent_threats['created_at'].dt.date).size().reset_index(name='count')

    anomalies = pd.DataFrame(columns=['indicator', 'type', 'country_code', 'indicator_freq'])
    if run_anomaly and not df.empty:
        df['indicator_freq'] = df.groupby('indicator')['indicator'].transform('count')
        df['type_encoded'] = df['type'].astype('category').cat.codes
        features = df[['indicator_freq', 'type_encoded']].fillna(0)

        iso_forest = IsolationForest(contamination=0.05, random_state=42)
        df['anomaly'] = iso_forest.fit_predict(features)
        anomalies = df[df['anomaly'] == -1][['indicator', 'type', 'country_code', 'indicator_freq']]

    return top_indicators, country_counts, time_trend, type_counts, anomalies

def main():
    st.title("Mini Threat Intelligence Dashboard (Powered by LevelBlue OTX)")

    # Initialize database
    init_db()

    # Fetch and store data
    if st.button("Fetch Latest Threat Data"):
        with st.spinner("Fetching data from AlienVault OTX..."):
            data = fetch_threat_data()
            if data:
                store_data(data)
                st.success("Data fetched and stored successfully!")

    # Load data
    df = load_data()

    if df.empty:
        st.warning("No data available. Please fetch threat data.")
        return

    # Date range filter
    st.subheader("Filter by Date Range")
    date_filter = st.radio("Select Date Range:", ("Last 24h", "Last 7 Days", "Last 30 Days", "All"))
    now = datetime.now()
    if date_filter == "Last 24h":
        df = df[pd.to_datetime(df['created_at'], errors='coerce') >= (now - timedelta(hours=24))]
    elif date_filter == "Last 7 Days":
        df = df[pd.to_datetime(df['created_at'], errors='coerce') >= (now - timedelta(days=7))]
    elif date_filter == "Last 30 Days":
        df = df[pd.to_datetime(df['created_at'], errors='coerce') >= (now - timedelta(days=30))]

    # KPI Metrics
    st.subheader("Key Metrics")
    total_threats = len(df)
    unique_indicators = df['indicator'].nunique()
    col1, col2 = st.columns(2)
    col1.metric("Total Threats", total_threats)
    col2.metric("Unique Indicators", unique_indicators)

    # Toggle anomaly detection
    run_anomaly = st.checkbox("Run Anomaly Detection", value=True)

    # Analyze data
    top_indicators, country_counts, time_trend, type_counts, anomalies = analyze_data(df, run_anomaly)

    # Search functionality
    st.subheader("Search Indicators")
    search_term = st.text_input("Enter IP, domain, or URL to search:")
    if search_term:
        search_results = df[df['indicator'].str.contains(search_term, case=False, na=False)]
        if not search_results.empty:
            st.write("Search Results:")
            st.dataframe(search_results[['indicator', 'type', 'country_code', 'created_at']])
        else:
            st.warning("No matching indicators found.")

    # Visualizations
    st.subheader("Top 10 Malicious Indicators")
    fig1 = px.bar(top_indicators, x='indicator', y='count', title="Top Indicators by Frequency")
    st.plotly_chart(fig1)

    st.subheader("Threats by Country")
    fig2 = px.scatter_geo(country_counts, locations="country_code", size="count", title="Threat Heatmap by Country",
                         locationmode="ISO-3", projection="natural earth")
    st.plotly_chart(fig2)

    st.subheader("Threat Trends (Last 7 Days)")
    fig3 = px.line(time_trend, x='created_at', y='count', title="Threats Over Time")
    st.plotly_chart(fig3)

    st.subheader("Indicator Type Distribution")
    fig4 = px.pie(type_counts, names='type', values='count', title="Distribution of Indicator Types")
    st.plotly_chart(fig4)

    if run_anomaly:
        st.subheader("Anomalous Indicators")
        if not anomalies.empty:
            st.write("Indicators flagged as anomalies (unusual frequency or type):")
            st.dataframe(anomalies)
        else:
            st.info("No anomalies detected.")

    # Data export
    st.subheader("Export Data")
    if st.button("Download Threat Data as CSV"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="threat_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
