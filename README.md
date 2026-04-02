# ClinicDesk AI Agents

Two AI agents for dental and medical clinics using practice management software.

- **Support Agent** — conversational support for clinic staff. Searches a knowledge base, handles multi-turn workflows, and escalates to a human when needed.
- **Sales Agent** — given a clinic name or URL, researches the prospect online, scores their fit for ClinicDesk, and drafts a personalized outreach email. Drafts require human approval before sending.

**Live demo**: _coming soon_

---

## Stack

| | Technology |
|-|-----------|
| Frontend | Vue 3 + Vite |
| Backend | FastAPI + Python 3.12 |
| Database | PostgreSQL (Supabase) |
| AI | Anthropic Claude (Haiku 4.5) |
| Web research | Tavily API |
| Frontend hosting | Vercel |
| Backend hosting | Render |

---

## Quick start

### Requirements
- Python 3.12 (install with `uv`: `uv python install 3.12`)
- Node.js 18+
- Supabase project (free tier)
- Anthropic API key
- Tavily API key (free tier)

### Backend

```bash
cd backend

# Create virtualenv
uv venv --python 3.12 .venv
uv pip install --python .venv/Scripts/python.exe -r requirements.txt

# Configure
cp .env.example .env
# Fill in your keys in .env

# Run migrations + seed knowledge base
.venv/Scripts/python.exe migrations/migrate.py

# Start dev server
.venv/Scripts/uvicorn.exe main:app --reload --port 8000
```

API → `http://localhost:8000`  
Interactive docs → `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

UI → `http://localhost:5173`

---

## Project structure

```
├── backend/
│   ├── src/
│   │   ├── domain/          # Entities (no external deps)
│   │   ├── application/     # Agent logic (support_agent, sales_agent)
│   │   ├── infrastructure/  # DB pool, config
│   │   └── presentation/    # FastAPI routers (support, sales, admin)
│   ├── migrations/          # SQL migrations + seed data
│   └── main.py
├── frontend/
│   └── src/
│       └── views/           # SupportView, SalesView, AdminView
└── docs/
    ├── ARCHITECTURE.md
    ├── AGENT_DESIGN.md
    ├── API_SPEC.md
    ├── DATABASE.md
    ├── SETUP.md
    └── WRITEUP.md
```

---

## Docs

- [Architecture](ekos-tecnical-test/docs/ARCHITECTURE.md)
- [Agent Design](ekos-tecnical-test/docs/AGENT_DESIGN.md)
- [API Reference](ekos-tecnical-test/docs/API_SPEC.md)
- [Database Schema](ekos-tecnical-test/docs/DATABASE.md)
- [Setup & Deploy](ekos-tecnical-test/docs/SETUP.md)
- [Write-up](ekos-tecnical-test/docs/WRITEUP.md)
