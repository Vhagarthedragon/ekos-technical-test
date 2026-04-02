# Agent Design

## Support Agent (Track A)

### Purpose
Answer software questions for clinic staff in real time. Handle multi-turn conversations, walk through multi-step procedures, and hand off to a human when confidence is low or the user is frustrated.

### Model
`claude-3-5-haiku-20241022` — fast response times matter for a support chat. Haiku handles tool calling well and is significantly cheaper for high-volume conversations.

### Tools

| Tool | Description |
|------|-------------|
| `search_knowledge_base` | Full-text search over help articles in PostgreSQL |
| `escalate_to_human` | Flags the session as escalated, saves reason to DB |

### Agentic loop
```
user message
    → Claude sees conversation history + system prompt
    → calls search_knowledge_base (usually 1-2 times)
    → tool results fed back
    → Claude produces final text response
    → if escalation needed: calls escalate_to_human first, then responds
```

Claude decides how many searches to run. On simple questions it usually calls the tool once. On ambiguous ones it might search twice with different queries.

### Escalation logic
The system prompt defines clear triggers. The backend also blocks further chat on escalated sessions — the user sees a notice and the next human rep picks it up from the database.

### System prompt philosophy
- Get to the point. Clinic staff are in the middle of a workday.
- Always search before saying you don't know.
- Escalate rather than guess on billing, legal, or account issues.

---

## Sales Agent (Track B)

### Purpose
Given a clinic name and optional URL, research the prospect online, score their fit for ClinicDesk (0–100), and produce a personalized outreach email that sounds like it was written by a thoughtful sales rep — not a template.

### Model
`claude-3-5-sonnet-20241022` — research + creative writing quality matters more than speed here. A rep will review the output before it goes anywhere.

### Tools

| Tool | Description |
|------|-------------|
| `search_web` | Tavily search — returns titles, URLs, and content snippets |

### Pipeline
```
input: clinic_name + website_url
    → save prospect to DB (status: 'researching')
    → Claude runs 2-4 web searches about the clinic
    → Claude reasons over findings
    → returns structured JSON with:
        - location, specialty, staff_size
        - fit_score (0-100) + fit_reasoning
        - email_subject + email_body
        - raw_research (key findings)
    → save prospect details + draft to DB
    → frontend shows result for human review
```

### Human-in-the-loop
Drafts are stored with `approved=FALSE`. The frontend shows the email with an "Approve" button. Only after a human clicks approve does the system mark it as ready to send. This is a hard constraint — no email leaves without review.

### Fit scoring criteria (in system prompt)
High fit (70-100): independent clinic, 1-50 staff, currently on paper or basic tools, dental or primary care.
Medium fit (40-69): part of a small group, already using some software.
Low fit (0-39): large hospital network, non-clinic healthcare, already on enterprise EMR.

### Why Tavily
Tavily returns clean, structured search results optimized for LLM consumption (no raw HTML). The free tier (1,000 searches/month) is sufficient for this use case. The agent typically runs 2-3 searches per prospect.

---

## Inter-agent handoff

The two agents are independent. However, there's a natural connection: if the Support Agent detects a user asking about pricing or upgrades (currently handled by an escalation), that escalation could automatically create a prospect record for the Sales Agent. This is the next iteration — the system prompt for the Support Agent could call `create_sales_prospect` instead of just flagging for a human.
