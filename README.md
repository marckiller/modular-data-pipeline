# modular-data-pipeline

A modular backend system for collecting, storing, and processing data from autonomous agents.

## Features

- FastAPI-based API server
- Agent registration and API key issuance
- Authenticated data submission by agents
- PostgreSQL-compatible SQLAlchemy models

## How It Works

1. Agents register via `/agent/register` and receive an API key
2. Agents send data to `/agent/readings` using their API token
3. Admins can access all agents and data via secured `/admin/*` routes
4. Data is stored and exposed using SQLAlchemy models and Pydantic schemas

## Running

Before running the app locally for the first time, initialize the database:

```bash
python app/db/init_db.py
```

```bash
uvicorn app.main:app --reload
```

API docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)

## Testing

```bash
PYTHONPATH=. pytest --cov=app --cov-report=term-missing
```

## Structure

```
app/
  api/        # FastAPI routers
  core/       # config and constants
  db/         # database models and schemas
  services/   # business logic
  utils/      # helper functions
tests/
```

## In Development

- Agent SDK (`agentkit`) to simplify agent creation
- Web-based dashboard for monitoring readings