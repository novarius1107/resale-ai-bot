# AI Reselling Store Bot – Full Implementation Guide

## 1. Install locally first

```bash
./scripts/start_bot.sh
```

Or on Windows:

```bat
scripts\start_bot.bat
```

Open:

```text
Backend:   http://127.0.0.1:8000
Dashboard: http://127.0.0.1:8501
```

## 2. Configure `.env`

Copy:

```bash
cp .env.example .env
```

Add API keys only after local testing.

## 3. Connect Shopify

1. Create a Shopify custom app.
2. Grant Admin API permissions for products/inventory.
3. Copy the Admin API access token.
4. Fill in:

```env
SHOPIFY_STORE_DOMAIN=your-store.myshopify.com
SHOPIFY_ADMIN_ACCESS_TOKEN=your_token
SHOPIFY_API_VERSION=2026-01
```

The template creates **draft products** unless `AUTO_PUBLISH=true`.

## 4. Connect eBay

1. Create an eBay developer account.
2. Create sandbox credentials first.
3. Complete OAuth and generate a refresh token.
4. Fill in:

```env
EBAY_ENV=sandbox
EBAY_CLIENT_ID=your_client_id
EBAY_CLIENT_SECRET=your_client_secret
EBAY_REFRESH_TOKEN=your_refresh_token
EBAY_MARKETPLACE_ID=EBAY_US
```

The template saves inventory draft records and intentionally avoids auto-publishing offers.

## 5. Deploy to cloud

On a VPS:

```bash
./scripts/deploy_cloud.sh
```

The bot will run with Docker and restart automatically.

## 6. 24/7 operations checklist

Before going live:

- Turn on server firewall
- Use HTTPS
- Add authentication to the dashboard
- Back up the database
- Keep approval gates enabled
- Test all customer-message auto replies
- Verify platform policy compliance

## 7. Automation levels

Recommended starting settings:

```env
AUTO_REPLY_FIRST_MESSAGE=true
AUTO_FOLLOW_UP=true
AUTO_OPTIMIZE_LISTINGS=true
AUTO_BUY=false
AUTO_PUBLISH=false
AUTO_REFUND=false
AUTO_POST_EXTERNAL_COMMUNITIES=false
REQUIRE_HUMAN_APPROVAL=true
```

## 8. What still requires your approval

- Buying inventory
- Publishing listings
- Refunds
- Returns
- Paid ads
- Posting in external communities
- Customer disputes
- Any restricted or high-risk product

## 9. Suggested first live test

1. Add one test product.
2. Generate a draft listing.
3. Send it to Shopify as a draft.
4. Simulate a customer question.
5. Confirm the message archive stores the conversation.
6. Confirm high-priority alerts appear.
7. Run a marketing recommendation scan.
\n\n## Mobile Deal Finder added\n\n- `dashboard/pages/07_Mobile_Deal_Finder.py`\n- `app/mobile_deal_finder/`\n- `MOBILE_DEAL_FINDER_GUIDE.md`\n\nThis module uses saved-search links and manual import instead of prohibited scraping.\n