# Database

PostgreSQL hosted on Supabase. Migrations are plain SQL files run in order via `migrations/migrate.py`.

## Tables

### `knowledge_articles`
Help articles that the Support Agent searches.

| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| title | TEXT | |
| content | TEXT | |
| category | TEXT | `billing`, `scheduling`, `insurance`, `general` |
| tags | TEXT[] | |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

**Index**: GIN index on `to_tsvector('english', title || ' ' || content)` for fast full-text search.

---

### `support_sessions`
One row per chat session.

| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| user_identifier | TEXT | email or anonymous ID |
| status | TEXT | `active`, `resolved`, `escalated` |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

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
Clinics researched by the Sales Agent.

| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| clinic_name | TEXT | |
| website_url | TEXT | nullable |
| location | TEXT | nullable, filled by agent |
| specialty | TEXT | `dental`, `medical`, `both` |
| staff_size | TEXT | `solo`, `small`, `medium` |
| fit_score | INTEGER | 0–100, CHECK constraint |
| fit_reasoning | TEXT | 2-3 sentence explanation |
| raw_research | JSONB | key findings from web search |
| status | TEXT | `researching`, `draft_ready`, `approved`, `sent` |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

---

### `outreach_drafts`
Email drafts tied to a prospect. Require explicit approval.

| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| prospect_id | UUID | FK → prospects |
| subject | TEXT | |
| body | TEXT | plain text |
| approved | BOOLEAN | default FALSE |
| approved_at | TIMESTAMPTZ | set when approved |
| sent_at | TIMESTAMPTZ | set when sent (future) |
| created_at | TIMESTAMPTZ | |

## Running migrations

```bash
cd backend
python migrations/migrate.py
```

This connects to `DATABASE_URL` from `.env` and runs all `*.sql` files in `migrations/` in alphabetical order. `001_initial.sql` creates tables. `002_seed_articles.sql` populates the knowledge base.
