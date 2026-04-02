from uuid import UUID

import asyncpg
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..infrastructure.database import get_pool

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
async def get_stats(pool: asyncpg.Pool = Depends(get_pool)):
    sessions = await pool.fetchval("SELECT COUNT(*) FROM support_sessions")
    escalations = await pool.fetchval("SELECT COUNT(*) FROM support_sessions WHERE status = 'escalated'")
    prospects = await pool.fetchval("SELECT COUNT(*) FROM prospects")
    drafts_pending = await pool.fetchval("SELECT COUNT(*) FROM outreach_drafts WHERE approved = FALSE")
    articles = await pool.fetchval("SELECT COUNT(*) FROM knowledge_articles")
    return {
        "total_sessions": sessions,
        "escalations": escalations,
        "prospects": prospects,
        "drafts_pending_approval": drafts_pending,
        "knowledge_articles": articles,
    }


@router.get("/sessions")
async def list_sessions(pool: asyncpg.Pool = Depends(get_pool)):
    rows = await pool.fetch(
        """
        SELECT s.id, s.user_identifier, s.status, s.created_at,
               COUNT(m.id) AS message_count
        FROM support_sessions s
        LEFT JOIN support_messages m ON m.session_id = s.id
        GROUP BY s.id
        ORDER BY s.created_at DESC
        """
    )
    return [dict(r) for r in rows]


@router.get("/sessions/{session_id}")
async def get_session(session_id: UUID, pool: asyncpg.Pool = Depends(get_pool)):
    session = await pool.fetchrow("SELECT * FROM support_sessions WHERE id = $1", session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    messages = await pool.fetch(
        "SELECT role, content, created_at FROM support_messages WHERE session_id = $1 ORDER BY created_at",
        session_id,
    )
    return {**dict(session), "messages": [dict(m) for m in messages]}


@router.get("/escalations")
async def list_escalations(pool: asyncpg.Pool = Depends(get_pool)):
    rows = await pool.fetch(
        """
        SELECT s.id, s.user_identifier, s.created_at, s.updated_at,
               COUNT(m.id) AS message_count
        FROM support_sessions s
        LEFT JOIN support_messages m ON m.session_id = s.id
        WHERE s.status = 'escalated'
        GROUP BY s.id
        ORDER BY s.updated_at DESC
        """
    )
    return [dict(r) for r in rows]


@router.get("/articles")
async def list_articles(pool: asyncpg.Pool = Depends(get_pool)):
    rows = await pool.fetch(
        "SELECT id, title, category, tags, created_at FROM knowledge_articles ORDER BY category, title"
    )
    return [dict(r) for r in rows]


class ArticleBody(BaseModel):
    title: str
    content: str
    category: str
    tags: list[str] = []


@router.post("/articles")
async def create_article(body: ArticleBody, pool: asyncpg.Pool = Depends(get_pool)):
    row = await pool.fetchrow(
        "INSERT INTO knowledge_articles (title, content, category, tags) VALUES ($1, $2, $3, $4) RETURNING id",
        body.title, body.content, body.category, body.tags,
    )
    return {"id": str(row["id"])}


@router.delete("/articles/{article_id}")
async def delete_article(article_id: UUID, pool: asyncpg.Pool = Depends(get_pool)):
    await pool.execute("DELETE FROM knowledge_articles WHERE id = $1", article_id)
    return {"deleted": True}
