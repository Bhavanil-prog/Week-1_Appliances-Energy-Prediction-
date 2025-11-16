"""
Dashboard entrypoint for Streamlit. This file now performs graceful import checks
and prints helpful install instructions if required packages are missing.
"""

import sys

try:
    import streamlit as st  # type: ignore
except Exception:
    print("Error: 'streamlit' is not installed or could not be imported.")
    print("Install it with: python -m pip install streamlit")
    sys.exit(1)

try:
    import pandas as pd  # type: ignore
except Exception:
    print("Error: 'pandas' is not installed or could not be imported.")
    print("Install it with: python -m pip install pandas")
    sys.exit(1)

try:
    import numpy as np  # type: ignore
except Exception:
    print("Error: 'numpy' is not installed or could not be imported.")
    print("Install it with: python -m pip install numpy")
    sys.exit(1)

try:
    import plotly.graph_objects as go  # type: ignore
    import plotly.express as px  # type: ignore
except Exception:
    print("Error: 'plotly' is not installed or could not be imported.")
    print("Install it with: python -m pip install plotly")
    sys.exit(1)
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Energy Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('../energydata_complete.csv')
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y %H:%M')
    df = df.sort_values('date').reset_index(drop=True)
    
    # Create time features
    df['hour'] = df['date'].dt.hour
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['weekday'] = df['date'].dt.dayofweek
    
    return df

@st.cache_data
def prepare_model():
    df = load_data()
    
    feature_cols = [col for col in df.columns if col not in ['date', 'Appliances']]
    X = df[feature_cols].fillna(df[feature_cols].mean())
    y = df['Appliances']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
    model.fit(X_train_scaled, y_train)
    
    predictions = model.predict(X_test_scaled)
    
    metrics = {
        'mae': mean_absolute_error(y_test, predictions),
        'rmse': np.sqrt(mean_squared_error(y_test, predictions)),
        'r2': r2_score(y_test, predictions)
    }
    
    return df, model, scaler, feature_cols, metrics

# Load data and model
df = load_data()
model, scaler, feature_cols, metrics = prepare_model()[1:]

# Header
st.markdown("# ⚡ Energy Consumption Dashboard")
st.markdown("Advanced analytics and predictions for building energy usage")

# Sidebar
with st.sidebar:
    st.header("🔧 Controls")
    view = st.radio("Select View", 
        ["📊 Overview", "📈 Analytics", "🤖 AI Predictions", "🔍 Deep Dive"])

if view == "📊 Overview":
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Appliances", f"{df['Appliances'].mean():.2f} Wh", 
                 f"{(df['Appliances'].std()):.2f} σ")
    
    with col2:
        st.metric("Avg Lights", f"{df['lights'].mean():.2f} Wh",
                 f"{(df['lights'].std()):.2f} σ")
    
    with col3:
        st.metric("Avg Temperature", f"{df['T1'].mean():.2f}°C",
                 f"Range: {df['T1'].min():.1f}°C - {df['T1'].max():.1f}°C")
    
    with col4:
        st.metric("Total Records", f"{len(df):,}",
                 f"{(len(df)/60):.1f} days")
    
    st.divider()
    
    # Energy Consumption Overview
    col1, col2 = st.columns(2)
    
    with col1:
        # Hourly pattern
        hourly = df.groupby('hour').agg({
            'Appliances': 'mean',
            'lights': 'mean'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hourly['hour'],
            y=hourly['Appliances'],
            name='Appliances',
            mode='lines+markers',
            line=dict(color='#2563eb', width=3),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=hourly['hour'],
            y=hourly['lights'],
            name='Lights',
            mode='lines+markers',
            line=dict(color='#f59e0b', width=3),
            marker=dict(size=8)
        ))
        fig.update_layout(
            title="Hourly Energy Consumption Pattern",
            xaxis_title="Hour of Day",
            yaxis_title="Energy (Wh)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Daily pattern
        df['day_date'] = df['date'].dt.date
        daily = df.groupby('day_date').agg({
            'Appliances': 'mean',
            'lights': 'mean'
        }).reset_index().tail(30)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=daily['day_date'],
            y=daily['Appliances'],
            name='Appliances',
            marker=dict(color='#2563eb')
        ))
        fig.add_trace(go.Bar(
            x=daily['day_date'],
            y=daily['lights'],
            name='Lights',
            marker=dict(color='#f59e0b')
        ))
        fig.update_layout(
            title="Daily Energy Consumption (Last 30 Days)",
            xaxis_title="Date",
            yaxis_title="Energy (Wh)",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Room temperature analysis
    st.subheader("🏠 Room Temperature Distribution")
    temp_cols = [col for col in df.columns if col.startswith('T')][:8]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure()
        for col in temp_cols:
            fig.add_trace(go.Box(
                y=df[col],
                name=col,
                boxmean='sd'
            ))
        fig.update_layout(
            title="Temperature by Room",
            yaxis_title="Temperature (°C)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average temp by room
        room_temps = pd.DataFrame({
            'Room': temp_cols,
            'Avg Temp': [df[col].mean() for col in temp_cols],
            'Max Temp': [df[col].max() for col in temp_cols],
            'Min Temp': [df[col].min() for col in temp_cols]
        })
        
        fig = px.bar(room_temps, x='Room', y='Avg Temp',
                    title="Average Temperature by Room",
                    color='Avg Temp', color_continuous_scale='Viridis')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

elif view == "📈 Analytics":
    st.header("📈 Advanced Analytics")
    
    # Correlation analysis
    st.subheader("Correlation Analysis")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Select columns for correlation
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        correlation_cols = st.multiselect(
            "Select columns for correlation",
            numeric_cols,
            default=['Appliances', 'lights', 'T1', 'T_out', 'RH_1', 'Press_mm_hg'][:5]
        )
        
        if correlation_cols:
            corr_matrix = df[correlation_cols].corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr_matrix.values,
                texttemplate='%{text:.2f}',
                colorbar=dict(title="Correlation")
            ))
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.info("""
        **Correlation Insights:**
        - Values close to +1 indicate strong positive correlation
        - Values close to -1 indicate strong negative correlation
        - Values near 0 indicate weak or no correlation
        """)
    
    # Time series decomposition
    st.subheader("Time Series Pattern")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Weekday comparison
        weekday_data = df.groupby('weekday')['Appliances'].mean()
        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        fig = px.bar(x=weekday_names, y=weekday_data.values,
                    title="Average Energy by Day of Week",
                    labels={'x': 'Day', 'y': 'Energy (Wh)'},
                    color=weekday_data.values,
                    color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Monthly comparison
        monthly_data = df.groupby('month')['Appliances'].mean()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        fig = px.line(x=month_names[:len(monthly_data)], y=monthly_data.values,
                     title="Energy Trend by Month",
                     labels={'x': 'Month', 'y': 'Energy (Wh)'},
                     markers=True)
        fig.update_traces(line=dict(color='#2563eb', width=3), marker=dict(size=10))
        st.plotly_chart(fig, use_container_width=True)

elif view == "🤖 AI Predictions":
    st.header("🤖 AI-Powered Predictions")
    
    st.info("🔬 Machine Learning Model: Random Forest Regressor with 100 trees")
    
    # Model Performance
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("R² Score", f"{metrics['r2']:.4f}", "Higher is better ↑")
    with col2:
        st.metric("Mean Absolute Error", f"{metrics['mae']:.2f} Wh", "Lower is better ↓")
    with col3:
        st.metric("RMSE", f"{metrics['rmse']:.2f} Wh", "Lower is better ↓")
    
    st.divider()
    
    # Prediction interface
    st.subheader("Make Predictions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        temp = st.slider("Temperature (°C)", 
                        min_value=float(df['T1'].min()), 
                        max_value=float(df['T1'].max()),
                        value=float(df['T1'].mean()))
    
    with col2:
        humidity = st.slider("Humidity (%)", 
                            min_value=0.0, 
                            max_value=100.0,
                            value=float(df['RH_1'].mean()))
    
    with col3:
        hour = st.slider("Hour (0-23)", 
                        min_value=0, 
                        max_value=23,
                        value=12)
    
    # Prepare prediction
    pred_data = []
    for col in feature_cols:
        if col == 'T1':
            pred_data.append(temp)
        elif col == 'RH_1':
            pred_data.append(humidity)
        elif col == 'hour':
            pred_data.append(hour)
        else:
            pred_data.append(df[col].mean())
    
    # Make prediction
    pred_scaled = scaler.transform([pred_data])
    prediction = model.predict(pred_scaled)[0]
    prediction = max(0, prediction)
    
    # Display prediction
    st.divider()
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Predicted Energy Consumption", f"{prediction:.2f} Wh", "⚡")
    
    with col2:
        # Context
        avg_consumption = df['Appliances'].mean()
        diff_percent = ((prediction - avg_consumption) / avg_consumption) * 100
        
        if abs(diff_percent) < 10:
            status = "🟢 Normal"
        elif diff_percent > 10:
            status = "🟡 Above Average"
        else:
            status = "🟢 Below Average"
        
        st.write(f"**Status:** {status}")
        st.write(f"Average consumption: {avg_consumption:.2f} Wh")
        st.write(f"Difference: {diff_percent:+.1f}%")
    
    # Feature importance
    st.subheader("Feature Importance")
    feature_importance = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False).head(10)
    
    fig = px.bar(feature_importance, x='Importance', y='Feature',
                orientation='h', title="Top 10 Important Features",
                color='Importance', color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

elif view == "🔍 Deep Dive":
    st.header("🔍 Deep Analysis")
    
    # Distribution analysis
    st.subheader("Energy Consumption Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(df, x='Appliances', nbins=50,
                          title="Appliances Energy Distribution",
                          color_discrete_sequence=['#2563eb'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.histogram(df, x='lights', nbins=50,
                          title="Lights Energy Distribution",
                          color_discrete_sequence=['#f59e0b'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Scatter plots
    st.subheader("Relationships")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(df.sample(min(1000, len(df))), 
                        x='T1', y='Appliances',
                        title="Temperature vs Appliances Energy",
                        trendline="ols",
                        color='hour',
                        color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(df.sample(min(1000, len(df))), 
                        x='RH_1', y='lights',
                        title="Humidity vs Lights Energy",
                        trendline="ols",
                        color='hour',
                        color_continuous_scale='Plasma')
        st.plotly_chart(fig, use_container_width=True)
    
    # Data statistics
    st.subheader("Data Statistics")
    
    stats_df = df[['Appliances', 'lights', 'T1', 'RH_1', 'T_out', 'Press_mm_hg']].describe()
    st.dataframe(stats_df.round(3), use_container_width=True)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #6b7280; font-size: 0.9rem;'>
    <p>⚡ Energy Consumption Dashboard | Built with Streamlit & ML</p>
    <p>Data-driven insights for sustainable energy management</p>
</div>
""", unsafe_allow_html=True)
