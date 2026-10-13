from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.db import Base
def utcnow(): return datetime.utcnow()
class Incident(Base):
    __tablename__ = "incidents"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    title: Mapped[str] = mapped_column(String(240))
    symptoms: Mapped[str] = mapped_column(Text)
    service: Mapped[str] = mapped_column(String(120), default="unknown")
    severity: Mapped[str] = mapped_column(String(16), default="sev3", index=True)
    status: Mapped[str] = mapped_column(String(32), default="open", index=True)
    runbook_json: Mapped[str] = mapped_column(Text, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
