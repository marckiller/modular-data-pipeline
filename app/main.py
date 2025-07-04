from fastapi import FastAPI
from app.api import agents, readings

app = FastAPI()

app.include_router(agents.router, prefix="", tags=["Agents"])
app.include_router(readings.router, prefix="", tags=["Readings"])