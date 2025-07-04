from fastapi import FastAPI
from app.api import admin, agents

app = FastAPI()

app.include_router(agents.router, prefix="", tags=["Agents"])
app.include_router(admin.router, prefix="", tags=["Readings"])