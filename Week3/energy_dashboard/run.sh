#!/bin/bash

# Energy Dashboard Startup Script for Linux/Mac

echo ""
echo "===================================="
echo "   Energy Consumption Dashboard"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "[1/3] Checking dependencies..."
if pip3 list | grep -i flask > /dev/null; then
    echo "All packages are already installed!"
else
    echo "[2/3] Installing required packages..."
    pip3 install -r requirements.txt
    echo "Packages installed successfully!"
fi

echo ""
echo "[3/3] Starting Energy Dashboard..."
echo ""
echo "Available options:"
echo ""
echo "Option 1: Run Flask Web App (HTML/CSS/JS Dashboard)"
echo "  Command: python3 app.py"
echo "  URL: http://localhost:5000"
echo ""
echo "Option 2: Run Streamlit Dashboard (Advanced Analytics)"
echo "  Command: streamlit run dashboard.py"
echo "  URL: http://localhost:8501"
echo ""
echo "Option 3: Run Enhanced Flask App (with better error handling)"
echo "  Command: python3 app_enhanced.py"
echo "  URL: http://localhost:5000"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "Starting Flask Web App..."
        python3 app.py
        ;;
    2)
        echo "Starting Streamlit Dashboard..."
        streamlit run dashboard.py
        ;;
    3)
        echo "Starting Enhanced Flask App..."
        python3 app_enhanced.py
        ;;
    *)
        echo "Invalid choice!"
        exit 1
        ;;
esac
