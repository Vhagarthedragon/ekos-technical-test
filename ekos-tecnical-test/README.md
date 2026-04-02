# ClinicDesk AI — Technical Test Submission

Two AI agents built for dental and medical clinics using ClinicDesk — combining **Track A (Customer Support)** and **Track B (Sales & Outreach)**.

**Live demo:** https://ekos-technical-test-1.onrender.com

---

## What's inside

### Support Agent (Track A)
A floating chat widget that embeds in any page — the same way a real product would ship it. Built on a simulated ClinicDesk dashboard to make the use case obvious at a glance.

- Multi-turn conversation with full session history
- RAG over a structured knowledge base (PostgreSQL full-text search + GIN index)
- Escalation to a human agent when confidence is low — enforced at the session level
- Guided product tour on first visit

### Sales Agent (Track B)
Two prospecting modes in one interface:

**Single Clinic** — Deep research on one practice: 2–4 Tavily web searches, ICP fit score (0–100), clinic profile with contact details, and personalized email + WhatsApp drafts. Human approval required before anything is "sent".

**City Scan** *(new)* — Find and score multiple clinics in any city in one shot. Enter a city + specialty, get a scored grid of prospects with reasoning. Each card has a "Full Research →" button to run the deep analysis.

### Admin Dashboard
Overview stats, session browser, escalation queue, and full knowledge base CRUD.

---

## Stack

| | |
|---|---|
| **Backend** | FastAPI · Python 3.12 · asyncpg |
| **Frontend** | Vue 3 · Vite |
| **Database** | PostgreSQL (Supabase free tier) |
| **AI** | Anthropic Claude (`claude-haiku-4-5`) |
| **Web search** | Tavily API (free tier) |
| **Deployment** | Render (backend + frontend static site) |

---

## Project structure

```
ekos-tecnical-test/
├── backend/
│   ├── src/
│   │   ├── domain/          # dataclasses, no dependencies
│   │   ├── application/     # support_agent.py, sales_agent.py
│   │   ├── infrastructure/  # database pool, config
│   │   └── presentation/    # FastAPI routers
│   ├── migrations/          # SQL + migrate.py
│   └── main.py
├── frontend/
│   └── src/
│       ├── views/           # SupportView, SalesView, AdminView
│       ├── composables/     # useTheme.js
│       └── api.js
└── docs/
    ├── ARCHITECTURE.md
    ├── AGENT_DESIGN.md
    ├── API_SPEC.md
    ├── DATABASE.md
    ├── SETUP.md
    └── WRITEUP.md
```

---

## Quick start

```bash
# Backend
cd backend
uv venv --python 3.12 .venv
uv pip install --python .venv/Scripts/python.exe -r requirements.txt
cp .env.example .env   # fill in API keys
.venv/Scripts/python.exe migrations/migrate.py
.venv/Scripts/uvicorn.exe main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm install
cp .env.example .env   # VITE_API_URL=http://localhost:8000/api
npm run dev
```

See [`docs/SETUP.md`](docs/SETUP.md) for full setup and deployment instructions.

---

## Docs

| File | Contents |
|---|---|
| [`docs/WRITEUP.md`](docs/WRITEUP.md) | Design decisions, tradeoffs, and what I'd build next |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | System diagram and layer responsibilities |
| [`docs/AGENT_DESIGN.md`](docs/AGENT_DESIGN.md) | How each agent works internally |
| [`docs/API_SPEC.md`](docs/API_SPEC.md) | All endpoints with request/response shapes |
| [`docs/DATABASE.md`](docs/DATABASE.md) | Schema and indexing decisions |
| [`docs/SETUP.md`](docs/SETUP.md) | Local setup and Render deployment |
