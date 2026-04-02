# Architecture

## Overview

Two AI agents for dental and medical clinics on ClinicDesk:

- **Support Agent (Track A):** floating chat widget embedded in the host application — answers software questions, walks through procedures, escalates to a human when needed.
- **Sales Agent (Track B):** researches a clinic prospect online, scores their fit for ClinicDesk (0–100), and drafts personalized outreach. Includes a City Scan mode to bulk-prospect clinics in any city.

Both share a single PostgreSQL database (Supabase) and are deployed on Render.

---

## System diagram

```
┌──────────────────────────────────────────────────────────────┐
│                   Vue 3 Frontend (Render)                    │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────┐  │
│  │  Support Widget │  │   Sales Agent    │  │  Admin     │  │
│  │  (floating,     │  │  Single Clinic   │  │  Dashboard │  │
│  │   embedded UI)  │  │  City Scan       │  │            │  │
│  └────────┬────────┘  └────────┬─────────┘  └─────┬──────┘  │
└───────────┼────────────────────┼─────────────────-┼─────────┘
            │ REST               │ REST              │ REST
┌───────────┼────────────────────┼──────────────────┼──────────┐
│           ▼                    ▼                  ▼  FastAPI  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    Presentation Layer                   │  │
│  │   /api/support/*     /api/sales/*     /api/admin/*      │  │
│  └────────────────────────────┬────────────────────────────┘  │
│                               │                               │
│  ┌────────────────────────────▼────────────────────────────┐  │
│  │                   Application Layer                     │  │
│  │  ┌──────────────────────┐  ┌────────────────────────┐   │  │
│  │  │    support_agent     │  │      sales_agent       │   │  │
│  │  │  claude-haiku-4-5    │  │  claude-haiku-4-5      │   │  │
│  │  │  tools:              │  │  tools:                │   │  │
│  │  │  - search_knowledge  │  │  - search_web (Tavily) │   │  │
│  │  │  - escalate_to_human │  │  + find_in_city()      │   │  │
│  │  └──────────────────────┘  └────────────────────────┘   │  │
│  └────────────────────────────┬────────────────────────────┘  │
│                               │                               │
│  ┌────────────────────────────▼────────────────────────────┐  │
│  │                  Infrastructure Layer                   │  │
│  │      asyncpg pool  │  Anthropic SDK  │  Tavily client   │  │
│  │      pydantic-settings  │  config.py                    │  │
│  └────────────────────────────┬────────────────────────────┘  │
└───────────────────────────────┼───────────────────────────────┘
                                │
                    ┌───────────▼──────────┐
                    │   Supabase Postgres   │
                    │  knowledge_articles   │
                    │  support_sessions     │
                    │  support_messages     │
                    │  prospects            │
                    │  outreach_drafts      │
                    └───────────────────────┘
```

---

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 + Vite |
| Backend | FastAPI + Python 3.12 |
| Database | PostgreSQL (Supabase free tier) |
| AI | Anthropic Claude `claude-haiku-4-5-20251001` |
| Web research | Tavily API (free tier, 1,000 searches/month) |
| Hosting | Render (backend web service + static site) |

---

## Layer responsibilities

**Domain** (`src/domain/`) — plain dataclasses, no external imports. Entities: `Article`, `SupportSession`, `Message`, `Prospect`, `OutreachDraft`.

**Application** (`src/application/`) — all agent logic. `support_agent.py` and `sales_agent.py` import `anthropic`, `asyncpg`, and `tavily`. They do not import `fastapi`.

**Infrastructure** (`src/infrastructure/`) — `config.py` loads `.env` via Pydantic Settings; `database.py` manages the asyncpg connection pool.

**Presentation** (`src/presentation/`) — FastAPI routers. Validate input with Pydantic, call application functions, return JSON. No Claude or Tavily imports.

---

## Key design decisions

**Embedded widget, not a standalone page.** The Support view renders full-screen and simulates a ClinicDesk dashboard with the chat widget floating in the corner — matching how the feature would ship inside the real product. The Vue router skips the app shell for this route.

**City Scan as a single-call operation.** `find_in_city()` runs one Tavily search and one Claude call — no agentic loop. It extracts and scores up to 10 clinics from the raw search snippets. Speed matters here: 15 seconds for a full batch is acceptable; 15 seconds per clinic is not.

**Human-in-the-loop enforced at the database layer.** Drafts are inserted with `approved=FALSE`. The only way to flip it is via `POST /sales/drafts/:id/approve`. Nothing else in the system reads this field — but the constraint is auditable and real.

**Full-text search for the knowledge base.** `tsvector`/`tsquery` with a GIN index covers the structured, titled-article shape of support content. Requires no external service. The honest tradeoff is that semantic similarity (synonyms, paraphrases) requires `pgvector` — documented as the clear next step.

**Agentic tool loop.** Both agents run `while True` until `stop_reason == "end_turn"`. This lets Claude adapt its search strategy — search twice on ambiguous questions, once on simple ones. Single-shot prompts can't do this.
