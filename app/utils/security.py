import secrets
from app.core.config import settings
from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Agent
import os

def generate_api_key(length: int = 16) -> str:
    return secrets.token_hex(length)

def get_current_agent(api_key: str = Header(...), db: Session = Depends(get_db)) -> Agent:
    agent = db.query(Agent).filter(Agent.api_key == api_key).first()
    if not agent:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return agent

def verify_agent_token(api_key: str = Header(...), db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.api_key == api_key).first()
    if not agent:
        raise HTTPException(status_code=401, detail="Invalid API key")

def verify_admin_token(x_token: str = Header(...)):
    expected_token = settings.ADMIN_API_KEY
    if x_token != expected_token:
        raise HTTPException(status_code=403, detail="Admin access required")