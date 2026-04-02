# Setup

## Requirements

- Python 3.12 (`uv` recommended for version management)
- Node.js 18+
- Supabase project (free tier)
- Anthropic API key — [console.anthropic.com](https://console.anthropic.com)
- Tavily API key — [tavily.com](https://tavily.com) (free: 1,000 searches/month)

---

## Local development

### 1. Backend

```bash
cd backend

# Create virtualenv with Python 3.12
uv venv --python 3.12 .venv
uv pip install --python .venv/Scripts/python.exe -r requirements.txt

# Configure environment
cp .env.example .env
# Fill in: ANTHROPIC_API_KEY, DATABASE_URL, TAVILY_API_KEY, APP_SECRET_KEY

# Run migrations (creates tables + seeds knowledge base)
.venv/Scripts/python.exe migrations/migrate.py

# Start dev server
.venv/Scripts/uvicorn.exe main:app --reload --port 8000
```

API: `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

### 2. Frontend

```bash
cd frontend
npm install

cp .env.example .env
# VITE_API_URL=http://localhost:8000/api  (already set in .env.example)

npm run dev
```

UI: `http://localhost:5173`

---

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Claude API key |
| `DATABASE_URL` | Yes | Supabase Session Pooler URL |
| `TAVILY_API_KEY` | Yes | Sales Agent web search |
| `APP_SECRET_KEY` | Yes | Random 32-byte hex string |
| `APP_ENV` | No | `development` (default) or `production` |
| `FRONTEND_URL` | No | Frontend URL for CORS allowlist |

**Getting the Supabase URL:**  
Supabase dashboard → Connect → Session pooler → copy the connection string.  
Format: `postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres`

---

## Deployment (Render)

Both services are defined in `render.yaml`. Render picks them up automatically on first connect.

### Manual setup

**Backend — Web Service**

| Setting | Value |
|---------|-------|
| Root directory | `backend` |
| Build command | `pip install -r requirements.txt` |
| Start command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Python version | `3.12.0` (set as env var `PYTHON_VERSION`) |

Environment variables to add in Render dashboard:
```
ANTHROPIC_API_KEY=...
DATABASE_URL=...
TAVILY_API_KEY=...
APP_SECRET_KEY=...
APP_ENV=production
FRONTEND_URL=https://your-frontend.onrender.com
```

**Frontend — Static Site**

| Setting | Value |
|---------|-------|
| Root directory | `frontend` |
| Build command | `npm install && npm run build` |
| Publish directory | `dist` |

Environment variable:
```
VITE_API_URL=https://your-backend.onrender.com/api
```

### render.yaml (infrastructure as code)

The `render.yaml` in the repo root defines both services. Connecting the repo to Render and clicking "Apply" provisions everything automatically.

---

## Notes on free tier

- **Render free tier** spins down after 15 minutes of inactivity. The first request after a cold start takes ~30 seconds. Expected for a demo deployment.
- **Supabase free tier** pauses after 7 days of inactivity. Resume from the Supabase dashboard if needed.
- **Tavily free tier** allows 1,000 searches/month. A full single-clinic research uses 2–4; a city scan uses 1.
