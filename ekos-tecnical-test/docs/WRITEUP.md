# Write-Up

## Problem

Clinic staff — office managers, front desk coordinators, billing specialists — spend significant time on two things that AI can meaningfully accelerate: getting help with their software, and being sold to effectively.

On the support side: when a billing coordinator doesn't know how to handle a denied insurance claim, they either call support (hold times), dig through documentation (slow), or guess (risky). A conversational agent with the full knowledge base available, one that can walk them step by step through the right procedure, removes that friction entirely.

On the sales side: outreach to independent clinics is high-volume and highly repetitive. Most sales emails are generic. Clinics are busy and ignore them. An agent that researches a specific clinic — their specialty, size, likely pain points — and writes an email that references something real about them changes the hit rate.

## What I built

Two agents that address both problems:

**Support Agent** handles multi-turn conversations for clinic staff. It searches a structured knowledge base on every question, walks through procedures step by step, and escalates to a human with full context when it can't confidently answer. The escalation path is intentional — the agent knows its limits.

**Sales Agent** takes a clinic name and optional website, runs 2–4 web searches via Tavily, scores the prospect's fit for ClinicDesk (0–100 with reasoning), and writes a personalized outreach email referencing specific details it found. Every draft sits behind a human approval step — no email goes anywhere without a person reading it first.

## Key design decisions

**Two agents, two models** — Support uses Claude Haiku (fast, cheap, conversational). Sales uses Claude Sonnet (better reasoning for multi-step research and writing). Matching model capability to task complexity made an obvious difference in email quality.

**Agentic tool loop** — Both agents run a `while True` loop where Claude calls tools, gets results, and decides whether to call more or respond. This lets the agent reason across multiple search results and stop when it has enough. A single-shot prompt would produce worse results because the agent couldn't adapt its search strategy mid-run.

**Human-in-the-loop as a hard constraint** — Outreach drafts are stored with `approved=False` and the backend enforces this. The approval step isn't optional UI — it's a database field that has to be flipped before anything can move forward. This reflects a real-world reality: AI-drafted sales emails need a human to sanity-check tone and accuracy before going to a prospect.

**PostgreSQL full-text search** — The knowledge base is structured with titled, categorized articles. `tsvector`/`tsquery` with a GIN index is fast, accurate, and requires no external service. The tradeoff is that it won't handle semantically related terms well (searching "claim rejected" won't match an article titled "handling EOB denials"). Vector embeddings via pgvector would solve this — it's the obvious next step.

**Clean separation of concerns** — Agent logic lives in `application/`, database access in `infrastructure/`, HTTP handling in `presentation/`. The agents don't import FastAPI; the routes don't touch Claude directly. This makes both easier to test and extend independently.

## Tradeoffs

**No real email sending** — The approval step is implemented but the actual send is not. In a real system, approving a draft would trigger a SendGrid or Gmail API call. The infrastructure decision (which service, how to handle bounces) is straightforward — I prioritized getting the agent logic and approval flow right first.

**Knowledge base seeded manually** — The 10 articles in the seed migration are representative but limited. A production system would have a content management interface where support leads add and update articles as the product evolves. The database schema and full-text index are already set up for it.

**Single-tenant** — There's no authentication or multi-tenant separation. Sessions are identified by a user-provided string (email). For a real deployment, sessions would be tied to authenticated clinic accounts.

## What I'd build next

**Support → Sales handoff** — When the Support Agent escalates because a user is asking about upgrades or pricing, that should automatically create a prospect record for the Sales Agent. The infrastructure is there (both agents write to the same database) — it's a system prompt change and a new tool call away.

**Knowledge gap detection** — Track which queries return zero search results. Surface them to whoever manages the knowledge base. The support agent gets better without any code changes.

**Structured workflow for sales** — The research pipeline is currently fully agentic (Claude decides how many searches to run, in what order). For production, the research phase would be a deterministic workflow: fetch website → search for reviews → search for staff size → score → draft. This makes it faster, cheaper, and easier to debug when the output isn't great.
