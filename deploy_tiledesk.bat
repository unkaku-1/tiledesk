@echo off
cd /d "%~dp0"

echo "Stopping and removing existing Tiledesk containers..."
cd docker-compose
docker-compose down --remove-orphans --volumes
docker stop mongo redis >nul 2>nul
docker rm mongo redis >nul 2>nul

echo "Checking if Docker is running..."
docker info >nul 2>nul
if %errorlevel% neq 0 (
    echo "Docker is not running. Please start Docker Desktop and try again."
    pause
    exit /b
)

echo "Starting Tiledesk..."
docker-compose up -d
echo "Tiledesk has been deployed."
pause
