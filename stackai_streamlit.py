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

# Check if password is already verified in session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# If not authenticated, show the password input
if not st.session_state['authenticated']:
    st.title("🔒 Private App - Authentication Required")
    password = st.text_input("Enter the password to access the app:", type="password")
    
    if password:
        if password == "AquaponicsAssociation@2025": # Replace with your actual password
            st.session_state['authenticated'] = True
            st.rerun() # Rerun the script to show the main app
        else:
            st.error("Incorrect password. Please try again.")
    st.stop() # Stop execution here, preventing the rest of the app from showing

# If the code gets here, the user is authenticated. Show your main app.
st.title("My Private App")
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
    "SOLAR": "#FFA726",
    "BIOGAS": "#66BB6A",
    "WIND": "#42A5F5"
}

DATA_SOURCES = {
    "ENERGY": "https://raw.githubusercontent.com/ohkelly/aquatic/main/data/energy_data.csv",
    "WATER": "https://raw.githubusercontent.com/ohkelly/aquatic/main/data/sensor_data.csv",
}

# LOGO_PATH = Path("data/omfeonix-logo.png")
LOGO_PATH = "https://raw.githubusercontent.com/ohkelly/aquatic/main/data//omfeonix-logo.png"

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
        color_discrete_sequence=[
            BRAND_COLORS["SOLAR"],
            BRAND_COLORS["BIOGAS"],
            BRAND_COLORS["WIND"],
        ],
    )

    # Apply Streamlit-style formatting
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="x unified",
        xaxis=dict(
            showline=True,
            linecolor="#e1e4e8",
            gridcolor="#f0f2f6",
            title="",
        ),
        yaxis=dict(
            showline=True,
            linecolor="#e1e4e8",
            gridcolor="#f0f2f6",
            title="Power (kW)",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=None,
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Inter",
        ),
    )

    return fig


def create_water_quality_chart(df: pd.DataFrame) -> go.Figure:
    """Create water quality chart with standardized styling.

    Args:
        df: DataFrame containing water quality data.

    Returns:
        Formatted Plotly figure object.
    """
    time_col = next(
        (col for col in ["timestamp", "date", "time", "datetime"] if col in df.columns),
        df.index,
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=df[time_col],
            y=df["temperature"],
            name="Temperature (°C)",
            line=dict(color="#EF5350", width=2),  # Red for temperature
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=df[time_col],
            y=df["humidity"],
            name="Humidity (%)",
            line=dict(color="#5C6BC0", width=2),  # Blue for humidity
        ),
        secondary_y=True,
    )

    fig.update_layout(
        title_text="Temperature and Humidity Over Time",
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="x unified",
        xaxis=dict(
            showline=True,
            linecolor="#e1e4e8",
            gridcolor="#f0f2f6",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    fig.update_yaxes(
        title_text="Temperature (°C)",
        secondary_y=False,
        showline=True,
        linecolor="#e1e4e8",
        gridcolor="#f0f2f6",
    )

    fig.update_yaxes(
        title_text="Humidity (%)",
        secondary_y=True,
        showline=True,
        linecolor="#e1e4e8",
        gridcolor="#f0f2f6",
    )

    return fig


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


def show_metrics(energy_df: pd.DataFrame, water_df: pd.DataFrame) -> None:
    """Display standardized metrics cards.

    Args:
        energy_df: DataFrame containing energy metrics.
        water_df: DataFrame containing water quality metrics.
    """
    # --- Default values ---
    DEFAULT_WINDOW = "Last 1h"
    DEFAULT_TOLERANCE = 1.0

    # Initialize session state if not already set
    if "trend_window" not in st.session_state:
        st.session_state.trend_window = DEFAULT_WINDOW
    if "trend_tolerance" not in st.session_state:
        st.session_state.trend_tolerance = DEFAULT_TOLERANCE

    # --- Sidebar controls ---
    st.sidebar.markdown("## 📊 Trend Settings")

    # Reset button with auto-disappearing confirmation
    if st.sidebar.button("Reset to Defaults"):
        st.session_state.trend_window = DEFAULT_WINDOW
        st.session_state.trend_tolerance = DEFAULT_TOLERANCE

        placeholder = st.sidebar.empty()
        placeholder.success("✅ Reset applied")
        time.sleep(2.5)
        placeholder.empty()

    # Trend window selectbox
    window_choice = st.sidebar.selectbox(
        "Compare latest value against:",
        ["Global Average", "Last 1h", "Last 6h", "Last 24h"],
        index=["Global Average", "Last 1h", "Last 6h", "Last 24h"].index(st.session_state.trend_window),
        key="trend_window"
    )

    # Tolerance slider
    tolerance_pct = st.sidebar.slider(
        "Trend tolerance (% of reference)",
        min_value=0.0, max_value=10.0,
        value=st.session_state.trend_tolerance,
        step=0.1,
        key="trend_tolerance",
        help="Differences smaller than this % will be treated as stable ➡️"
    )

    # --- Reference calculation ---
    def compute_reference(series: pd.Series) -> float:
        if window_choice == "Global Average":
            return series.mean()
        elif window_choice == "Last 1h":
            return series.last("1h").mean() if isinstance(series.index, pd.DatetimeIndex) else series.tail(12).mean()
        elif window_choice == "Last 6h":
            return series.last("6h").mean() if isinstance(series.index, pd.DatetimeIndex) else series.tail(72).mean()
        elif window_choice == "Last 24h":
            return series.last("24h").mean() if isinstance(series.index, pd.DatetimeIndex) else series.tail(288).mean()
        return series.mean()

    # --- Styles + icons ---
    CATEGORY_STYLES = {
        "energy": {"border": "#2e7d32", "bg": "#e8f5e9", "icon": "⚡"},
        "operations": {"border": "#6c757d", "bg": "#f1f3f5", "icon": "🛠️"},
        "water": {"border": "#2196f3", "bg": "#e3f2fd", "icon": "💧"},
    }

    # Trend icons
    def get_trend_icon(latest: float, ref: float) -> str:
        tol = abs(ref) * (tolerance_pct / 100)
        if latest > ref + tol:
            return '<span style="color:#2e7d32;">📈</span>'
        elif latest < ref - tol:
            return '<span style="color:#d32f2f;">📉</span>'
        else:
            return '<span style="color:#6c757d;">➡️</span>'

    # Render metric card with tooltip
    def render_metric(title: str, latest_value: float, ref_numeric: float, unit: str, category: str):
        style = CATEGORY_STYLES[category]
        trend_icon = get_trend_icon(latest_value, ref_numeric)

        # Percentage deviation
        pct_dev = ((latest_value - ref_numeric) / abs(ref_numeric) * 100) if ref_numeric != 0 else 0.0

        tooltip_text = f"Latest: {latest_value:.2f} {unit}\nReference: {ref_numeric:.2f} {unit}\nDeviation: {pct_dev:+.1f}%"

        st.markdown(
            f"""
            <div class="metric-card" 
                 title="{tooltip_text}" 
                 style="border-left: 4px solid {style['border']};
                        background-color: {style['bg']}; cursor: help;">
                <div class="metric-title">{style['icon']} {title}</div>
                <div class="metric-value">{latest_value:.2f} {unit} {trend_icon}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- Energy metrics ---
    st.markdown("### ⚡ Energy Metrics")
    energy_metrics = [
        ("Solar Power", energy_df["solar"], "kW"),
        ("Wind Power", energy_df["wind"], "kW"),
        ("Biogas Power", energy_df["biogas"], "kW"),
    ]
    cols = st.columns(len(energy_metrics))
    for col, (title, series, unit) in zip(cols, energy_metrics):
        ref = compute_reference(series)
        latest = series.iloc[-1]
        with col:
            render_metric(title, latest, ref, unit, "energy")

    # --- Operations metrics ---
    st.markdown("### 🛠️ Operations Metrics")
    ops_metrics = [
        ("Pumps Usage", energy_df["pumps"], "kW"),
        ("Lighting", energy_df["lighting"], "kW"),
        ("Climate Control", energy_df["climate_control"], "kW"),
        ("Other Ops", energy_df["other_operations"], "kW"),
    ]
    cols = st.columns(len(ops_metrics))
    for col, (title, series, unit) in zip(cols, ops_metrics):
        ref = compute_reference(series)
        latest = series.iloc[-1]
        with col:
            render_metric(title, latest, ref, unit, "operations")

    # --- Water quality metrics ---
    st.markdown("### 💧 Water Quality Metrics")
    water_metrics = [
        ("Temperature", water_df["temperature"], "°C"),
        ("Humidity", water_df["humidity"], "%"),
        ("pH", water_df["pH"], ""),
        ("ORP", water_df["orp"], "mV"),
        ("EC", water_df["ec"], "mS/cm"),
        ("TDS", water_df["tds"], "ppm"),
        ("Dissolved Oxygen", water_df["do"], "mg/L"),
    ]
    cols = st.columns(3)
    for i, (title, series, unit) in enumerate(water_metrics):
        ref = compute_reference(series)
        latest = series.iloc[-1]
        with cols[i % 3]:
            render_metric(title, latest, ref, unit, "water")
        if (i + 1) % 3 == 0 and (i + 1) < len(water_metrics):
            cols = st.columns(3)  # new row


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

    with st.spinner("Loading AI Assistant..."):
        components.html(
            """
            <iframe 
                src="https://www.stack-ai.com/chat-assistant/ac72067d-4aef-4716-a438-e7ecdf656bda/5f094b2c-790b-4cad-8dba-1aa4c964932b/6782ed152ac8e84e2db9ac15"
                style="width: 100%; height: 70vh; border: none; border-radius: 8px;">
            </iframe>
            """,
            height=700,
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
