from fastapi import APIRouter
from backend.api import health, incidents, ui
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(incidents.router, prefix="/api/incidents", tags=["incidents"])
api_router.include_router(ui.router, tags=["ui"])
