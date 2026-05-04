from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import Base
from db.session import engine
from engines.customer_engine import process_incoming_message
from engines.trend_engine import add_trending_candidate
from engines.marketing_engine import create_marketing_opportunity

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Resale AI Store Bot")

class CustomerMessageIn(BaseModel):
    platform: str = "unknown"
    customer_id: str
    customer_name: str = ""
    thread_id: str | None = None
    order_id: str = ""
    message_text: str

class TrendCandidateIn(BaseModel):
    product_name: str
    category: str = "general"
    avg_sold_price: float
    estimated_cost: float
    source: str = "manual"

class MarketingIn(BaseModel):
    product_name: str
    category: str = "general"
    demand: float = 70
    margin: float = 70
    competition: float = 50
    velocity: float = 60

@app.get("/")
def health():
    return {"status": "ok", "service": "Resale AI Store Bot"}

@app.post("/webhooks/customer-message")
def customer_message(payload: CustomerMessageIn, db: Session = Depends(get_db)):
    return process_incoming_message(db, payload.model_dump())

@app.post("/trend/candidate")
def trend_candidate(payload: TrendCandidateIn, db: Session = Depends(get_db)):
    item = add_trending_candidate(db, **payload.model_dump())
    return {"id": item.id, "status": item.status, "risk_level": item.risk_level, "estimated_profit": item.estimated_profit}

@app.post("/marketing/opportunity")
def marketing(payload: MarketingIn, db: Session = Depends(get_db)):
    opp = create_marketing_opportunity(db, **payload.model_dump())
    return {"id": opp.id, "marketing_score": opp.marketing_score, "auto_action_allowed": opp.auto_action_allowed}
