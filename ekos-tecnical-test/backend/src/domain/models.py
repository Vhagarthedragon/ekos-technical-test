from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Article:
    id: UUID
    title: str
    content: str
    category: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class SupportSession:
    id: UUID
    user_identifier: str
    status: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Message:
    id: UUID
    session_id: UUID
    role: str  # 'user' | 'assistant'
    content: str
    created_at: datetime


@dataclass
class Prospect:
    id: UUID
    clinic_name: str
    status: str
    created_at: datetime
    updated_at: datetime
    website_url: Optional[str] = None
    location: Optional[str] = None
    specialty: Optional[str] = None
    staff_size: Optional[str] = None
    fit_score: Optional[int] = None
    fit_reasoning: Optional[str] = None
    raw_research: dict = field(default_factory=dict)


@dataclass
class OutreachDraft:
    id: UUID
    prospect_id: UUID
    subject: str
    body: str
    approved: bool
    created_at: datetime
    approved_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
