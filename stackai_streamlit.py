"""AquaECO Dashboard: A Pythonic Streamlit application for aquaponics monitoring."""
import base64
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
from plotly.subplots import make_subplots


# ... the rest of your app's code goes here ...
# ==============================================
# CONSTANTS (UPPER_SNAKE_CASE)
# ==============================================
BRAND_COLORS = {
    "PRIMARY": "#2e7d32",  # Omfeonix green
    "SECONDARY": "#4caf50",
    "ACCENT": "#8bc34a",
    "DARK": "#1b5e20",
    "LIGHT": "#c8e6c9",
    "TEXT": "#333333",
    
}


# ==============================================
# UTILITY FUNCTIONS
# ==============================================
def get_base64_encoded_image(image_path: Path) -> str:
    """Encode local image to base64.

    Args:
        image_path: Path to the image file.

    Returns:
        Base64 encoded string of the image.
    """
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def load_logo_html() -> str:
    """Load and format logo HTML with proper structure."""
    try:
        return f"""
        <div style="text-align: center;">
            <a href="https://www.omfeonix.com" target="_blank" style="text-decoration: none;">
                <img src="{LOGO_PATH}" 
                     style="transition: all 0.3s; max-width: 180px; opacity: 0.9;"
                     onmouseover="this.style.opacity='1'; this.style.filter='drop-shadow(0 0 4px {BRAND_COLORS['ACCENT']})'" 
                     onmouseout="this.style.opacity='0.9'; this.style.filter='none'"
                     alt="Omfeonix Logo">
            </a>
        </div>
        """
    except Exception as e:
        logging.warning("Logo not found: %s", e)
        return f"""
        <div style="color: {BRAND_COLORS['PRIMARY']}; 
                    font-weight: 700; 
                    font-size: 1.5rem;
                    text-align: center;">
            Omfeonix
        </div>
        """


@st.cache_data
def load_data(url: str) -> Optional[pd.DataFrame]:
    """Load and preprocess data from URL.

    Args:
        url: URL to fetch CSV data from.

    Returns:
        Loaded DataFrame or None if error occurs.
    """
    try:
        df = pd.read_csv(url)
        # Standardize timestamp columns
        for col in ["date", "timestamp", "time", "datetime"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
                df = df.sort_values(col)
                break
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


# ==============================================
# CHART COMPONENTS
# ==============================================
def create_energy_chart(df: pd.DataFrame) -> go.Figure:
    """Create standardized energy chart with Streamlit styling.

    Args:
        df: DataFrame containing energy data.

    Returns:
        Formatted Plotly figure object.
    """
    time_col = next(
        (col for col in ["timestamp", "date", "time", "datetime"] if col in df.columns),
        df.index,
    )

    fig = px.line(
        df,
        x=time_col,
        y=["solar", "biogas", "wind"],
        title="Energy Generation Over Time",
    
        ],
    )

# ==============================================
# UI COMPONENTS
# ==============================================
def inject_custom_css() -> None:
    """Inject standardized CSS styles."""
    st.markdown(
        f"""
        <style>
        :root {{
            --primary: {BRAND_COLORS['PRIMARY']};
            --secondary: {BRAND_COLORS['SECONDARY']};
            --accent: {BRAND_COLORS['ACCENT']};
            --dark: {BRAND_COLORS['DARK']};
            --light: {BRAND_COLORS['LIGHT']};
        }}
        
        /* Main container styling */
        .main {{
            background-color: #f8faf9;
            padding: 0 1rem;
        }}
        
        /* Header styling */
        .main-header {{
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 1.5rem;
        }}
        
        /* Metric card styling */
        .metric-card {{
            border-left: 4px solid var(--primary);
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: all 0.2s ease;
            height: 100%;
        }}
        
        .metric-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }}
        
        .metric-title {{
            color: var(--primary);
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 5px;
        }}
        
        .metric-value {{
            color: var(--dark);
            font-size: 1.6rem;
            font-weight: 700;
        }}
        
        /* Chart container styling */
        .stPlotlyChart {{
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border: 1px solid #e1e4e8;
            background: white;
            padding: 10px;
        }}
        
        /* Responsive adjustments */
        @media (max-width: 768px) {{
            .main-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
            
            .metric-card {{
                margin-bottom: 1rem;
            }}
        }}
        
        .header-content {{
            flex: 1;
            margin-left: 20px;
        }}
        
        
        .header-title {{
            margin: 0;  
            color: var(--primary);
            font-size: 1.8rem;
            line-height: 1.2;
        }}
        .header-subtitle {{
            margin: 0.5rem 0 0 0;
            color: var(--secondary);
            font-size: 1rem;    
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==============================================
# PAGE LAYOUTS
# ==============================================
def render_dashboard() -> None:
    """Render the main dashboard view."""
    # Load data
    energy_df = load_data(DATA_SOURCES["ENERGY"])
    water_df = load_data(DATA_SOURCES["WATER"])

    if energy_df is None or water_df is None:
        st.warning("No data available - please check your data sources")
        return

    # Header section
    st.markdown(
        f"""
        <div class="main-header" style="display: flex; align-items: center; gap: 20px; margin-bottom: 1.5rem;">
            {LOGO_HTML}
            
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.title("🌊 AquaECO AI Aquaponics System Performance Dashboard")

    # Metrics overview
    st.markdown("## System Metrics Overview")
    show_metrics(energy_df, water_df)

    # Energy metrics section
    st.markdown("---")
    st.markdown(
        f"## <span style='color:{BRAND_COLORS['PRIMARY']}'>Energy Performance Trend</span>",
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["Trends", "Composition", "Raw Data"])

    with tab1:
        fig = create_energy_chart(energy_df)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        energy_sum = energy_df[["solar", "biogas", "wind"]].sum()
        fig = px.pie(
            values=energy_sum,
            names=energy_sum.index,
            title="Energy Source Composition",
            color=energy_sum.index,
            color_discrete_sequence=[
                BRAND_COLORS["SOLAR"],
                BRAND_COLORS["BIOGAS"],
                BRAND_COLORS["WIND"],
            ],
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        with st.expander("View Raw Energy Data"):
            st.dataframe(energy_df.style.background_gradient(cmap='Greens'), use_container_width=True)

    # Water quality section
    st.markdown("---")
    st.markdown(
        f"## <span style='color:{BRAND_COLORS['PRIMARY']}'>Water Quality Performance Trend</span>",
        unsafe_allow_html=True,
    )

    wq_tab1, wq_tab2, wq_tab3 = st.tabs(["Temperature & Humidity", "Correlations", "Raw Data"])

    with wq_tab1:
        # fig = create_water_quality_chart(water_df)
        # st.plotly_chart(fig, use_container_width=True)
        # Identify time column
        time_col = "timestamp" if "timestamp" in water_df.columns else water_df.index

        # Melt DataFrame for long format (better for px.line)
        df_melted = water_df.melt(
            id_vars=[time_col],
            value_vars=["temperature", "humidity"],
            var_name="Parameter",
            value_name="Value"
        )

        # Create line chart
        fig = px.line(
            df_melted,
            x=time_col,
            y="Value",
            color="Parameter",
            title="Temperature and Humidity Over Time",
            color_discrete_map={
                "temperature": "#EF5350",  # Red
                "humidity": "#5C6BC0"      # Blue
            }
        )

        # Improve layout
        fig.update_layout(
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                title=None
            ),
            xaxis_title="",
            yaxis_title="Values",
            plot_bgcolor="white",
            paper_bgcolor="white",
        )

        st.plotly_chart(fig, use_container_width=True)

    with wq_tab2:
        # Correlation heatmap if there are more parameters
        if len(water_df.columns) > 2:
            numeric_cols = water_df.select_dtypes(include=["float64", "int64"]).columns
            corr_matrix = water_df[numeric_cols].corr()
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="Viridis",
                title="Water Quality Parameter Correlations",
            )
            st.plotly_chart(fig, use_container_width=True)

    with wq_tab3:
        with st.expander("View Raw Water Quality Data"):
            st.dataframe(water_df.style.background_gradient(cmap='Blues'), use_container_width=True)


def render_ai_assistant() -> None:
    """Render the AI Assistant view."""
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 1.5rem;">
            {LOGO_HTML}
            
        </div>
        """,
        unsafe_allow_html=True,
    )

   
    st.markdown(
        f"""
        <div style="margin-top: 20px; padding: 20px; background-color: {BRAND_COLORS['LIGHT']}; 
            border-radius: 10px; border-left: 4px solid {BRAND_COLORS['PRIMARY']};">
            <h4 style="color: {BRAND_COLORS['PRIMARY']}; margin-top: 0;">💡 Assistant Tips</h4>
            <ul style="color: {BRAND_COLORS['DARK']};">
                <li>Ask "How can I optimize energy usage in my system?"</li>
                <li>Request "Show me ideal water parameters for tilapia"</li>
                <li>Try "What's causing these temperature fluctuations?"</li>
                <li>Ask "How can I reduce my system's carbon footprint?"</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==============================================
# MAIN APP
# ==============================================
def main() -> None:
    """Main application entry point."""
    # Initialize app
    st.set_page_config(
        page_title="AquaECO Dashboard",
        page_icon="🌿",
        layout="wide",
    )

    # Load logo and inject CSS
    global LOGO_HTML
    LOGO_HTML = load_logo_html()
    inject_custom_css()

    # Sidebar navigation
    with st.sidebar:
        st.markdown(
            f'<div class="sidebar-logo-container">{LOGO_HTML}</div>',
            unsafe_allow_html=True,
        )
        st.title("🌿 Navigation")
        option = st.radio(
            "Navigation",  # Non-empty label
            ("Dashboard", "AI Assistant"),
            index=0,
            label_visibility="collapsed",
        )

        if option == "Dashboard":
            st.markdown("---")
            st.markdown("### Date Range Selector")
            current_date = datetime.now()
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input(
                    "Start date",
                    value=current_date.replace(year=current_date.year - 1),
                    max_value=current_date,
                )
            with col2:
                end_date = st.date_input(
                    "End date",
                    value=current_date,
                    max_value=current_date,
                )

    # Render selected page
    if option == "Dashboard":
        render_dashboard()
    else:
        render_ai_assistant()


if __name__ == "__main__":
    main()
