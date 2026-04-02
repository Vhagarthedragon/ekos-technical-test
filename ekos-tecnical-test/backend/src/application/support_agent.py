"""
Support Agent — Track A

Handles multi-turn conversations for clinic staff using ClinicDesk software.
Uses Claude with tool calling to search the knowledge base and decide when to escalate.
"""
import json
from uuid import UUID

import anthropic
import asyncpg

from ..infrastructure.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

SYSTEM_PROMPT = """You are a helpful support agent for ClinicDesk, a practice management platform \
used by dental and medical clinics. You help front desk staff, office managers, and clinic owners \
with questions about scheduling, billing, insurance, and general software use.

Keep answers concise and practical. Clinic staff are busy — get to the point.

You have access to a knowledge base. Always search it before answering. If you cannot find \
a relevant answer, say so honestly and offer to escalate to a human agent.

When to escalate:
- The user is frustrated or has asked the same thing more than once
- The issue involves account access, data loss, or a billing dispute
- You cannot find a confident answer after searching
"""

tools = [
    {
        "name": "search_knowledge_base",
        "description": "Search ClinicDesk help articles for a given query.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "What to search for"}
            },
            "required": ["query"],
        },
    },
    {
        "name": "escalate_to_human",
        "description": "Flag this session for human follow-up when you cannot resolve the issue.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {"type": "string", "description": "Why escalation is needed"}
            },
            "required": ["reason"],
        },
    },
]


async def _search_articles(pool: asyncpg.Pool, query: str) -> str:
    rows = await pool.fetch(
        """
        SELECT title, content, category
        FROM knowledge_articles
        WHERE to_tsvector('english', title || ' ' || content) @@ plainto_tsquery('english', $1)
        ORDER BY ts_rank(to_tsvector('english', title || ' ' || content), plainto_tsquery('english', $1)) DESC
        LIMIT 3
        """,
        query,
    )
    if not rows:
        return "No articles found."
    results = []
    for row in rows:
        results.append(f"[{row['category'].upper()}] {row['title']}\n{row['content']}")
    return "\n\n---\n\n".join(results)


async def _get_history(pool: asyncpg.Pool, session_id: UUID) -> list[dict]:
    rows = await pool.fetch(
        "SELECT role, content FROM support_messages WHERE session_id = $1 ORDER BY created_at",
        session_id,
    )
    return [{"role": r["role"], "content": r["content"]} for r in rows]


async def _save_message(pool: asyncpg.Pool, session_id: UUID, role: str, content: str):
    await pool.execute(
        "INSERT INTO support_messages (session_id, role, content) VALUES ($1, $2, $3)",
        session_id, role, content,
    )


async def _escalate_session(pool: asyncpg.Pool, session_id: UUID):
    await pool.execute(
        "UPDATE support_sessions SET status = 'escalated', updated_at = NOW() WHERE id = $1",
        session_id,
    )


async def chat(pool: asyncpg.Pool, session_id: UUID, user_message: str) -> dict:
    """
    Process one turn of a support conversation.
    Returns {"reply": str, "escalated": bool}.
    """
    await _save_message(pool, session_id, "user", user_message)

    history = await _get_history(pool, session_id)
    messages = [{"role": m["role"], "content": m["content"]} for m in history]

    escalated = False
    reply = ""

    # Agentic loop: let Claude call tools until it produces a final text response
    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages,
        )

        # Collect any text blocks as the candidate reply
        for block in response.content:
            if hasattr(block, "text"):
                reply = block.text

        if response.stop_reason == "end_turn":
            break

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue

                if block.name == "search_knowledge_base":
                    result = await _search_articles(pool, block.input["query"])
                elif block.name == "escalate_to_human":
                    await _escalate_session(pool, session_id)
                    escalated = True
                    result = "Session flagged for human follow-up."
                else:
                    result = "Unknown tool."

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

            # Feed tool results back and continue the loop
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            break

    if not reply:
        reply = "I'm sorry, I couldn't generate a response. Please try again."

    await _save_message(pool, session_id, "assistant", reply)

    if escalated:
        suffix = "\n\n_I've flagged this conversation for a human agent who will follow up with you._"
        reply += suffix

    return {"reply": reply, "escalated": escalated}
