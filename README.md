# Resale AI Store Bot

A safe, semi-autonomous reselling store assistant with:

- Trend-to-listing product discovery
- Draft listing generation
- Customer intake and priority classification
- Conversation memory
- Auto follow-ups
- Message archive
- Marketing intelligence and safe free promotion recommendations
- Streamlit owner dashboard
- FastAPI webhook/backend
- SQLite database for local development

## Safety defaults

The system is designed to assist, not replace owner approval for risky actions.

```python
AUTO_BUY = False
AUTO_PUBLISH = False
AUTO_REFUND = False
AUTO_ACCEPT_RETURNS = False
AUTO_SEND_MONEY = False
AUTO_POST_EXTERNAL_COMMUNITIES = False
REQUIRE_HUMAN_APPROVAL = True
REQUIRE_APPROVAL_FOR_PAID_ADS = True
```

## Quick start

```bash
cd resale_ai_store_bot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python scripts/init_db.py
uvicorn backend.main:app --reload
```

In a second terminal:

```bash
streamlit run app/dashboard.py
```

## Environment variables

Copy `.env.example` to `.env` and fill in platform/API keys later.
The app runs locally without keys using demo data and mock services.

## Important

Before connecting to real marketplaces or social channels, review each platform's API terms, listing policies, messaging rules, and advertising rules.
