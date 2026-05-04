#!/usr/bin/env bash
set -e

echo "Deploying AI Reselling Store Bot to cloud..."

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found. Installing Docker..."
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker "$USER" || true
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose plugin not found. Please install Docker Compose and rerun this script."
  exit 1
fi

if [ ! -f ".env" ]; then
  echo "Creating .env from .env.example..."
  cp .env.example .env
  echo "Review .env and add real API keys before enabling platform integrations."
fi

mkdir -p data logs

docker compose down || true
docker compose build
docker compose up -d

echo ""
echo "Deployment complete."
echo "Backend API: http://YOUR_SERVER_IP:8000"
echo "Dashboard:   http://YOUR_SERVER_IP:8501"
echo ""
echo "Check logs with:"
echo "docker compose logs -f"
