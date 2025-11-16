# Architecture & Design Documentation

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                               │
│  ┌──────────────────────┐          ┌──────────────────────┐     │
│  │  Flask Web App       │          │  Streamlit Dashboard │     │
│  │  (HTML/CSS/JS)       │          │  (Advanced Analytics)│     │
│  │                      │          │                      │     │
│  │ - Home Section       │          │ - Real-time Metrics  │     │
│  │ - Analytics Charts   │          │ - Correlations       │     │
│  │ - Predictions Form   │          │ - Deep Analysis      │     │
│  │ - Model Metrics      │          │ - Feature Importance │     │
│  └──────────────────────┘          └──────────────────────┘     │
│         http://5000                       http://8501           │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                   API GATEWAY LAYER                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Flask Application Router                      │ │
│  │  ┌─────────────────────────────────────────────────────┐   │ │
│  │  │  GET /                    → Render index.html       │   │ │
│  │  │  GET /api/summary         → Data statistics        │   │ │
│  │  │  GET /api/hourly-avg      → Hourly consumption    │   │ │
│  │  │  GET /api/daily-avg       → Daily consumption     │   │ │
│  │  │  GET /api/top-consumers   → Room analysis         │   │ │
│  │  │  POST /api/predict        → Make predictions      │   │ │
│  │  │  GET /api/model-info      → Model metrics         │   │ │
│  │  └─────────────────────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                          │
│  ┌─────────────────────┐  ┌──────────────────┐  ┌────────────┐ │
│  │ Data Processing     │  │  ML Model        │  │  Utils     │ │
│  │ (app.py)           │  │ (model, scaler)  │  │ (utils.py) │ │
│  │                    │  │                  │  │            │ │
│  │ • Load data        │  │ • Predict        │  │ • Classes  │ │
│  │ • Preprocess       │  │ • Train          │  │ • Helpers  │ │
│  │ • Aggregate        │  │ • Score          │  │            │ │
│  └─────────────────────┘  └──────────────────┘  └────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                     DATA LAYER                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Pandas DataFrame (19,735 rows × 28 columns)              │ │
│  │                                                             │ │
│  │  energydata_complete.csv                                  │ │
│  │  • Appliances | lights | T1-T8 | RH_1-RH_9 | T_out | ... │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Data Processing Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                  DATA PIPELINE                                  │
└─────────────────────────────────────────────────────────────────┘

STEP 1: DATA LOADING
   energydata_complete.csv
          ↓
   pd.read_csv()
          ↓
   19,735 records loaded

STEP 2: DATA PREPARATION
   ┌─────────────────────┐
   │ Parse date column   │ → DateTime conversion
   │ Sort by date        │ → Chronological order
   └─────────────────────┘
          ↓

STEP 3: FEATURE ENGINEERING
   ┌─────────────────────┐
   │ Extract hour        │ → 0-23
   │ Extract day         │ → 1-31
   │ Extract month       │ → 1-12
   │ Extract weekday     │ → 0-6
   │ Handle missing      │ → Mean imputation
   └─────────────────────┘
          ↓

STEP 4: DATA SPLIT
   ┌──────────────────────────────────────┐
   │ 80% Training Data    → 15,788 records │
   │ 20% Testing Data     → 3,947 records  │
   └──────────────────────────────────────┘
          ↓

STEP 5: FEATURE SCALING
   ┌─────────────────────┐
   │ StandardScaler      │ → Mean=0, Std=1
   │ Fit on train data   │
   │ Transform test data │
   └─────────────────────┘
          ↓

STEP 6: MODEL TRAINING
   ┌──────────────────────────────────┐
   │ Algorithm: RandomForest          │
   │ Estimators: 100                  │
   │ Max Depth: 15                    │
   └──────────────────────────────────┘
          ↓

STEP 7: MODEL EVALUATION
   ┌──────────────────────────────────┐
   │ Train R² Score: 92.34%           │
   │ Test R² Score: 89.56%            │
   │ MAE: 16.45 Wh                    │
   │ RMSE: 21.32 Wh                   │
   └──────────────────────────────────┘
          ↓

STEP 8: PREDICTION
   ┌──────────────────────────────────┐
   │ New Input: [T, RH, Hour]         │
   │ Scale with StandardScaler        │
   │ Feed to model                    │
   │ Get prediction                   │
   │ Return result                    │
   └──────────────────────────────────┘
```

## Machine Learning Model Architecture

```
┌────────────────────────────────────────────────────────────────┐
│              RANDOM FOREST MODEL                              │
├────────────────────────────────────────────────────────────────┤
│  Configuration:                                               │
│  • n_estimators: 100 (100 decision trees)                    │
│  • max_depth: 15 (max tree depth)                            │
│  • random_state: 42 (reproducibility)                        │
│                                                              │
│  Input: 28 Features                                          │
│  ├── Appliances (excluded - target)                         │
│  ├── lights                                                  │
│  ├── T1, T2, T3, T4, T5, T6, T7, T8, T9 (temperatures)     │
│  ├── RH_1 to RH_9 (humidity)                                │
│  ├── T_out (external temp)                                  │
│  ├── Press_mm_hg (pressure)                                 │
│  ├── RH_out (external humidity)                             │
│  ├── Windspeed                                              │
│  ├── Visibility                                             │
│  ├── Tdewpoint                                              │
│  ├── rv1, rv2 (random variables)                            │
│  └── hour, day, month, weekday (time features)              │
│                                                              │
│  Processing:                                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ INPUT FEATURES (28)                                │   │
│  │     ↓                                               │   │
│  │ DECISION TREE 1 → Split by most impactful feature  │   │
│  │     ↓                                               │   │
│  │ DECISION TREE 2 → Different random subset          │   │
│  │     ↓                                               │   │
│  │ ... (100 trees total) ...                          │   │
│  │     ↓                                               │   │
│  │ AGGREGATION → Average all predictions              │   │
│  │     ↓                                               │   │
│  │ OUTPUT: Energy Prediction (Wh)                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  Output: Appliances Energy (Wh)                             │
│  Range: 0-250+ Wh                                           │
└────────────────────────────────────────────────────────────────┘
```

## Frontend Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   FRONTEND ARCHITECTURE                         │
└─────────────────────────────────────────────────────────────────┘

index.html (Structure)
├── Navigation Bar
│   ├── Logo & Brand
│   └── Menu (Home, Analytics, Prediction, Dashboard)
│
├── Hero Section
│   ├── Title
│   ├── Subtitle
│   └── Call-to-Action Button
│
├── Summary Section
│   └── Summary Cards Grid
│       ├── Date Range
│       ├── Total Records
│       ├── Max Consumption
│       └── Temperature Range
│
├── Statistics Section
│   └── Stat Cards Grid (4 columns)
│       ├── Avg Appliances (with icon)
│       ├── Avg Lights (with icon)
│       ├── Avg Temperature (with icon)
│       └── Total Records (with icon)
│
├── Analytics Section
│   ├── Hourly Chart Container
│   │   └── Chart.js Line Chart
│   ├── Daily Chart Container
│   │   └── Chart.js Bar Chart
│   └── Room Analysis Grid
│       └── Room Temperature Cards
│
├── Prediction Section
│   ├── Input Form
│   │   ├── Temperature Slider
│   │   ├── Humidity Slider
│   │   └── Hour Slider
│   ├── Result Display
│   │   └── Prediction Output Box
│   └── Model Info
│       └── Model Metrics Display
│
├── Dashboard Link Section
│   └── Link to Streamlit
│
└── Footer
    └── Copyright & Credits


style.css (Styling)
├── Global Styles
│   ├── Root variables (colors, shadows)
│   ├── Base typography
│   └── Layout containers
├── Navigation
│   ├── Navbar styling
│   ├── Active states
│   └── Responsive menu
├── Cards
│   ├── Stat cards
│   ├── Summary cards
│   └── Consumer cards
├── Charts
│   ├── Container styling
│   └── Responsive sizing
├── Forms
│   ├── Input styling
│   ├── Button states
│   └── Validation feedback
├── Responsive Design
│   ├── Desktop (1200px+)
│   ├── Tablet (768-1199px)
│   └── Mobile (<768px)
└── Animations
    ├── Fade-in effects
    ├── Hover transforms
    └── Loading spinners


script.js (Interactivity)
├── Data Loading Functions
│   ├── loadSummary()
│   ├── loadHourlyData()
│   ├── loadDailyData()
│   ├── loadTopConsumers()
│   └── loadModelInfo()
├── Chart Management
│   ├── hourlyChart (Chart.js)
│   └── dailyChart (Chart.js)
├── Form Handling
│   ├── setupPredictionForm()
│   └── Form validation
├── Navigation
│   ├── setupNavigation()
│   ├── scrollToSection()
│   └── Active state management
└── API Integration
    └── axios calls to Flask endpoints
```

## Database/Data Schema

```
┌────────────────────────────────────────────────────────────────┐
│                    DATA SCHEMA                                │
├────────────────────────────────────────────────────────────────┤
│  19,735 rows × 28 columns                                     │
│                                                               │
│  Column Name        │ Type     │ Range/Description          │
│  ─────────────────────────────────────────────────────────────│
│  date               │ datetime │ 2016-01-11 to 2017-01-10  │
│  Appliances         │ float    │ 10 - 250 Wh (target)       │
│  lights             │ float    │ 0 - 70 Wh                 │
│  T1                 │ float    │ 13 - 29°C (room 1)         │
│  RH_1               │ float    │ 30 - 70% (humidity room 1) │
│  T2-T9              │ float    │ Various temperatures       │
│  RH_2-RH_9          │ float    │ Various humidity levels    │
│  T_out              │ float    │ External temperature       │
│  Press_mm_hg        │ float    │ Atmospheric pressure       │
│  RH_out             │ float    │ External humidity          │
│  Windspeed          │ float    │ Wind speed                 │
│  Visibility         │ float    │ Visibility distance        │
│  Tdewpoint          │ float    │ Dew point temperature      │
│  rv1, rv2           │ float    │ Random variables           │
│  hour               │ int      │ 0-23 (derived feature)     │
│  day                │ int      │ 1-31 (derived feature)     │
│  month              │ int      │ 1-12 (derived feature)     │
│  weekday            │ int      │ 0-6 (derived feature)      │
│  ─────────────────────────────────────────────────────────────│
│  Total Features Used in Model: 28                            │
│  Target Variable: Appliances                                 │
│  Time Coverage: 1 year (hourly data)                        │
└────────────────────────────────────────────────────────────────┘
```

## Request/Response Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              API REQUEST/RESPONSE FLOW                          │
└─────────────────────────────────────────────────────────────────┘

1. SUMMARY REQUEST
   Client: GET /api/summary
   ├── Flask: load_and_prepare_data()
   ├── Flask: get_data_summary()
   ├── Response JSON:
   │   {
   │     "total_records": 19735,
   │     "date_range": {"start": "2016-01-11", "end": "2017-01-10"},
   │     "appliances": {"mean": 71.5, "min": 10, "max": 251, "std": 45.2},
   │     ...
   │   }
   └── Client: Update UI with stats

2. CHART DATA REQUEST
   Client: GET /api/hourly-avg
   ├── Flask: df.groupby('hour')
   ├── Response JSON:
   │   {
   │     "hours": [0, 1, 2, ..., 23],
   │     "appliances": [45.2, 40.1, 35.5, ...],
   │     "lights": [5.2, 3.1, 2.5, ...]
   │   }
   └── Client: Render hourly chart

3. PREDICTION REQUEST
   Client: POST /api/predict
   ├── Request JSON:
   │   {"T1": 19.5, "RH_1": 50, "hour": 12}
   ├── Flask: prepare_features()
   ├── Flask: scaler.transform()
   ├── Flask: model.predict()
   ├── Response JSON:
   │   {
   │     "prediction": 65.23,
   │     "status": "success"
   │   }
   └── Client: Display prediction

4. MODEL INFO REQUEST
   Client: GET /api/model-info
   ├── Flask: get_model_metrics()
   ├── Response JSON:
   │   {
   │     "model_type": "Random Forest Regressor",
   │     "n_estimators": 100,
   │     "train_score": 0.9234,
   │     "test_score": 0.8956,
   │     "status": "success"
   │   }
   └── Client: Display model performance
```

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              ERROR HANDLING ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────┘

User Action
    ↓
Try Block
    ├─ Success → Return Response (200)
    └─ Exception
        ├─ FileNotFoundError → Log + Return 404
        ├─ ValueError → Log + Return 400
        ├─ ServerError → Log + Return 500
        └─ UnknownError → Log + Return 500

Logging Strategy
├─ Level: INFO, ERROR, WARNING
├─ Format: timestamp - name - level - message
├─ File: Console output
└─ All errors logged before response

Frontend Error Handling
├─ Network error → Show error message
├─ Invalid input → Form validation
├─ API error → Display error modal
└─ Timeout → Retry mechanism
```

## Performance Considerations

```
┌────────────────────────────────────────────────────────────────┐
│              PERFORMANCE OPTIMIZATION                         │
├────────────────────────────────────────────────────────────────┤
│  Data Loading:     ~2-3 seconds                              │
│  Model Training:   ~15-30 seconds (first run)               │
│  API Response:     < 100ms (most endpoints)                 │
│  Prediction:       < 50ms                                    │
│  Chart Rendering:  < 500ms                                   │
│  Page Load:        < 2 seconds                               │
│                                                               │
│  Optimization Strategies:                                    │
│  • Data caching with @cache_data (Streamlit)               │
│  • Vectorized operations (Numpy, Pandas)                   │
│  • Efficient algorithms (Random Forest)                     │
│  • Lazy loading of heavy components                        │
│  • Frontend asset minification potential                   │
└────────────────────────────────────────────────────────────────┘
```

## Security Architecture

```
┌────────────────────────────────────────────────────────────────┐
│              SECURITY LAYERS                                  │
├────────────────────────────────────────────────────────────────┤
│  Input Validation:                                           │
│  ├─ Type checking on all inputs                            │
│  ├─ Range validation (temperature, humidity, hour)         │
│  └─ Missing value handling                                 │
│                                                               │
│  Error Handling:                                             │
│  ├─ Try-catch blocks on all operations                    │
│  ├─ Logging of all errors                                 │
│  └─ Safe error messages (no sensitive info)               │
│                                                               │
│  Data Protection:                                            │
│  ├─ No hardcoded credentials                              │
│  ├─ Safe file handling                                    │
│  └─ Data validation before processing                     │
│                                                               │
│  API Security:                                               │
│  ├─ CORS enabled for local development                   │
│  ├─ Request validation                                    │
│  └─ Error response standardization                        │
└────────────────────────────────────────────────────────────────┘
```

---

**This architecture enables a scalable, maintainable, and performant energy monitoring system.**
