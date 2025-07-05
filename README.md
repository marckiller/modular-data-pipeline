# modular-data-pipeline

`modular-data-pipeline` is a modular backend system for collecting, storing, and sharing data from autonomous agents.

It acts as a central data hub — a backend platform that receives and stores time-stamped readings from multiple external agents.  
Agents are lightweight programs (e.g., web data collectors or sensors) that fetch data from various sources and send it to this backend using a REST API.

If you're starting from scratch, it's easy to begin with the companion project [`agentkit`](https://github.com/marckiller/agentkit),  
which provides a minimal SDK to build and run agents that integrate directly with this backend.

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

## API Endpoints

### Agent endpoints

- `POST /agent/register` – Register a new agent and receive a token
- `POST /agent/readings` – Submit data using token
- `GET /agent/ping` – Heartbeat mechanism

### Admin endpoints

- `GET /admin/agents` – List all agents
- `GET /admin/readings` – Access all readings
- (Authentication via admin token required — the token must match `ADMIN_API_KEY` from the `.env` file)

## Running

First, create a `.env` file in the root directory with your configuration. Example:

```
DATABASE_URL=sqlite:///./database.db
ADMIN_API_KEY=abcdef
```

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

## Project Structure

```
app/
├── api/        # FastAPI routers
├── core/       # App config and constants
├── db/         # SQLAlchemy models and Pydantic schemas
├── services/   # Business logic
└── utils/      # Utility functions
tests/          # Pytest unit tests
```

## Development

Planned features:
- Web dashboard for live monitoring
- More flexible agent SDK (`agentkit`)