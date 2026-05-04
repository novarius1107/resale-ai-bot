# AI Reselling Store – Quick Start Guide

## Overview
This system helps you:
- Find trending products
- Create listings
- Manage customers
- Automate follow-ups
- Analyze marketing opportunities

## Setup Steps

1. Install Python 3.10+
2. Create virtual environment
3. Install dependencies:
   pip install -r requirements.txt

4. Configure environment:
   Copy .env.example to .env and update values

5. Run backend:
   uvicorn app.main:app --reload

6. Run dashboard:
   streamlit run dashboard/Home.py

## Key Features

### Trend Engine
- Finds trending items
- Generates draft listings

### Customer Engine
- Auto replies
- Categorizes messages
- Assigns priority
- Sends alerts

### Conversation Memory
- Tracks full history
- Improves responses

### Auto Follow-Ups
- Follows up after 24–72 hours
- Stops when customer replies

### Message Archive
- Search all past interactions
- Export data

### Marketing Engine
- Suggests best platforms
- Auto-posts to owned channels
- Recommends campaigns

## Safety Rules (Important)

- No auto buying
- No auto refunds
- No auto publishing
- Always require approval

## Recommended Workflow

1. Review trending items
2. Approve listings
3. Monitor customer messages
4. Respond to alerts
5. Review marketing suggestions

## Next Steps

- Connect Shopify or eBay API
- Enable limited automation
- Scale gradually



## New cloud-ready additions

- `IMPLEMENTATION_GUIDE.md`
- `DEPLOYMENT_GUIDE.md`
- `Dockerfile`
- `docker-compose.yml`
- `scripts/start_bot.sh`
- `scripts/start_bot.bat`
- `scripts/deploy_cloud.sh`
- `scripts/deploy_cloud.ps1`
- `app/integrations/shopify_client.py`
- `app/integrations/ebay_client.py`
\n\n## Mobile Deal Finder added\n\n- `dashboard/pages/07_Mobile_Deal_Finder.py`\n- `app/mobile_deal_finder/`\n- `MOBILE_DEAL_FINDER_GUIDE.md`\n\nThis module uses saved-search links and manual import instead of prohibited scraping.\n