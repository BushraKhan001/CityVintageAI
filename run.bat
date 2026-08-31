@echo off
echo ========================================
echo City Vantage AI - Launching Application
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Check if streamlit is installed
python -m pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Streamlit is not installed
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo [INFO] Starting City Vantage AI...
echo.
echo The application will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

streamlit run app.py

pause
