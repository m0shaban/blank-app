import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Elkatamy | Denyo Fleet Command",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to enforce Corporate Identity (Blue/Dark Grey) and "Executive" look
st.markdown("""
    <style>
        /* Global styles for dark mode consistency */
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        /* Metric Cards Styling */
        div[data-testid="stMetric"] {
            background-color: #1f2937;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #00a8e8; /* Elkatamy Blue Accent */
            box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        }
        div[data-testid="stMetricValue"] {
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 14px;
            color: #9ca3af;
        }
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #111827;
        }
        /* Header Styling */
        h1, h2, h3 {
            color: #00a8e8;
            font-family: 'Helvetica Neue', sans-serif;
        }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. MOCK DATA GENERATION (Simulating an SQL Database Connection)
# -----------------------------------------------------------------------------
@st.cache_data
def get_fleet_data():
    """
    Generates realistic mock data for 50 Denyo generators across Egypt.
    """
    np.random.seed(42)  # For reproducible results
    
    n_generators = 50
    models = ['DCA-18ESX', 'DCA-25USI', 'DCA-45USI', 'DCA-150ESK', 'DCA-400ESK']
    locations_coords = {
        'Cairo': {'lat': 30.0444, 'lon': 31.2357},
        'Giza': {'lat': 30.0131, 'lon': 31.2089},
        'Alexandria': {'lat': 31.2001, 'lon': 29.9187},
        'Aswan': {'lat': 24.0889, 'lon': 32.8998},
        'Red Sea': {'lat': 27.2579, 'lon': 33.8116},
        'Suez': {'lat': 29.9668, 'lon': 32.5498}
    }
    
    data = []
    
    for i in range(n_generators):
        loc_name = np.random.choice(list(locations_coords.keys()))
        base_lat = locations_coords[loc_name]['lat']
        base_lon = locations_coords[loc_name]['lon']
        
        # Add jitter to coords so they don't overlap perfectly on the map
        lat = base_lat + np.random.uniform(-0.05, 0.05)
        lon = base_lon + np.random.uniform(-0.05, 0.05)
        
        model = np.random.choice(models)
        
        # Correlation: Bigger models generate more revenue
        kva_map = {'DCA-18ESX': 15, 'DCA-25USI': 20, 'DCA-45USI': 37, 'DCA-150ESK': 125, 'DCA-400ESK': 350}
        kva = kva_map[model]
        revenue = np.random.randint(5000, 20000) * (kva/50) 
        
        status = np.random.choice(['Active', 'Active', 'Active', 'Idle', 'Maintenance'], p=[0.6, 0.1, 0.1, 0.1, 0.1])
        
        # Telemetry Data simulation
        fuel_level = np.random.randint(10, 100)
        temp = np.random.randint(70, 110) # Celsius
        
        # Create alerts based on logic
        alert = "None"
        if fuel_level < 20:
            alert = "Low Fuel"
        elif temp > 100:
            alert = "Overheating"
        elif status == 'Maintenance':
            alert = "Service Due"
        
        data.append({
            'Gen ID': f'DNY-{1000+i}',
            'Model': model,
            'Capacity (kVA)': kva,
            'Location': loc_name,
            'lat': lat,
            'lon': lon,
            'Status': status,
            'Monthly Revenue (EGP)': round(revenue, 2),
            'Fuel Level (%)': fuel_level,
            'Engine Temp (°C)': temp,
            'Active Alert': alert,
            'Project Site': f"{loc_name} Site-{np.random.randint(1,5)}"
        })
    
    return pd.DataFrame(data)

df = get_fleet_data()

# -----------------------------------------------------------------------------
# 3. SIDEBAR - EXECUTIVE CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.title("🎛️ Fleet Controls")
st.sidebar.markdown("Filter views to analyze specific regions or fleet segments.")

# Filters
selected_locations = st.sidebar.multiselect(
    "Filter by Region:",
    options=df['Location'].unique(),
    default=df['Location'].unique()
)

selected_status = st.sidebar.multiselect(
    "Filter by Status:",
    options=df['Status'].unique(),
    default=df['Status'].unique()
)

min_kva, max_kva = st.sidebar.slider(
    "Capacity Range (kVA):",
    int(df['Capacity (kVA)'].min()),
    int(df['Capacity (kVA)'].max()),
    (int(df['Capacity (kVA)'].min()), int(df['Capacity (kVA)'].max()))
)

# Apply Filters
df_filtered = df[
    (df['Location'].isin(selected_locations)) &
    (df['Status'].isin(selected_status)) &
    (df['Capacity (kVA)'].between(min_kva, max_kva))
]

# -----------------------------------------------------------------------------
# 4. KPI DASHBOARD HEADER (Strategic View)
# -----------------------------------------------------------------------------
st.title("⚡ Elkatamy Power Systems | Executive Dashboard")
st.markdown(f"**Live Overview**: Tracking {len(df_filtered)} Generators across Egypt.")

# Calculations
total_revenue = df_filtered['Monthly Revenue (EGP)'].sum()
utilization_rate = (len(df_filtered[df_filtered['Status'] == 'Active']) / len(df_filtered)) * 100 if len(df_filtered) > 0 else 0
critical_alerts = len(df_filtered[df_filtered['Active Alert'].isin(['Low Fuel', 'Overheating'])])
avg_fuel_efficiency = df_filtered['Fuel Level (%)'].mean() # Proxy metric

# Display KPI Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="💰 Total Monthly Revenue",
        value=f"{total_revenue/1_000_000:.2f}M EGP",
        delta=f"{np.random.randint(2, 8)}% vs last month"
    )

with kpi2:
    st.metric(
        label="⚙️ Fleet Utilization",
        value=f"{utilization_rate:.1f}%",
        delta="-2%" if utilization_rate < 70 else "+5%"
    )

with kpi3:
    st.metric(
        label="🚨 Critical Alerts",
        value=critical_alerts,
        delta="Needs Attention" if critical_alerts > 0 else "Stable",
        delta_color="inverse"
    )

with kpi4:
    st.metric(
        label="⛽ Avg Fuel Level",
        value=f"{avg_fuel_efficiency:.0f}%",
        delta=f"Refuel Schd: {datetime.date.today()}"
    )

st.divider()

# -----------------------------------------------------------------------------
# 5. MAIN VISUALIZATIONS (Geospatial & Financial)
# -----------------------------------------------------------------------------

col_map, col_chart = st.columns([2, 3])

with col_map:
    st.subheader("📍 Asset Geolocation")
    # Using simple Streamlit Map for clean look. 
    # For advanced needs, pydeck or folium could be used.
    st.map(df_filtered, color='#00a8e8', size=20, zoom=5)
    st.caption("Real-time GPS telemetry from IoT modules.")

with col_chart:
    st.subheader("📊 Revenue by Project Site")
    
    # Aggregating data for better visualization
    rev_by_site = df_filtered.groupby('Project Site')['Monthly Revenue (EGP)'].sum().reset_index().sort_values(by='Monthly Revenue (EGP)', ascending=False).head(10)
    
    fig_bar = px.bar(
        rev_by_site,
        x='Project Site',
        y='Monthly Revenue (EGP)',
        color='Monthly Revenue (EGP)',
        color_continuous_scale=['#1f2937', '#00a8e8'], # Dark grey to Elkatamy Blue
        template="plotly_dark"
    )
    fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=350)
    st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------------------------------------------------------
# 6. AI INSIGHTS & ALERTS (Predictive Analytics)
# -----------------------------------------------------------------------------

col_ai, col_table = st.columns([1, 2])

with col_ai:
    st.subheader("🤖 Elkatamy AI Insights")
    st.markdown("""
        <div style="background-color: #1a202c; padding: 15px; border-radius: 10px; border: 1px solid #00a8e8;">
            <h4 style="margin-top:0; color: #00a8e8;">⚠️ Predictive Maint. Alert</h4>
            <p style="font-size: 14px;"><strong>Asset:</strong> DNY-1023 (Aswan)</p>
            <p style="font-size: 14px;"><strong>Issue:</strong> Irregular vibration patterns detected in alternator bearing.</p>
            <p style="font-size: 14px;"><strong>Risk Score:</strong> High (85%)</p>
            <hr style="border-color: #4b5563;">
            <p style="font-size: 14px; font-weight: bold;">Recommendation:</p>
            <p style="font-size: 14px;">Dispatch technician team from Luxor branch within 24 hours to prevent catastrophic failure.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("System optimized fuel routes for Cairo sector, saving estimated 12,000 EGP next cycle.")

with col_table:
    st.subheader("📋 Active Fleet Alerts")
    
    # Filter for items needing attention
    alerts_df = df_filtered[df_filtered['Active Alert'] != 'None'][['Gen ID', 'Model', 'Location', 'Active Alert', 'Engine Temp (°C)', 'Fuel Level (%)']]
    
    if not alerts_df.empty:
        # Style the dataframe for visual impact
        st.dataframe(
            alerts_df.style.map(lambda x: 'color: #ff4b4b; font-weight: bold' if x == 'Overheating' or x == 'Low Fuel' else ''),
            use_container_width=True,
            hide_index=True,
            height=250
        )
    else:
        st.success("✅ No critical fleet alerts at this time.")

# -----------------------------------------------------------------------------
# 7. FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: grey; font-size: 12px;'>
        Elkatamy Group Internal System | Powered by Industrial IoT Telemetry | v2.4.0
    </div>
    """, unsafe_allow_html=True
)
