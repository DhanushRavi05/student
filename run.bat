@echo off
TITLE EduTrack AI - Student Learning Behaviour & Intervention Analytics
COLOR 0B

echo ===============================================================================
echo       EduTrack AI: Student Learning Behaviour & Intervention Analytics
echo                    Higher Education Analytics Platform
echo ===============================================================================
echo.

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.10+ and re-run this script.
    pause
    exit /b 1
)

echo [1/3] Python detected. Verifying dependencies...
pip install -r requirements.txt --quiet

echo [2/3] Starting Academic Portal server on http://127.0.0.1:5000 ...
echo [3/3] Opening browser...

start http://127.0.0.1:5000

echo.
echo ===============================================================================
echo Application is running! Press CTRL+C to stop the server anytime.
echo Access URL: http://127.0.0.1:5000
echo ===============================================================================
echo.

python app.py
pause
