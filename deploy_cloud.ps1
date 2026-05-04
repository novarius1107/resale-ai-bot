Write-Host "Deploying AI Reselling Store Bot with Docker..."

if (!(Test-Path ".env")) {
  Write-Host "Creating .env from .env.example..."
  Copy-Item ".env.example" ".env"
}

if (!(Test-Path "data")) { New-Item -ItemType Directory -Path "data" | Out-Null }
if (!(Test-Path "logs")) { New-Item -ItemType Directory -Path "logs" | Out-Null }

docker compose down
docker compose build
docker compose up -d

Write-Host ""
Write-Host "Deployment complete."
Write-Host "Backend API: http://YOUR_SERVER_IP:8000"
Write-Host "Dashboard:   http://YOUR_SERVER_IP:8501"
Write-Host "Check logs with: docker compose logs -f"
