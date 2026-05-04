# Cloud Deployment Guide

This guide explains how to run the AI Reselling Store Bot 24/7 in the cloud.

## Recommended simple cloud options

### Option A: Docker VPS
Use this on a basic cloud server from providers like:
- DigitalOcean
- AWS Lightsail
- Google Cloud VM
- Azure VM
- Hetzner
- Linode

### Option B: Render / Railway / Fly.io
Good for simpler web deployment, but you may need separate services for:
- Backend API
- Dashboard
- Scheduler/worker
- Database

## Safe default automation settings

Keep these values in `.env` while testing:

```env
REQUIRE_HUMAN_APPROVAL=true
AUTO_BUY=false
AUTO_PUBLISH=false
AUTO_REFUND=false
AUTO_POST_EXTERNAL_COMMUNITIES=false
REQUIRE_APPROVAL_FOR_PAID_ADS=true
```

## Files added for deployment

```text
Dockerfile
docker-compose.yml
scripts/start_bot.sh
scripts/start_bot.bat
scripts/deploy_cloud.sh
scripts/deploy_cloud.ps1
.env.example
```

## Local one-click startup

Mac/Linux:

```bash
chmod +x scripts/start_bot.sh
./scripts/start_bot.sh
```

Windows:

```bat
scripts\start_bot.bat
```

## Cloud one-click deployment on a VPS

1. Upload this project folder to your cloud server.
2. SSH into the server.
3. Run:

```bash
chmod +x scripts/deploy_cloud.sh
./scripts/deploy_cloud.sh
```

This will:
- Install Docker if needed
- Build the app containers
- Start backend, dashboard, and scheduler services
- Configure restart policies so the bot comes back online after reboot

## Service URLs

After deployment:

```text
Backend API: http://YOUR_SERVER_IP:8000
Dashboard:   http://YOUR_SERVER_IP:8501
```

## Important production note

For real production use, put the app behind:
- HTTPS
- Login/authentication
- Firewall rules
- Backups
- Secure secrets management

Do not expose customer data publicly.
