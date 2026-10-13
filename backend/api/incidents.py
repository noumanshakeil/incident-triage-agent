import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import incidents as svc

class CreateIn(BaseModel):
    title: str = Field(min_length=3)
    symptoms: str = Field(min_length=3)
    service: str = "api"

router = APIRouter()

@router.get("")
async def list_incidents(db: AsyncSession = Depends(get_db)):
    rows = await svc.list_incidents(db)
    return {"incidents": [{"id": i.id, "title": i.title, "service": i.service, "severity": i.severity, "status": i.status, "runbook": json.loads(i.runbook_json or "[]")} for i in rows]}

@router.post("")
async def create(payload: CreateIn, db: AsyncSession = Depends(get_db)):
    i = await svc.triage(db, payload.title, payload.symptoms, payload.service)
    return {"id": i.id, "severity": i.severity, "runbook": json.loads(i.runbook_json)}

@router.post("/{incident_id}/resolve")
async def resolve(incident_id: str, db: AsyncSession = Depends(get_db)):
    try:
        i = await svc.resolve(db, incident_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    return {"id": i.id, "status": i.status}
