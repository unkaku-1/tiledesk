@echo off
echo "Checking if Docker is running..."
docker info >nul 2>nul
if %errorlevel% neq 0 (
    echo "Docker is not running. Please start Docker Desktop and try again."
    pause
    exit /b
)

echo "Starting Tiledesk..."
cd tiledesk-deployment\docker-compose
docker-compose up -d
echo "Tiledesk has been deployed."
pause
