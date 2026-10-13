from __future__ import annotations
import json, uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.llm import get_llm
from backend.models import Incident

RUNBOOKS = {
    "sev1": ["Page primary + secondary", "Open war room", "Freeze deploys", "Start status page draft"],
    "sev2": ["Page primary", "Check dashboards/logs", "Mitigate if known", "Notify stakeholders"],
    "sev3": ["Create ticket", "Investigate in business hours", "Document findings"],
    "sev4": ["Log for backlog", "No immediate page"],
}

async def triage(session: AsyncSession, title: str, symptoms: str, service: str) -> Incident:
    llm = get_llm()
    result = await llm.complete_json(
        f"Triage incident JSON with severity sev1-sev4 and steps list.\nTitle: {title}\nService: {service}\nSymptoms: {symptoms}",
        system="You are an experienced incident commander.",
    )
    severity = str(result.get("severity") or "sev3").lower()
    if severity not in RUNBOOKS:
        severity = "sev3"
    steps = result.get("steps") or RUNBOOKS[severity]
    inc = Incident(id=uuid.uuid4().hex[:10], title=title, symptoms=symptoms, service=service,
                   severity=severity, runbook_json=json.dumps(steps), status="open")
    session.add(inc); await session.commit(); await session.refresh(inc); return inc

async def list_incidents(session: AsyncSession):
    return list((await session.execute(select(Incident).order_by(Incident.created_at.desc()))).scalars())

async def resolve(session: AsyncSession, incident_id: str) -> Incident:
    inc = await session.get(Incident, incident_id)
    if not inc: raise ValueError("not found")
    inc.status = "resolved"; await session.commit(); await session.refresh(inc); return inc
