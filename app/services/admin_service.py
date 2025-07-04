from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException
from datetime import datetime

def list_all_agents(db: Session) -> list[models.Agent]:
    return db.query(models.Agent).all()

def get_agent_by_id( agent_id: int, db: Session) ->models.Agent | None:
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

def list_readings_for_agent(
    agent_id: int,
    db: Session,
    limit: int | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None) -> list[models.Reading]:

    query = db.query(models.Reading).filter(models.Reading.agent_id == agent_id)

    if from_date:
        query = query.filter(models.Reading.received_at >= from_date)
    if to_date:
        query = query.filter(models.Reading.received_at <= to_date)

    query = query.order_by(models.Reading.received_at.desc())

    if limit:
        query = query.limit(limit)

    return query.all()

def get_latest_reading_for_agent(agent_id: int, db: Session) -> models.Reading | None:
    reading = db.query(models.Reading).filter(models.Reading.agent_id == agent_id).order_by(models.Reading.received_at.desc()).first()
    if not reading:
        raise HTTPException(status_code=404, detail="No readings found for agent")
    return reading

def get_reading_by_id(reading_id: int, db: Session) -> models.Reading | None:
    reading = db.query(models.Reading).filter(models.Reading.id == reading_id).first()
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    return reading