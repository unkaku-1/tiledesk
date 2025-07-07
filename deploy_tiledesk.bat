@echo off
cd /d "%~dp0\docker-compose"

echo "Starting smart deployment script..."
python smart_deploy.py

echo.
echo Deployment process finished.
pause
