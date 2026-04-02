-- Knowledge base: help articles about clinic software
CREATE TABLE IF NOT EXISTS knowledge_articles (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title       TEXT NOT NULL,
    content     TEXT NOT NULL,
    category    TEXT NOT NULL,
    tags        TEXT[] DEFAULT '{}',
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_articles_fts
    ON knowledge_articles
    USING gin(to_tsvector('english', title || ' ' || content));

-- Support chat sessions
CREATE TABLE IF NOT EXISTS support_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_identifier TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'active',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS support_messages (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id  UUID NOT NULL REFERENCES support_sessions(id) ON DELETE CASCADE,
    role        TEXT NOT NULL,
    content     TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_messages_session ON support_messages(session_id);

-- Sales prospects researched by the agent
CREATE TABLE IF NOT EXISTS prospects (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clinic_name     TEXT NOT NULL,
    website_url     TEXT,
    location        TEXT,
    specialty       TEXT,
    staff_size      TEXT,
    fit_score       INTEGER CHECK (fit_score BETWEEN 0 AND 100),
    fit_reasoning   TEXT,
    raw_research    JSONB DEFAULT '{}',
    status          TEXT NOT NULL DEFAULT 'researched',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Outreach drafts waiting for human approval
CREATE TABLE IF NOT EXISTS outreach_drafts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prospect_id     UUID NOT NULL REFERENCES prospects(id) ON DELETE CASCADE,
    subject         TEXT NOT NULL,
    body            TEXT NOT NULL,
    approved        BOOLEAN DEFAULT FALSE,
    approved_at     TIMESTAMPTZ,
    sent_at         TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_drafts_prospect ON outreach_drafts(prospect_id);
