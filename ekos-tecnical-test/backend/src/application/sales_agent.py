"""
Sales Agent — Track B

Given a clinic name or URL, the agent researches the prospect online,
scores their fit for ClinicDesk, and drafts outreach across two channels:
  - Email (personalized, 3-4 paragraphs)
  - WhatsApp (short, conversational, under 300 chars)

Human-in-the-loop: drafts are saved with approved=False.
"""
import json
from uuid import UUID

import anthropic
import asyncpg
from tavily import TavilyClient

from ..infrastructure.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
tavily = TavilyClient(api_key=settings.tavily_api_key)

SYSTEM_PROMPT = """You are a sales research assistant for ClinicDesk, a practice management platform \
for dental and medical clinics. Your job is to research a clinic prospect and produce:

1. A fit assessment: score 0–100 and 2-3 sentence reasoning.
   High fit: independent clinic, 1–50 staff, dental or primary care, not on enterprise EMR.

2. An email draft: personalized, sounds human. Reference something specific about the clinic. \
No generic openers like "I hope this finds you well." 3-4 short paragraphs.

3. A WhatsApp message: short and direct, under 280 characters. Conversational tone. \
Reference one specific thing you found. No formal language.

Always search before writing anything.

IMPORTANT: All output must be in English — email, WhatsApp message, reasoning, findings, everything.
"""

tools = [
    {
        "name": "search_web",
        "description": "Search the web for information about a clinic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"],
        },
    }
]


async def _save_prospect(pool: asyncpg.Pool, clinic_name: str, website_url: str | None) -> UUID:
    row = await pool.fetchrow(
        "INSERT INTO prospects (clinic_name, website_url, status) VALUES ($1, $2, 'researching') RETURNING id",
        clinic_name, website_url,
    )
    return row["id"]


async def _update_prospect(pool: asyncpg.Pool, prospect_id: UUID, data: dict):
    await pool.execute(
        """
        UPDATE prospects SET
            location = $2, specialty = $3, staff_size = $4,
            fit_score = $5, fit_reasoning = $6, raw_research = $7,
            status = 'draft_ready', updated_at = NOW()
        WHERE id = $1
        """,
        prospect_id,
        data.get("location"),
        data.get("specialty"),
        data.get("staff_size"),
        data.get("fit_score"),
        data.get("fit_reasoning"),
        json.dumps({
            **data.get("raw_research", {}),
            "contact_phone": data.get("contact_phone"),
            "contact_email": data.get("contact_email"),
            "contact_address": data.get("contact_address"),
            "website_found": data.get("website_found"),
            "key_findings": data.get("key_findings", []),
        }),
    )


async def _save_draft(pool: asyncpg.Pool, prospect_id: UUID, data: dict) -> UUID:
    row = await pool.fetchrow(
        """
        INSERT INTO outreach_drafts (prospect_id, subject, body, whatsapp_message)
        VALUES ($1, $2, $3, $4)
        RETURNING id
        """,
        prospect_id,
        data.get("email_subject", ""),
        data.get("email_body", ""),
        data.get("whatsapp_message", ""),
    )
    return row["id"]


async def research_and_draft(
    pool: asyncpg.Pool,
    clinic_name: str,
    website_url: str | None = None,
) -> dict:
    """Research a clinic and produce email + WhatsApp drafts."""
    prospect_id = await _save_prospect(pool, clinic_name, website_url)

    messages = [
        {
            "role": "user",
            "content": (
                f"Research this clinic and produce outreach drafts for ClinicDesk.\n"
                f"Clinic: {clinic_name}\n"
                f"Website: {website_url or 'unknown — search for it'}\n\n"
                f"Return a JSON object with:\n"
                f"- location: string or null\n"
                f"- specialty: 'dental' | 'medical' | 'both' | null\n"
                f"- staff_size: 'solo' | 'small' | 'medium' | null\n"
                f"- fit_score: 0-100\n"
                f"- fit_reasoning: 2-3 sentences\n"
                f"- key_findings: array of 3-5 short strings (facts found during research)\n"
                f"- contact_phone: string or null\n"
                f"- contact_email: string or null\n"
                f"- contact_address: string or null\n"
                f"- website_found: string or null (actual URL if discovered)\n"
                f"- email_subject: string\n"
                f"- email_body: plain text, 3-4 paragraphs\n"
                f"- whatsapp_message: under 280 chars, conversational\n"
                f"- raw_research: object with anything else relevant"
            ),
        }
    ]

    research_data = {}

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages,
        )

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                results = tavily.search(block.input["query"], max_results=3)
                result_text = "\n\n".join(
                    f"{r['title']}\n{r['content']}" for r in results.get("results", [])
                )
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result_text or "No results found.",
                })
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

        elif response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    text = block.text.strip()
                    start = text.find("{")
                    end = text.rfind("}") + 1
                    if start != -1 and end > start:
                        research_data = json.loads(text[start:end])
            break
        else:
            break

    await _update_prospect(pool, prospect_id, research_data)
    draft_id = await _save_draft(pool, prospect_id, research_data)

    return {
        "prospect_id": str(prospect_id),
        "draft_id": str(draft_id),
        "fit_score": research_data.get("fit_score"),
        "fit_reasoning": research_data.get("fit_reasoning"),
        "location": research_data.get("location"),
        "specialty": research_data.get("specialty"),
        "staff_size": research_data.get("staff_size"),
        "key_findings": research_data.get("key_findings", []),
        "contact_phone": research_data.get("contact_phone"),
        "contact_email": research_data.get("contact_email"),
        "contact_address": research_data.get("contact_address"),
        "website_found": research_data.get("website_found") or website_url,
        "email_subject": research_data.get("email_subject"),
        "email_body": research_data.get("email_body"),
        "whatsapp_message": research_data.get("whatsapp_message"),
    }


async def approve_draft(pool: asyncpg.Pool, draft_id: UUID) -> bool:
    result = await pool.execute(
        "UPDATE outreach_drafts SET approved = TRUE, approved_at = NOW() WHERE id = $1",
        draft_id,
    )
    return result == "UPDATE 1"
