@echo off
REM Energy Dashboard Startup Script for Windows

echo.
echo ====================================
echo   Energy Consumption Dashboard
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
pip list | find "flask" >nul
if %errorlevel% neq 0 (
    echo [2/3] Installing required packages...
    pip install -r requirements.txt
    echo Packages installed successfully!
) else (
    echo All packages are already installed!
)

echo.
echo [3/3] Starting Energy Dashboard...
echo.
echo Available options:
echo.
echo Option 1: Run Flask Web App (HTML/CSS/JS Dashboard)
echo   Command: python app.py
echo   URL: http://localhost:5000
echo.
echo Option 2: Run Streamlit Dashboard (Advanced Analytics)
echo   Command: streamlit run dashboard.py
echo   URL: http://localhost:8501
echo.
echo Option 3: Run Enhanced Flask App (with better error handling)
echo   Command: python app_enhanced.py
echo   URL: http://localhost:5000
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Starting Flask Web App...
    python app.py
) else if "%choice%"=="2" (
    echo Starting Streamlit Dashboard...
    streamlit run dashboard.py
) else if "%choice%"=="3" (
    echo Starting Enhanced Flask App...
    python app_enhanced.py
) else (
    echo Invalid choice!
    pause
    exit /b 1
)

pause
