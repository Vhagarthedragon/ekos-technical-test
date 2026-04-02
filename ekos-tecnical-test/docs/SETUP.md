# Setup

## Requirements

- Python 3.12
- Node.js 18+
- A Supabase project (free tier)
- Anthropic API key
- Tavily API key (free tier, 1,000 searches/month)

## Backend

```bash
cd backend

# Create virtualenv with Python 3.12 (using uv)
uv venv --python 3.12 .venv
uv pip install --python .venv/Scripts/python.exe -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your keys

# Run migrations (creates tables + seeds knowledge base)
.venv/Scripts/python.exe migrations/migrate.py

# Start dev server
.venv/Scripts/uvicorn.exe main:app --reload --port 8000
```

API available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

## Frontend

```bash
cd frontend

npm install

# Configure environment
cp .env.example .env
# .env already points to http://localhost:8000/api for local dev

npm run dev
```

UI available at `http://localhost:5173`

## Environment variables

See `backend/.env.example` for all required variables.

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Claude API key |
| `DATABASE_URL` | Yes | Supabase connection string (Session Pooler URL) |
| `TAVILY_API_KEY` | Yes | For Sales Agent web search |
| `APP_SECRET_KEY` | Yes | Random string for signing tokens |
| `FRONTEND_URL` | No | Frontend URL for CORS (default: localhost:3000) |

## Deployment

**Backend → Render**
1. Connect GitHub repo to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `.env`

**Frontend → Vercel**
1. Connect GitHub repo to Vercel
2. Set root directory to `frontend`
3. Add `VITE_API_URL` pointing to your Render backend URL
