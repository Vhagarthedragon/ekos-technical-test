# API Reference

Base URL (local): `http://localhost:8000/api`  
Base URL (production): `https://ekos-technical-test.onrender.com/api`  
Interactive docs: `{base_url}/docs`

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

If `escalated` is `true`, the session is locked and a human will follow up.

---

### GET /support/sessions/:id/history
All messages in a session.

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
Deep-research a clinic and generate outreach drafts. Takes ~10–20 seconds (2–4 web searches + LLM).

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
  "location": "Miami, FL",
  "specialty": "dental",
  "staff_size": "small",
  "key_findings": ["Est. 2009", "Active Google reviews", "No online booking"],
  "contact_phone": "+1 305 000 0000",
  "contact_email": "info@westsidedental.com",
  "contact_address": "123 Coral Way, Miami FL 33145",
  "website_found": "https://westsidedental.com",
  "email_subject": "Managing Westside's scheduling during your busy season",
  "email_body": "Hi Dr. Johnson,\n\nI noticed Westside Family Dental...",
  "whatsapp_message": "Hi Dr. Johnson — saw Westside Dental has been around since 2009..."
}
```

---

### POST /sales/prospect-city
Find and quick-score multiple clinics in a city. Takes ~15 seconds for up to 10 results.

**Body**
```json
{
  "city": "Miami, FL",
  "specialty": "dental",
  "max_results": 5
}
```
`specialty` is optional. `max_results` must be 1–10.

**Response**
```json
[
  {
    "prospect_id": "uuid",
    "clinic_name": "Coral Gables Dental",
    "website_url": "https://coralgablesdental.com",
    "location": "Miami, FL",
    "specialty": "dental",
    "staff_size": "small",
    "fit_score": 78,
    "fit_reasoning": "Independent dental practice, active website, no enterprise EMR detected.",
    "status": "new"
  }
]
```

---

### GET /sales/prospects
All prospects, ordered by creation date.

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

Possible `status` values: `new` · `researching` · `draft_ready`

---

### GET /sales/prospects/:id
Full prospect with all drafts.

**Response**
```json
{
  "id": "uuid",
  "clinic_name": "...",
  "fit_score": 82,
  "fit_reasoning": "...",
  "location": "...",
  "specialty": "dental",
  "staff_size": "small",
  "raw_research": {
    "key_findings": ["..."],
    "contact_phone": "...",
    "contact_email": "...",
    "contact_address": "...",
    "website_found": "..."
  },
  "drafts": [
    {
      "id": "uuid",
      "subject": "...",
      "body": "...",
      "whatsapp_message": "...",
      "approved": false,
      "created_at": "..."
    }
  ]
}
```

---

### POST /sales/drafts/:id/approve
Approve a draft (human-in-the-loop step). Sets `approved=TRUE` in the database.

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
  "prospects": 8,
  "drafts_pending_approval": 3,
  "knowledge_articles": 10
}
```

---

### GET /admin/sessions
All support sessions with message counts.

---

### GET /admin/sessions/:id
Full session with all messages.

---

### GET /admin/escalations
Sessions with `status = 'escalated'`.

---

### GET /admin/articles
All knowledge base articles.

---

### POST /admin/articles
Create a new article.

**Body**
```json
{
  "title": "How to handle a denied claim",
  "content": "When a claim is denied...",
  "category": "billing",
  "tags": ["denial", "claims"]
}
```

---

### DELETE /admin/articles/:id
Delete an article.

---

## Health

### GET /health
```json
{ "status": "ok" }
```
