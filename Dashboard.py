import streamlit as st
import pandas as pd
import plotly.express as px
# import plotly.graph_objects as go
# import plotly_express as px
# from plotly.subplots import make_subplots
# import seaborn as sns
# import matplotlib.pyplot as plt
from datetime import datetime
# import numpy as np
import time

# Set page configuration
st.set_page_config(
    page_title="EV Population Analysis Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS with animations and enhanced styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background-color: #d9e7f1;
        padding: 0rem 1rem;
    }
    
    /* Metric cards styling with hover effect */
    .stMetric {
        background: linear-gradient(135deg, #d9e7f1, #7daaf5);
        color: white !important;
        padding: 15px;
        border-radius: 10px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Custom container styling */
    .custom-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Header styling with gradient */
    .main-header {
        background: linear-gradient(135deg, #d9e7f1, #7daaf5);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        animation: fadeIn 1s ease-in;
    }
    
    /* Loading animation */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 4px;
        padding: 8px 16px;
        transition: background-color 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e0e2e6;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f1f3f6;
    }
    
    /* Chart container styling */
    .chart-container {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
    }
    .chart-container:hover {
        transform: scale(1.01);
    }
    </style>
    """, unsafe_allow_html=True)

# Add loading animation
with st.spinner('Loading Dashboard...'):
    time.sleep(1)

# Header with animation
st.markdown("""
    <div class="main-header">
        <h1>🚗 Electric Vehicle Population Analysis</h1>
        <p>Interactive Dashboard for EV Market Insights</p>
    </div>
    """, unsafe_allow_html=True)

# Load data with progress bar
@st.cache_data
def load_data():
    df = pd.read_csv("data-to-visualize/Electric_Vehicle_Population_Data.csv")
    df['Model Year'] = pd.to_numeric(df['Model Year'], errors='coerce')
    return df

# Custom color schemes
color_scheme = px.colors.qualitative.Set3
background_color = '#f8f9fa'

# Load the data
df = load_data()

# Sidebar with enhanced styling
st.sidebar.markdown("""
    <div style='background: linear-gradient(120deg, #d9e7f1, #7daaf5); 
                padding: 20px; 
                border-radius: 10px; 
                color: white;'>
        <h2 style='text-align: center;'>Dashboard Controls</h2>
    </div>
    """, unsafe_allow_html=True)

# Year range filter with animation
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df['Model Year'].min()),
    max_value=int(df['Model Year'].max()),
    value=(int(df['Model Year'].min()), int(df['Model Year'].max())),
    help="Drag to select your desired year range"
)

# Make selection with search
make_list = sorted(df['Make'].unique())
selected_make = st.sidebar.multiselect(
    "Select Make",
    make_list,
    default=make_list[:5],
    help="You can select multiple manufacturers"
)

# Filter data
filtered_df = df[
    (df['Model Year'].between(year_range[0], year_range[1])) &
    (df['Make'].isin(selected_make))
]

# Animated metrics
with st.container():
    col1, col2, col3 = st.columns(3)
    
    # Add animation delay for each metric
    with col1:
        time.sleep(0.2)
        st.metric("Total EVs", f"{len(filtered_df):,}", 
                 delta=f"{len(filtered_df)/len(df)*100:.1f}% of total")
    with col2:
        time.sleep(0.2)
        st.metric("Unique Makes", filtered_df['Make'].nunique(),
                 delta=f"{filtered_df['Make'].nunique()} manufacturers")
    with col3:
        time.sleep(0.2)
        st.metric("Unique Models", filtered_df['Model'].nunique(),
                 delta=f"{filtered_df['Model'].nunique()} variations")

# Create tabs with enhanced styling
tab1, tab2, tab3 = st.tabs(["📊 Makes & Models", "🗺️ Geographic Analysis", "⚡ Technical Details"])

with tab1:
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)
    
    # Top manufacturers with enhanced styling
    fig_makes = px.bar(
        filtered_df['Make'].value_counts().head(10),
        title="Top 10 EV Manufacturers",
        labels={'value': 'Number of Vehicles', 'index': 'Manufacturer'},
        color_discrete_sequence=px.colors.qualitative.Set3,
        template='plotly_white'
    )
    fig_makes.update_layout(
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        title_x=0.5,
        title_font_size=20
    )
    st.plotly_chart(fig_makes, use_container_width=True)
    
    # Model distribution with animations
    selected_manufacturer = st.selectbox(
        "Select Manufacturer for Model Distribution",
        sorted(filtered_df['Make'].unique())
    )
    
    model_dist = filtered_df[filtered_df['Make'] == selected_manufacturer]['Model'].value_counts()
    fig_models = px.pie(
        values=model_dist.values,
        names=model_dist.index,
        title=f"Model Distribution for {selected_manufacturer}",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_models.update_traces(textposition='inside', textinfo='percent+label')
    fig_models.update_layout(
        showlegend=False,
        title_x=0.5,
        title_font_size=20
    )
    st.plotly_chart(fig_models, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)
    
    # Geographic distribution with enhanced visuals
    col1, col2 = st.columns(2)
    
    with col1:
        city_counts = filtered_df['City'].value_counts().head(15)
        fig_cities = px.bar(
            city_counts,
            title="Top 15 Cities by EV Population",
            labels={'value': 'Number of Vehicles', 'index': 'City'},
            color=city_counts.values,
            color_continuous_scale='Viridis'
        )
        fig_cities.update_layout(title_x=0.5, title_font_size=20)
        st.plotly_chart(fig_cities, use_container_width=True)
    
    with col2:
        county_counts = filtered_df['County'].value_counts()
        fig_counties = px.pie(
            values=county_counts.values,
            names=county_counts.index,
            title="EV Distribution by County",
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig_counties.update_layout(title_x=0.5, title_font_size=20)
        st.plotly_chart(fig_counties, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)
    
    # Technical specifications with interactive elements
    col1, col2 = st.columns(2)
    
    with col1:
        fig_range = px.histogram(
            filtered_df,
            x="Electric Range",
            title="Distribution of Electric Range",
            labels={'Electric Range': 'Range (miles)'},
            color_discrete_sequence=['#4B79E4'],
            opacity=0.7
        )
        fig_range.update_layout(
            title_x=0.5,
            title_font_size=20,
            bargap=0.1
        )
        st.plotly_chart(fig_range, use_container_width=True)
    
    with col2:
        msrp_data = filtered_df[filtered_df['Base MSRP'] > 0]
        fig_msrp = px.box(
            msrp_data,
            x='Make',
            y='Base MSRP',
            title="Base MSRP Distribution",
            color='Make',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_msrp.update_layout(
            title_x=0.5,
            title_font_size=20,
            showlegend=False
        )
        st.plotly_chart(fig_msrp, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer with gradient
st.markdown("""
    <div style='background: linear-gradient(135deg, #d9e7f1, #7daaf5);
                color: Black;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin-top: 30px;'>
        <p>Dashboard created for MapUp Analytics Assessment</p>
        <p>Last updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%B %d, %Y")), unsafe_allow_html=True)

