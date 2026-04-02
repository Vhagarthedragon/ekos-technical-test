# API Reference

Base URL (local): `http://localhost:8000/api`  
Interactive docs: `http://localhost:8000/docs`

---

## Support Agent

### POST /support/sessions
Create a new chat session.

**Body**
```json
{ "user_identifier": "jane@westsidedental.com" }
```

**Response**
```json
{ "session_id": "uuid" }
```

---

### POST /support/sessions/:id/chat
Send a message and get the agent's reply.

**Body**
```json
{ "message": "How do I submit an insurance claim?" }
```

**Response**
```json
{
  "reply": "To submit a claim, go to Billing > New Claim...",
  "escalated": false
}
```

If `escalated` is `true`, the session is closed for further chat and a human will follow up.

---

### GET /support/sessions/:id/history
Get all messages in a session.

**Response**
```json
[
  { "role": "user", "content": "...", "created_at": "..." },
  { "role": "assistant", "content": "...", "created_at": "..." }
]
```

---

## Sales Agent

### POST /sales/research
Research a clinic and generate an outreach email draft. This call takes ~15-30 seconds (web search + LLM).

**Body**
```json
{
  "clinic_name": "Westside Family Dental",
  "website_url": "https://westsidedental.com"
}
```

**Response**
```json
{
  "prospect_id": "uuid",
  "draft_id": "uuid",
  "fit_score": 82,
  "fit_reasoning": "Independent single-location dental clinic with ~8 staff...",
  "email_subject": "Managing Westside's scheduling during your busy season",
  "email_body": "Hi Dr. Johnson,\n\nI noticed Westside Family Dental..."
}
```

---

### GET /sales/prospects
List all researched prospects.

**Response**
```json
[
  {
    "id": "uuid",
    "clinic_name": "Westside Family Dental",
    "website_url": "https://westsidedental.com",
    "fit_score": 82,
    "status": "draft_ready",
    "created_at": "..."
  }
]
```

---

### GET /sales/prospects/:id
Get full prospect details including all drafts.

**Response**
```json
{
  "id": "uuid",
  "clinic_name": "...",
  "fit_score": 82,
  "fit_reasoning": "...",
  "drafts": [
    {
      "id": "uuid",
      "subject": "...",
      "body": "...",
      "approved": false,
      "created_at": "..."
    }
  ]
}
```

---

### POST /sales/drafts/:id/approve
Approve a draft for sending (human-in-the-loop step).

**Response**
```json
{ "approved": true }
```

---

## Admin Dashboard

### GET /admin/stats
Overview numbers.

**Response**
```json
{
  "total_sessions": 12,
  "escalations": 2,
  "prospects": 5,
  "drafts_pending_approval": 3,
  "knowledge_articles": 10
}
```

---

### GET /admin/sessions
All support sessions with message counts.

**Response**
```json
[
  {
    "id": "uuid",
    "user_identifier": "jane@westsidedental.com",
    "status": "active",
    "message_count": 6,
    "created_at": "..."
  }
]
```

---

### GET /admin/sessions/:id
Full session with all messages.

**Response**
```json
{
  "id": "uuid",
  "user_identifier": "...",
  "status": "escalated",
  "messages": [
    { "role": "user", "content": "...", "created_at": "..." },
    { "role": "assistant", "content": "...", "created_at": "..." }
  ]
}
```

---

### GET /admin/escalations
Sessions flagged for human follow-up.

**Response** — same shape as `/admin/sessions` but filtered to `status = 'escalated'`.

---

### GET /admin/articles
All knowledge base articles.

**Response**
```json
[
  {
    "id": "uuid",
    "title": "How to submit an insurance claim",
    "category": "billing",
    "tags": ["insurance", "claims"],
    "created_at": "..."
  }
]
```

---

### POST /admin/articles
Create a new knowledge base article.

**Body**
```json
{
  "title": "How to handle a denied claim",
  "content": "When a claim is denied...",
  "category": "billing",
  "tags": ["denial", "claims"]
}
```

**Response**
```json
{ "id": "uuid" }
```

---

### DELETE /admin/articles/:id
Delete an article.

**Response**
```json
{ "deleted": true }
```

---

## Health

### GET /health
```json
{ "status": "ok" }
```
