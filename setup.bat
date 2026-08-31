@echo off
echo ========================================
echo City Vantage AI - Environment Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo During installation, make sure to check:
    echo "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Check if pip is available
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo [OK] pip is available
echo.

REM Install dependencies
echo [INFO] Installing dependencies...
echo This may take a few minutes...
echo.

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo ========================================
echo [SUCCESS] Setup complete!
echo ========================================
echo.
echo To run the application:
echo   streamlit run app.py
echo.
echo Or use: run.bat
echo.
echo To run tests:
echo   pytest tests/ -v
echo.
pause
