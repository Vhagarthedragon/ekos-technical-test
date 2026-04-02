# Architecture

## Overview

Two AI agents built for dental and medical clinics using ClinicDesk practice management software:

- **Support Agent** (Track A): conversational support for clinic staff — answers software questions, walks through multi-step procedures, escalates to a human when needed.
- **Sales Agent** (Track B): given a clinic name or URL, researches the prospect online, scores their fit for ClinicDesk, and drafts a personalized outreach email. Drafts require human approval before sending.

## System Diagram

```
┌───────────────────────────────────────────────────────┐
│                  Vue 3 Frontend (Vercel)               │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │ Support Chat │  │Sales Dashboard│  │Admin Dashboard│ │
│  │ - Sessions   │  │ - Research   │  │ - Overview  │  │
│  │ - Chat UI    │  │ - Fit score  │  │ - Sessions  │  │
│  │ - Escalation │  │ - Approve    │  │ - Escalations│ │
│  └──────┬───────┘  └──────┬───────┘  │ - Knowledge │  │
│         │                │          └──────┬──────┘  │
└─────────┼────────────────┼─────────────────┼──────────┘
          │ REST           │ REST            │ REST
┌─────────┼────────────────┼─────────────────┼──────────┐
│         ▼                ▼                 ▼  FastAPI  │
│  ┌─────────────────────────────────────────────────┐   │
│  │                 Presentation Layer               │   │
│  │   /api/support/*   /api/sales/*   /api/admin/*  │   │
│  └──────────────────────┬──────────────────────────┘   │
│                 │                              │
│  ┌──────────────▼───────────────────────────┐  │
│  │            Application Layer             │  │
│  │  ┌─────────────────┐  ┌───────────────┐  │  │
│  │  │  support_agent  │  │  sales_agent  │  │  │
│  │  │  Claude Haiku   │  │  Claude Sonnet│  │  │
│  │  │  + KB search    │  │  + Tavily     │  │  │
│  │  └─────────────────┘  └───────────────┘  │  │
│  └──────────────┬───────────────────────────┘  │
│                 │                              │
│  ┌──────────────▼───────────────────────────┐  │
│  │          Infrastructure Layer            │  │
│  │   asyncpg pool  │  Anthropic SDK         │  │
│  │   Tavily client │  pydantic-settings     │  │
│  └──────────────┬───────────────────────────┘  │
└─────────────────┼──────────────────────────────┘
                  │
        ┌─────────▼──────────┐
        │  Supabase Postgres  │
        │  knowledge_articles │
        │  support_sessions   │
        │  support_messages   │
        │  prospects          │
        │  outreach_drafts    │
        └─────────────────────┘
```

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 + Vite |
| Backend | FastAPI + Python 3.12 |
| Database | PostgreSQL (Supabase) |
| AI | Anthropic Claude (Haiku for support, Sonnet for sales) |
| Web research | Tavily API |
| Frontend hosting | Vercel |
| Backend hosting | Render |

## Layer responsibilities

**Domain** — plain dataclasses, no external dependencies. Entities: `Article`, `SupportSession`, `Message`, `Prospect`, `OutreachDraft`.

**Application** — agent logic lives here. `support_agent.py` and `sales_agent.py` call Claude and the database. No FastAPI imports.

**Infrastructure** — `config.py` (Pydantic Settings reading `.env`), `database.py` (asyncpg connection pool).

**Presentation** — FastAPI routers that validate input with Pydantic, call application functions, and return JSON.

## Key design decisions

**Two models, two jobs** — Support uses `claude-3-5-haiku` (fast, cheap, conversational). Sales uses `claude-3-5-sonnet` (better reasoning for multi-step research + writing). Using Haiku everywhere would save cost but hurt the quality of the outreach emails.

**Human-in-the-loop for sales** — Drafts are stored with `approved=FALSE`. The frontend shows a review UI before any email can be sent. This is intentional: AI-drafted outreach should never go out without a human reading it first.

**Full-text search over embeddings** — The knowledge base is structured with titled, categorized articles. PostgreSQL `tsvector` with a GIN index is fast, zero-dependency, and more than sufficient at this scale. Vector search would be the upgrade path for unstructured documents.

**Agentic loop in Python** — Both agents run a `while True` tool-calling loop instead of a single-shot prompt. This lets Claude decide how many searches to run, chain reasoning across turns, and stop when it has enough confidence. The loop exits on `end_turn` or when no tool calls are made.
