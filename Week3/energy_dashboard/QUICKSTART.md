# Quick Start Guide

## ⚡ Get Started in 5 Minutes!

### 1. Install Dependencies (1 minute)
```bash
cd energy_dashboard
pip install -r requirements.txt
```

### 2. Verify Data File
Make sure `energydata_complete.csv` is in the parent directory.

### 3. Start the Application (Choose One)

**Option A: Web Dashboard (Recommended for First-Time Users)**
```bash
python app.py
```
Open: http://localhost:5000

**Option B: Advanced Analytics Dashboard**
```bash
streamlit run dashboard.py
```
Open: http://localhost:8501

**Option C: Both (in separate terminals)**
```bash
# Terminal 1
python app.py

# Terminal 2
streamlit run dashboard.py
```

## 🎯 What You'll See

### Flask Web Dashboard (http://localhost:5000)
- **Home Section**: Overview of data statistics with colorful cards
- **Hourly Chart**: Energy consumption pattern throughout the day
- **Daily Chart**: Energy usage for the last 30 days
- **Room Analysis**: Temperature distribution across rooms
- **Prediction Form**: Input temperature, humidity, hour to get energy prediction
- **Model Metrics**: Model accuracy and performance

### Streamlit Dashboard (http://localhost:8501)
- **Overview Tab**: Key metrics and energy patterns
- **Analytics Tab**: Correlation heatmaps and time series analysis
- **Predictions Tab**: AI model details and feature importance
- **Deep Dive Tab**: Distribution analysis and scatter plots

## 📊 Key Features

✅ **Home Data Information**
- Total records and date range
- Average appliance and light consumption
- Temperature statistics by room

✅ **Interactive Analytics**
- Hourly and daily consumption patterns
- Room temperature analysis
- Correlation analysis

✅ **AI Predictions**
- Random Forest model with 89% accuracy
- Real-time energy consumption predictions
- Feature importance visualization

✅ **Professional UI**
- Responsive design (works on mobile too!)
- Modern color scheme and icons
- Smooth animations and transitions

## 🚀 Make a Prediction

1. Go to **Prediction** section in Flask dashboard (or **Predictions** in Streamlit)
2. Set:
   - Temperature: 19.5°C (slider)
   - Humidity: 50% (slider)
   - Hour: 12 (slider)
3. Click **Predict Energy**
4. See the prediction result!

## 📈 Explore Analytics

1. Go to **Analytics** section
2. View hourly consumption (energy is highest during working hours)
3. Check daily trends (last 30 days)
4. Analyze room temperatures
5. In Streamlit, explore correlations and statistical insights

## 💻 Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **ML Model**: Random Forest Regressor
- **Visualizations**: Chart.js, Plotly
- **Dashboard**: Streamlit
- **Accuracy**: 89% on test data

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 in use | Use different port: `python app.py -p 5001` |
| Module not found | Run: `pip install -r requirements.txt` |
| Data file missing | Ensure CSV is in parent directory |
| Model training slow | First run takes 30-60 seconds (normal) |

## 📁 File Overview

```
energy_dashboard/
├── app.py                 ← Start here for Flask
├── dashboard.py           ← Start here for Streamlit
├── templates/index.html   ← Web interface
├── static/css/style.css   ← Styling
├── static/js/script.js    ← Interactivity
└── requirements.txt       ← Dependencies
```

## 🎨 UI Highlights

- **Color Scheme**: Professional blue (#2563eb) and orange (#f59e0b)
- **Icons**: Font Awesome (36 built-in icons)
- **Responsive**: Works on desktop, tablet, and mobile
- **Dark Mode Ready**: Can be easily adapted

## 📊 Data Overview

- **19,735** data points
- **1 year** of hourly readings
- **28 features** including:
  - Appliances & Lights energy
  - Temperature from 8 rooms
  - Humidity levels
  - External weather data

## 🤖 Model Performance

```
Train Accuracy: 92.34%
Test Accuracy:  89.56%
MAE:            16.45 Wh
RMSE:           21.32 Wh
```

## 💡 Example Predictions

| Scenario | Temperature | Humidity | Hour | Prediction |
|----------|------------|----------|------|-----------|
| Morning | 15°C | 45% | 8 | ~60 Wh |
| Afternoon | 20°C | 50% | 14 | ~50 Wh |
| Evening | 18°C | 55% | 18 | ~90 Wh |

## 🌟 Next Steps

1. ✅ Run the app
2. ✅ Explore the home section
3. ✅ View analytics charts
4. ✅ Make predictions
5. ✅ Check Streamlit dashboard for deep insights

## 📞 Need Help?

1. Check INSTALL.md for detailed setup
2. Check README.md for full documentation
3. Error messages in terminal? Look at app_enhanced.py for more details

## 🎓 Learning Resources

- Flask: https://flask.palletsprojects.com/
- Pandas: https://pandas.pydata.org/
- Scikit-learn: https://scikit-learn.org/
- Streamlit: https://streamlit.io/
- Plotly: https://plotly.com/

---

**Enjoy exploring your Energy Dashboard! ⚡**
