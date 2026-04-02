from uuid import UUID

import asyncpg
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..application import sales_agent
from ..infrastructure.database import get_pool

router = APIRouter(prefix="/sales", tags=["sales"])


class ResearchRequest(BaseModel):
    clinic_name: str
    website_url: str | None = None


@router.post("/research")
async def research(body: ResearchRequest, pool: asyncpg.Pool = Depends(get_pool)):
    result = await sales_agent.research_and_draft(pool, body.clinic_name, body.website_url)
    return result


@router.get("/prospects")
async def list_prospects(pool: asyncpg.Pool = Depends(get_pool)):
    rows = await pool.fetch(
        "SELECT id, clinic_name, website_url, fit_score, status, created_at FROM prospects ORDER BY created_at DESC"
    )
    return [dict(r) for r in rows]


@router.get("/prospects/{prospect_id}")
async def get_prospect(prospect_id: UUID, pool: asyncpg.Pool = Depends(get_pool)):
    row = await pool.fetchrow("SELECT * FROM prospects WHERE id = $1", prospect_id)
    if not row:
        raise HTTPException(status_code=404, detail="Prospect not found")

    drafts = await pool.fetch(
        "SELECT * FROM outreach_drafts WHERE prospect_id = $1 ORDER BY created_at DESC",
        prospect_id,
    )
    return {**dict(row), "drafts": [dict(d) for d in drafts]}


@router.post("/drafts/{draft_id}/approve")
async def approve_draft(draft_id: UUID, pool: asyncpg.Pool = Depends(get_pool)):
    ok = await sales_agent.approve_draft(pool, draft_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Draft not found")
    return {"approved": True}
