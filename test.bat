@echo off
echo ========================================
echo City Vantage AI - Running Tests
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

REM Check if pytest is installed
python -m pip show pytest >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing pytest...
    python -m pip install pytest
)

echo [INFO] Running all tests...
echo.

python -m pytest tests/ -v

echo.
echo ========================================
if errorlevel 1 (
    echo [FAILED] Some tests failed
) else (
    echo [SUCCESS] All tests passed
)
echo ========================================
echo.

pause
