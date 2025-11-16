# Installation & Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Windows/Linux/Mac OS

## Step-by-Step Installation

### Step 1: Navigate to Project Directory

```bash
cd "c:\projectss\Edunet Foundation Internship_4weeks\Week3\energy_dashboard"
```

### Step 2: Create Virtual Environment (Optional but Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Pandas (data processing)
- Numpy (numerical computing)
- Scikit-learn (machine learning)
- Streamlit (dashboard framework)
- Plotly (interactive visualizations)

## Running the Application

### Method 1: Using Startup Scripts

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
bash run.sh
```

Then select option 1, 2, or 3 from the menu.

### Method 2: Manual Startup

#### Flask Web App (Recommended for Web UI)

```bash
python app.py
```

Then open your browser and go to: **http://localhost:5000**

#### Streamlit Dashboard (Recommended for Analytics)

```bash
streamlit run dashboard.py
```

Then open your browser and go to: **http://localhost:8501**

#### Enhanced Flask App (with better error handling)

```bash
python app_enhanced.py
```

Then open your browser and go to: **http://localhost:5000**

### Method 3: Run Both Simultaneously

**Terminal 1:**
```bash
python app.py
```

**Terminal 2:**
```bash
streamlit run dashboard.py
```

Then access:
- Flask Dashboard: http://localhost:5000
- Streamlit Dashboard: http://localhost:8501

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
pip install flask
```

### Issue: "Data file not found"

**Solution:**
Make sure `energydata_complete.csv` is in the parent directory:
```
Week3/
├── energydata_complete.csv  ← File should be here
└── energy_dashboard/
```

### Issue: Port 5000 already in use

**Solution:**
The Flask app will automatically try the next available port. Check the terminal output for the actual port.

### Issue: Streamlit not found

**Solution:**
```bash
pip install streamlit plotly
```

## Testing the Application

### Test Data Loading
```python
# test.py
import pandas as pd
df = pd.read_csv('../energydata_complete.csv')
print(f"Loaded {len(df)} records")
print(df.head())
```

Run: `python test.py`

### Test Model Training
```python
# test_model.py
from app import load_and_prepare_data, train_model
load_and_prepare_data()
metrics = train_model()
print(f"Model Metrics: {metrics}")
```

Run: `python test_model.py`

### Test API Endpoints
```bash
# Get summary
curl http://localhost:5000/api/summary

# Get hourly data
curl http://localhost:5000/api/hourly-avg

# Make prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"T1": 19.5, "RH_1": 50, "hour": 12}'
```

## File Structure

```
energy_dashboard/
├── app.py                    # Main Flask application
├── app_enhanced.py           # Enhanced Flask with logging
├── dashboard.py              # Streamlit dashboard
├── utils.py                  # Utility functions
├── config.py                 # Configuration file
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── INSTALL.md               # This file
├── run.bat                  # Windows startup script
├── run.sh                   # Linux/Mac startup script
├── templates/
│   └── index.html           # HTML template
├── static/
│   ├── css/
│   │   └── style.css        # CSS styles
│   ├── js/
│   │   └── script.js        # JavaScript
│   └── images/              # Image assets
```

## Features Checklist

- [x] Home Section with Data Information
- [x] Interactive HTML/CSS/JS Frontend
- [x] Beautiful UI with Icons and Gradients
- [x] Advanced Dashboard (Streamlit)
- [x] Machine Learning Model (Random Forest)
- [x] AI Predictions
- [x] Responsive Design
- [x] Multiple Visualizations
- [x] Error Handling and Logging
- [x] API Endpoints
- [x] Feature Importance Analysis

## Performance Notes

- Initial load may take 30-60 seconds as the model is trained
- Predictions are instant once the model is trained
- Dashboard supports real-time data updates
- Optimized for datasets up to 100K+ records

## Browser Compatibility

- Chrome/Chromium ✅
- Firefox ✅
- Safari ✅
- Edge ✅
- Opera ✅

## System Requirements

- **CPU**: Any modern processor
- **RAM**: Minimum 2GB, recommended 4GB+
- **Disk Space**: ~100MB for dependencies
- **Internet**: Not required after initial setup

## Next Steps

1. Run the application
2. Explore the home section with data statistics
3. View analytics and charts
4. Make predictions using the AI model
5. Check the Streamlit dashboard for advanced analysis

## Support

If you encounter any issues:
1. Check the error message in the terminal
2. Verify all dependencies are installed: `pip list`
3. Ensure data file exists in the correct location
4. Try with the enhanced app for better error messages: `python app_enhanced.py`

---

**Happy Energy Monitoring! ⚡**
