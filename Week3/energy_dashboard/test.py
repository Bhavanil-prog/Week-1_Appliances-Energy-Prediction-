"""
Test script to verify the Energy Dashboard setup
"""

import os
import sys

def test_environment():
    """Test Python environment"""
    print("\n" + "="*50)
    print("TESTING PYTHON ENVIRONMENT")
    print("="*50)
    
    print(f"✓ Python Version: {sys.version}")
    print(f"✓ Python Path: {sys.executable}")
    print(f"✓ Current Directory: {os.getcwd()}")

def test_imports():
    """Test required imports"""
    print("\n" + "="*50)
    print("TESTING REQUIRED IMPORTS")
    print("="*50)
    
    packages = {
        'flask': 'Flask',
        'pandas': 'Pandas',
        'numpy': 'Numpy',
        'sklearn': 'Scikit-learn',
        'streamlit': 'Streamlit',
        'plotly': 'Plotly'
    }
    
    missing = []
    
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✓ {name} is installed")
        except ImportError:
            print(f"✗ {name} is NOT installed")
            missing.append(package)
    
    return len(missing) == 0, missing

def test_data_file():
    """Test if data file exists"""
    print("\n" + "="*50)
    print("TESTING DATA FILE")
    print("="*50)
    
    csv_path = '../energydata_complete.csv'
    
    if os.path.exists(csv_path):
        size_mb = os.path.getsize(csv_path) / (1024 * 1024)
        print(f"✓ Data file found: {csv_path}")
        print(f"✓ File size: {size_mb:.2f} MB")
        
        try:
            import pandas as pd
            df = pd.read_csv(csv_path)
            print(f"✓ Data loaded successfully")
            print(f"  - Records: {len(df):,}")
            print(f"  - Columns: {len(df.columns)}")
            return True
        except Exception as e:
            print(f"✗ Error loading data: {str(e)}")
            return False
    else:
        print(f"✗ Data file not found at: {csv_path}")
        print(f"  Current directory: {os.getcwd()}")
        return False

def test_file_structure():
    """Test project file structure"""
    print("\n" + "="*50)
    print("TESTING FILE STRUCTURE")
    print("="*50)
    
    required_files = [
        'app.py',
        'dashboard.py',
        'requirements.txt',
        'templates/index.html',
        'static/css/style.css',
        'static/js/script.js',
        'README.md'
    ]
    
    all_exist = True
    
    for file_path in required_files:
        full_path = os.path.join(os.getcwd(), file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - NOT FOUND")
            all_exist = False
    
    return all_exist

def test_model_training():
    """Test model training"""
    print("\n" + "="*50)
    print("TESTING MODEL TRAINING")
    print("="*50)
    
    try:
        print("Loading data...")
        import pandas as pd
        df = pd.read_csv('../energydata_complete.csv')
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y %H:%M')
        df['hour'] = df['date'].dt.hour
        df['day'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['weekday'] = df['date'].dt.dayofweek
        
        print("✓ Data loaded successfully")
        print(f"  - Shape: {df.shape}")
        
        print("Training model...")
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.metrics import r2_score
        
        feature_cols = [col for col in df.columns if col not in ['date', 'Appliances']]
        X = df[feature_cols].fillna(df[feature_cols].mean())
        y = df['Appliances']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
        model.fit(X_train_scaled, y_train)
        
        print("✓ Model trained successfully")
        
        train_score = model.score(X_train_scaled, y_train)
        test_score = model.score(X_test_scaled, y_test)
        
        print(f"  - Train R² Score: {train_score:.4f}")
        print(f"  - Test R² Score: {test_score:.4f}")
        
        return True
    
    except Exception as e:
        print(f"✗ Error training model: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n")
    print("╔════════════════════════════════════════════════════╗")
    print("║   ENERGY DASHBOARD - SETUP VERIFICATION TEST      ║")
    print("╚════════════════════════════════════════════════════╝")
    
    results = {}
    
    # Test environment
    test_environment()
    
    # Test imports
    imports_ok, missing = test_imports()
    results['imports'] = imports_ok
    
    # Test data file
    data_ok = test_data_file()
    results['data'] = data_ok
    
    # Test file structure
    files_ok = test_file_structure()
    results['files'] = files_ok
    
    # Test model training (only if data and imports are OK)
    model_ok = False
    if data_ok and imports_ok:
        model_ok = test_model_training()
    results['model'] = model_ok
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    all_passed = all(results.values())
    
    print(f"Python Environment: ✓")
    print(f"Imports: {'✓' if results['imports'] else '✗'}")
    print(f"Data File: {'✓' if results['data'] else '✗'}")
    print(f"File Structure: {'✓' if results['files'] else '✗'}")
    print(f"Model Training: {'✓' if results['model'] else '✗'}")
    
    print("\n" + "="*50)
    
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nYou can now run:")
        print("  python app.py")
        print("  or")
        print("  streamlit run dashboard.py")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease fix the issues above and try again.")
        
        if missing:
            print(f"\nMissing packages: {', '.join(missing)}")
            print("Install with: pip install -r requirements.txt")
        
        return 1

if __name__ == '__main__':
    sys.exit(main())
