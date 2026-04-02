from uuid import UUID

import asyncpg
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..application import support_agent
from ..infrastructure.database import get_pool

router = APIRouter(prefix="/support", tags=["support"])


class StartSessionRequest(BaseModel):
    user_identifier: str


class ChatRequest(BaseModel):
    message: str


@router.post("/sessions")
async def start_session(body: StartSessionRequest, pool: asyncpg.Pool = Depends(get_pool)):
    row = await pool.fetchrow(
        "INSERT INTO support_sessions (user_identifier) VALUES ($1) RETURNING id",
        body.user_identifier,
    )
    return {"session_id": str(row["id"])}


@router.post("/sessions/{session_id}/chat")
async def chat(session_id: UUID, body: ChatRequest, pool: asyncpg.Pool = Depends(get_pool)):
    session = await pool.fetchrow(
        "SELECT id, status FROM support_sessions WHERE id = $1", session_id
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session["status"] == "escalated":
        raise HTTPException(status_code=400, detail="Session has been escalated to a human agent")

    result = await support_agent.chat(pool, session_id, body.message)
    return result


@router.get("/sessions/{session_id}/history")
async def get_history(session_id: UUID, pool: asyncpg.Pool = Depends(get_pool)):
    rows = await pool.fetch(
        "SELECT role, content, created_at FROM support_messages WHERE session_id = $1 ORDER BY created_at",
        session_id,
    )
    return [dict(r) for r in rows]
