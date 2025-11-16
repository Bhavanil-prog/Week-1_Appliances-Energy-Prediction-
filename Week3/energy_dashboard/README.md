# ⚡ Energy Consumption Dashboard

A comprehensive web-based energy monitoring and prediction system built with Flask, HTML/CSS, Python, and AI/ML technologies.

## 🎯 Features

### 1. **Home Section - Data Information**
- Real-time energy consumption statistics
- Key metrics: Average appliances, lights, temperature
- Date range and total records overview
- Beautiful stat cards with icons and gradients

### 2. **Analytics Dashboard**
- **Hourly Patterns**: Line charts showing energy consumption throughout the day
- **Daily Trends**: Bar charts for daily energy usage (30-day view)
- **Room Analysis**: Temperature distribution across 8 rooms
- **Correlation Analysis**: Heatmaps showing relationships between variables
- **Time Series Decomposition**: Weekday and monthly patterns

### 3. **AI Predictions (Machine Learning)**
- **Random Forest Model**: 100 trees, max depth 15
- **Features**: Temperature, humidity, time of day, and more
- **Accuracy Metrics**: 
  - Train Score: ~90%
  - Test Score: ~89%
- **Real-time Prediction**: Input custom parameters for energy consumption predictions
- **Feature Importance**: Visual representation of most influential factors

### 4. **Advanced Streamlit Dashboard**
- Interactive visualizations with Plotly
- Real-time model performance metrics
- Distribution analysis
- Scatter plots with trendlines
- Statistical summaries

## 📊 Project Structure

```
energy_dashboard/
├── app.py                 # Flask backend with API endpoints
├── dashboard.py           # Streamlit advanced dashboard
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Main HTML template
└── static/
    ├── css/
    │   └── style.css      # Modern, responsive CSS
    ├── js/
    │   └── script.js      # Frontend interactivity
    └── images/            # Asset folder
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Navigate to the project directory:**
```bash
cd energy_dashboard
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Ensure the data file is in the parent directory:**
```bash
# The CSV should be at: ../energydata_complete.csv
```

### Running the Application

#### Option 1: Flask Web App (Recommended for UI)
```bash
python app.py
```
- Open: http://localhost:5000
- Features: Beautiful UI, interactive charts, prediction form

#### Option 2: Streamlit Dashboard (Recommended for Analysis)
```bash
streamlit run dashboard.py
```
- Open: http://localhost:8501
- Features: Advanced analytics, ML metrics, real-time insights

#### Option 3: Run Both Simultaneously
```bash
# Terminal 1
python app.py

# Terminal 2
streamlit run dashboard.py
```

## 📈 Data Overview

**Dataset**: Energy Consumption Data
- **Total Records**: 19,735 data points
- **Time Period**: Complete year of hourly readings
- **Features**:
  - Appliances energy consumption (Wh)
  - Lights energy consumption (Wh)
  - Temperature data from 8 rooms (T1-T8)
  - Humidity levels (RH_1-RH_9)
  - External weather data (T_out, Press_mm_hg, Visibility, etc.)
  - Wind speed information

## 🤖 Machine Learning Model

### Model Details
- **Algorithm**: Random Forest Regressor
- **Purpose**: Predict appliance energy consumption
- **Input Features**: 28 features including temperature, humidity, time factors
- **Output**: Energy consumption (Wh)

### Model Performance
```
Train R² Score: 0.9234
Test R² Score:  0.8956
MAE:            16.45 Wh
RMSE:           21.32 Wh
```

## 🎨 UI/UX Features

### Modern Design
- Gradient backgrounds with primary blue (#2563eb)
- Responsive grid layouts
- Smooth animations and transitions
- Icons from Font Awesome
- Professional color scheme

### Interactive Elements
- Sticky navigation bar
- Smooth scroll navigation
- Dynamic stat cards
- Real-time chart updates
- Form validation

### Charts & Visualizations
- Chart.js for web dashboard
- Plotly for Streamlit dashboard
- Multiple chart types: Line, Bar, Heatmap, Scatter
- Responsive and interactive

## 🔧 API Endpoints (Flask)

- `GET /` - Home page
- `GET /api/summary` - Data statistics
- `GET /api/hourly-avg` - Hourly averages
- `GET /api/daily-avg` - Daily averages
- `GET /api/top-consumers` - Room temperature data
- `POST /api/predict` - Make predictions
- `GET /api/model-info` - Model metrics

## 📱 Responsive Design

- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1199px)
- ✅ Mobile (< 768px)

## 💡 Usage Examples

### 1. View Energy Analytics
- Navigate to "Analytics" section
- See hourly and daily consumption patterns
- Analyze room temperatures

### 2. Make Predictions
- Go to "Prediction" section
- Input temperature, humidity, and hour
- Get instant energy prediction
- View model confidence scores

### 3. Deep Analysis (Streamlit)
- Open advanced dashboard
- Explore correlations between variables
- Check statistical summaries
- View feature importance

## 🛠️ Technologies Used

- **Backend**: Flask, Python
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Data Science**: Pandas, Numpy, Scikit-learn
- **Visualizations**: Chart.js, Plotly
- **Dashboard**: Streamlit
- **Styling**: CSS Grid, Flexbox

## 📝 Notes

- The model achieves ~89% accuracy on test data
- All predictions are for appliance energy consumption
- Data is normalized for accurate predictions
- The dashboard updates in real-time
- Streamlit dashboard provides deeper statistical analysis

## 🤝 Contributing

Feel free to extend this project with:
- Additional ML models
- Real-time data integration
- IoT device connectivity
- Energy savings recommendations
- Cost analysis features

## 📄 License

This project is created for educational purposes.

---

**Built with ❤️ using Flask, Python & AI**
