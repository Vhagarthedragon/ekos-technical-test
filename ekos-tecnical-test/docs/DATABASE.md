# Database

PostgreSQL hosted on Supabase. Migrations are plain SQL files run in order via `migrations/migrate.py`.

## Tables

### `knowledge_articles`
Help articles that the Support Agent searches via full-text search.

| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| title | TEXT | |
| content | TEXT | |
| category | TEXT | `billing`, `scheduling`, `insurance`, `general` |
| tags | TEXT[] | |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

**Index:** GIN on `to_tsvector('english', title || ' ' || content)` — enables fast `@@` full-text queries.  
Managed through the Admin Dashboard (create, delete) without touching the DB directly.

---

### `support_sessions`
One row per chat session.

| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| user_identifier | TEXT | email or name provided at session start |
| status | TEXT | `active` · `resolved` · `escalated` |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

Sessions with `status = 'escalated'` appear in the Admin escalation queue.

---

### `support_messages`
Individual messages within a session.

| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| session_id | UUID | FK → support_sessions |
| role | TEXT | `user` or `assistant` |
| content | TEXT | |
| created_at | TIMESTAMPTZ | |

---

### `prospects`
Clinics researched or found by the Sales Agent (both Single Clinic and City Scan).

| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| clinic_name | TEXT | |
| website_url | TEXT | nullable |
| location | TEXT | nullable, filled by agent |
| specialty | TEXT | `dental` · `medical` · `physio` · etc. |
| staff_size | TEXT | `solo` · `small` · `medium` · `large` · `unknown` |
| fit_score | INTEGER | 0–100, CHECK constraint |
| fit_reasoning | TEXT | 2–3 sentence explanation |
| raw_research | JSONB | contact details + key findings from research |
| status | TEXT | `new` · `researching` · `draft_ready` |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

`raw_research` shape (Single Clinic):
```json
{
  "key_findings": ["Est. 2009", "Active Google reviews", "No online booking"],
  "contact_phone": "+1 305 000 0000",
  "contact_email": "info@clinic.com",
  "contact_address": "123 Main St, Miami FL",
  "website_found": "https://clinic.com"
}
```

City Scan prospects have `raw_research = {}` initially and are updated to `draft_ready` when Full Research is run.

---

### `outreach_drafts`
Outreach drafts tied to a prospect. Require explicit human approval.

| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| prospect_id | UUID | FK → prospects |
| subject | TEXT | email subject |
| body | TEXT | email body, plain text |
| whatsapp_message | TEXT | under 280 chars |
| approved | BOOLEAN | default FALSE |
| approved_at | TIMESTAMPTZ | set when approved |
| created_at | TIMESTAMPTZ | |

`approved` is set to `TRUE` only via `POST /sales/drafts/:id/approve`. This is the human-in-the-loop gate.

---

## Running migrations

```bash
cd backend
python migrations/migrate.py
```

Connects to `DATABASE_URL` from `.env` and runs all `*.sql` files in `migrations/` in alphabetical order:

| File | Purpose |
|------|---------|
| `001_initial.sql` | Creates all tables and GIN index |
| `002_seed_articles.sql` | Seeds 10 knowledge base articles |
| `003_whatsapp_channel.sql` | Adds `whatsapp_message` column to outreach_drafts |

The script is idempotent — already-applied migrations are tracked by filename and skipped on re-run.
