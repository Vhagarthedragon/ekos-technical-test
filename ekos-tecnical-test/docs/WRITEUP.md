# Write-Up

## Problem

Clinic staff — office managers, front desk coordinators, billing specialists — spend significant time on two things that AI can meaningfully accelerate: getting answers about their software, and being sold to effectively.

**Support side:** when a billing coordinator doesn't know how to handle a denied insurance claim, they either call support (hold times), dig through documentation (slow), or guess (risky). A conversational agent with the full knowledge base at hand, one that can walk them step by step through the right procedure, removes that friction — and it lives inside the app they already have open.

**Sales side:** outreach to independent clinics is high-volume and highly repetitive. Most sales emails are generic. Clinics are busy and ignore them. An agent that researches a specific clinic — their specialty, size, location, likely pain points — and writes an email that references something real about them changes the hit rate. Even better: an agent that proactively surfaces 10 prospects in a city in 15 seconds, ranked by fit.

---

## What I built

### Support Agent
A floating chat widget that embeds in any page via a launcher button — the same model used by Intercom, Crisp, and every serious SaaS support tool. It's not a full-page chat; it lives on top of the existing application. The demo page is a simulated ClinicDesk dashboard that makes this context obvious to evaluators.

- Multi-turn conversation with full session history stored in PostgreSQL
- Every response is grounded in the knowledge base via full-text search (RAG)
- Escalation path is explicit and enforced: when the agent flags a session, the chat locks and a human rep takes over from the admin dashboard
- Guided product tour on first visit explains the embedded widget concept

### Sales Agent — two modes

**Single Clinic:** deep research on one practice. The agent runs 2–4 Tavily web searches, reasons over the results, and produces: ICP fit score (0–100) with reasoning, full clinic profile (specialty, staff size, location, address, phone, email, website), key findings from research, and personalized email + WhatsApp drafts. Human approval required before any draft moves forward.

**City Scan:** bulk prospecting. Enter a city and optionally filter by specialty — the agent searches the web, extracts up to 10 distinct clinics from the results, and quick-scores each one in a single Claude call (~15 seconds total). Results appear as a scored grid. Each card has a "Full Research →" button that triggers the deep-dive analysis.

### Admin Dashboard
Operational visibility: session overview, escalation queue with full chat transcripts, knowledge base CRUD to add/edit/delete articles without touching the database.

---

## Key design decisions

**Embedded widget, not a standalone page.** The support feature is designed to live inside an existing product, not as its own page. This required rethinking the Vue routing so the widget view renders full-screen (matching the host app) while other views use the standard shell. A product tour explains the concept on first visit so evaluators don't have to guess.

**City Scan as a proactive capability.** Single-clinic research is reactive (you already know who to call). City Scan makes the agent proactive — it finds prospects you didn't know about. One Tavily search + one Claude call replaces what would otherwise be manual prospecting across multiple tabs.

**Two modes, one interface.** Sales could have been two separate pages. Instead it's a tab toggle that keeps prospect history unified. A clinic found via City Scan and then deepened via Full Research shows up once in the table, with its status updated.

**Human-in-the-loop as a hard constraint, not a UI suggestion.** Outreach drafts are stored with `approved=FALSE` at the database level. The approval endpoint flips that field. Nothing else in the system checks it — but the constraint is real and auditable. This reflects production reality: AI-drafted sales emails need a human to check tone and accuracy before reaching a prospect.

**PostgreSQL full-text search over a vector DB.** The knowledge base is structured with titled, categorized articles. `tsvector`/`tsquery` with a GIN index is fast, accurate, requires no external service, and works well for the structured question-and-answer shape of support content. The honest tradeoff: searching "claim rejected" won't match an article titled "handling EOB denials" unless both terms appear. `pgvector` with embeddings is the clear upgrade path and the schema is already normalized for it.

**Agentic tool loop.** Both agents run a `while True` loop where Claude calls tools, gets results back, and decides whether to call more or produce a final answer. The loop exits on `end_turn`. This lets the agent adapt its search strategy mid-run — on a complex question it might search twice with different queries before answering; on a simple one it answers after one. A single-shot prompt can't do this.

**One model, both agents.** Both agents run `claude-haiku-4-5`. The original design used Haiku for support and Sonnet for sales (better reasoning for multi-step research). In practice, `claude-haiku-4-5` handles the sales research task well and is significantly cheaper at scale. The system prompt does the heavy lifting: explicit scoring criteria, structured JSON output format, and a hard "English only" constraint.

**Clean Architecture in the backend.** Agents live in `application/`, have no FastAPI imports, and don't know about HTTP. Routes live in `presentation/`, have no Claude imports, and don't know about the agent loop. This separation isn't ceremony — it means the agents can be tested independently of the web framework, and new channels (WebSocket, CLI, Celery task) can call the same agent functions without refactoring.

---

## Tradeoffs

**No real email or WhatsApp sending.** The approval step is implemented and enforced. The actual send is not — it would require a SendGrid or Twilio integration and decisions about bounce handling, opt-out management, and rate limits. I prioritized getting the agent reasoning and approval workflow right, which is the harder and more interesting problem.

**Knowledge base seeded manually.** The 10 articles cover representative ClinicDesk scenarios. In production this would be managed through the admin dashboard (which is built) by whoever owns support content. The schema and index are already in place.

**Single-tenant.** Sessions are identified by a user-provided string (email or name). For a real deployment, sessions would be tied to authenticated clinic accounts with row-level security in Supabase. The database structure would need a `clinic_id` foreign key added to sessions and prospects tables.

**City Scan scores are approximate.** The quick score for city scan results is based on search snippets only — much less signal than a full research run. The UI communicates this: the card shows a score but the CTA is "Full Research →", not "Approve". The score is a triage tool, not a final judgment.

---

## What I'd build next

**Support → Sales handoff.** When a clinic staff member asks the Support Agent about pricing or upgrades, that's a warm sales signal. The agent currently escalates it to a human. The better behavior: call a `create_sales_prospect` tool instead, pass the clinic context from the session, and have a prospect record appear in the Sales Agent's queue with the conversation attached. The infrastructure is ready — both agents write to the same database.

**Knowledge gap detection.** Log every support query that returns zero results from the knowledge base. Surface the top patterns weekly to whoever manages content. The support agent gets smarter without code changes.

**Deterministic research pipeline for sales.** The agent currently decides how many searches to run and in what order. For production, this would be a fixed workflow: fetch website → search for reviews → search for staff count → score → draft. Deterministic pipelines are faster, cheaper, and easier to debug when the output quality drops.

**`pgvector` for semantic search.** The most impactful upgrade for the Support Agent. Add an `embedding` column to `knowledge_articles`, generate embeddings on insert, and swap the `tsvector` search for a cosine similarity query. "Claim rejected" would then find "handling EOB denials" because the concepts are semantically close.
