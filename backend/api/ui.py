import json
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import incidents as svc

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    rows = await svc.list_incidents(db)
    return templates.TemplateResponse("index.html", {"request": request, "title": "Incident Triage Agent", "incidents": rows, "loads": json.loads})

@router.post("/ui/incidents")
async def ui_create(title: str = Form(...), symptoms: str = Form(...), service: str = Form("api"), db: AsyncSession = Depends(get_db)):
    await svc.triage(db, title, symptoms, service)
    return RedirectResponse("/", status_code=303)

@router.post("/ui/incidents/{incident_id}/resolve")
async def ui_resolve(incident_id: str, db: AsyncSession = Depends(get_db)):
    await svc.resolve(db, incident_id)
    return RedirectResponse("/", status_code=303)
