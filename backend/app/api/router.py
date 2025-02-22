from fastapi import APIRouter
from app.api.routes import agent

router = APIRouter()

router.include_router(
    agent.router, tags=["Agent"], prefix="/agent")
