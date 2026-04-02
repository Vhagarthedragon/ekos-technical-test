# Demo Script

Quick walkthrough to show the evaluator both agents working end to end.

---

## Support Agent (~2 min)

1. Open the app, click **Support Agent** in the sidebar
2. Enter an email: `demo@greenpointdental.com`
3. Click **Start conversation**

**Message 1 — Knowledge base hit:**
> "How do I verify a patient's insurance before their appointment?"

Expected: Claude searches the knowledge base, returns a clear step-by-step answer about the Verify Eligibility button.

**Message 2 — Multi-step follow-up:**
> "What if the verification fails and shows inactive coverage?"

Expected: Claude follows up with guidance on manual verification or contacting the insurer.

**Message 3 — Trigger escalation:**
> "This is the third time I'm asking and nothing is working, I need to talk to someone"

Expected: Claude detects frustration, calls the `escalate_to_human` tool, and the conversation is flagged. The UI shows the escalation badge.

---

## Sales Agent (~3 min)

1. Click **Sales Agent** in the sidebar
2. Enter:
   - Clinic name: `Greenpoint Pediatric Dentistry`
   - Website: `https://greenpointpediatricdentistry.com`
3. Click **Research & Draft Email**

Wait ~15 seconds while Claude searches the web and drafts the email.

Expected output:
- Fit score (likely 65-85 for an independent pediatric practice)
- Short reasoning paragraph
- Email subject that references something specific about the clinic
- Email body: 3-4 paragraphs, no corporate opener, one clear CTA

4. Read the draft — notice it references something real found during research
5. Click **Approve & Send** to demonstrate the human-in-the-loop step
6. The badge changes to **Approved**

7. Scroll down to **Past prospects** — the clinic appears in the list with its fit score

---

## What to point out

- The support agent runs a tool call before every answer (not just making things up)
- The sales agent runs 2-3 searches before writing — visible in the 15s wait
- Escalation is a real state change in the database, not just a UI message
- Approval is a hard gate — `approved = false` until a human acts
