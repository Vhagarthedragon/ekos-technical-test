# Agent Design

## Support Agent (Track A)

### Purpose
Answer ClinicDesk software questions for clinic staff in real time. Handle multi-turn conversations, walk through multi-step procedures, and hand off to a human when confidence is low or the topic is outside the agent's scope (billing disputes, legal questions, account-level issues).

### Delivery model
A **floating chat widget** embedded in the host application — not a standalone page. The launcher button lives in the bottom-right corner of any page. Clicking it opens a 360×520px panel. This matches how production support tooling actually ships inside SaaS products.

### Model
`claude-haiku-4-5-20251001` — fast response times are essential for a support chat. The model handles tool calling well, costs less at scale, and handles ClinicDesk procedure questions accurately when grounded via the knowledge base.

### Tools

| Tool | Description |
|------|-------------|
| `search_knowledge_base` | Full-text search (`tsvector`/`tsquery`) over help articles in PostgreSQL. Returns up to 5 ranked results. |
| `escalate_to_human` | Marks the session `escalated` in the DB, saves the reason. The session is then locked — no more AI replies. |

### Agentic loop
```
user message
  → Claude sees full conversation history + system prompt
  → calls search_knowledge_base (1–2 times, adapts based on results)
  → tool results returned with titles + content
  → Claude produces final text response
  → if topic is out of scope: calls escalate_to_human, then replies with handoff message
```

### Escalation triggers (defined in system prompt)
- Insurance billing disputes or denied claim appeals
- Account cancellation, refunds, or pricing
- Legal or HIPAA compliance questions
- User expresses frustration after two unhelpful responses
- Agent has no relevant knowledge base results after two searches

### System prompt philosophy
- Get to the point — clinic staff are in the middle of a workday
- Always search before saying you don't know
- Give step-by-step instructions when procedures are involved
- Escalate rather than guess on high-stakes topics

---

## Sales Agent (Track B)

### Purpose
Research clinic prospects and produce personalized outreach. Operates in two modes: deep single-clinic research, and bulk city scanning.

### Model
`claude-haiku-4-5-20251001` — handles multi-step research and structured JSON output well. The quality of the outreach drafts comes primarily from the research depth and the system prompt's explicit instructions (reference something specific, no generic openers, no formal language for WhatsApp).

### Mode 1: Single Clinic (deep research)

**Input:** clinic name + optional website URL

**Pipeline:**
```
save prospect (status: 'researching')
  → Claude runs 2–4 Tavily web searches about the clinic
  → tool results fed back after each search
  → Claude reasons over all findings
  → returns structured JSON with:
      location, specialty, staff_size
      fit_score (0–100), fit_reasoning (2–3 sentences)
      key_findings (3–5 bullets from research)
      contact_phone, contact_email, contact_address, website_found
      email_subject, email_body (3–4 paragraphs)
      whatsapp_message (under 280 chars, conversational)
update prospect (status: 'draft_ready')
save outreach_draft (approved=FALSE)
```

**Tool:**

| Tool | Description |
|------|-------------|
| `search_web` | Tavily search — returns titles, URLs, and content snippets optimized for LLM consumption. |

### Mode 2: City Scan (bulk prospecting)

**Input:** city name + optional specialty + result count (1–10)

**Pipeline:**
```
one Tavily search: "{specialty} clinics in {city}"
  → one Claude call (no tool loop):
      extract up to N distinct clinics from search snippets
      quick-score each (0–100) based on available signal
      return JSON array
save each clinic as prospect (status: 'new')
return scored list to frontend
```

This runs as a single Claude call — no agentic loop — because the goal is fast triage, not deep analysis. The scores are approximate and labeled as such. The "Full Research →" button on each card triggers Mode 1.

### Fit scoring criteria (in system prompt)

| Signal | Points |
|--------|--------|
| Independent clinic (not hospital chain) | +30 |
| Dental or primary care specialty | +20 |
| Has a real website | +15 |
| Small/medium staff (1–50) | +15 |
| No visible enterprise EMR (Epic, Cerner) | +20 |

Score ranges: **70–100** = strong fit, **40–69** = medium, **0–39** = weak.

### Human-in-the-loop
Drafts are stored with `approved=FALSE`. The frontend shows the email and WhatsApp message with an "Approve" button. Only after a human clicks approve does the system mark the draft as ready. This is enforced at the database layer — no email or message leaves the system without review.

---

## Inter-agent connection

The two agents are independent modules but share the same database. A natural next step: when the Support Agent detects a staff member asking about pricing or upgrades (currently handled by escalation), instead of only flagging for a human it could call a `create_sales_prospect` tool, passing the clinic context from the session. The Sales Agent's queue would receive a warm lead with conversation context attached. The infrastructure is in place — it's a system prompt change and a new tool definition.
