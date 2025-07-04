import pytest
from app.services.agents_service import (
    ask_for_ping,
    create_agent_in_db,
    add_agent_readings,
    get_agents_last_reading
)
from app.db import models, schemas
from unittest.mock import MagicMock
from fastapi import HTTPException

def test_ask_for_ping():
    db = MagicMock()
    agent = MagicMock()
    result = ask_for_ping(db, agent)
    assert result == {"status": "pong"}

def test_create_agent_in_db():
    db = MagicMock()
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()

    request = schemas.AgentRegisterRequest(name="AgentX", description="test")
    result = create_agent_in_db(request, db)

    assert isinstance(result, models.Agent)
    assert result.api_key is not None
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

def test_add_agent_readings():
    db = MagicMock()
    db.add = MagicMock()
    db.commit = MagicMock()

    reading_request = schemas.ReadingCreateRequest(data={"val": 123})
    agent = MagicMock()
    agent.id = 1

    result = add_agent_readings(reading_request, db, agent)

    assert result == {"status": "reading accepted"}
    db.add.assert_called_once()
    db.commit.assert_called_once()

def test_get_agents_last_reading_found():
    db = MagicMock()
    fake_reading = MagicMock()
    db.query().filter().order_by().first.return_value = fake_reading
    agent = MagicMock()
    agent.id = 1

    schemas.AgentLastReadingResponse.from_orm = MagicMock(return_value="response")

    result = get_agents_last_reading(db, agent)
    assert result == "response"

def test_get_agents_last_reading_not_found():
    db = MagicMock()
    db.query().filter().order_by().first.return_value = None
    agent = MagicMock()
    agent.id = 1

    with pytest.raises(HTTPException) as exc_info:
        get_agents_last_reading(db, agent)

    assert exc_info.value.status_code == 404
