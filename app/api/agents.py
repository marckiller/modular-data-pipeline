from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import models, schemas
from app.db.database import get_db

router = APIRouter()

@router.post("/agents", response_model=schemas.AgentResponse)
def create_agent(agent: schemas.AgentCreateRequest, db: Session = Depends(get_db)):
    db_agent = models.Agent(**agent.dict())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@router.get("/agents/{agent_id}", response_model=schemas.AgentResponse)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agent

@router.get("/agents", response_model=list[schemas.AgentResponse])
def list_agents(db: Session = Depends(get_db)):
    agents = db.query(models.Agent).all()
    return agents