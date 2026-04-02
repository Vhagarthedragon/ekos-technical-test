<template>
  <div class="sales">

    <!-- ── Tour overlay ──────────────────────────────── -->
    <Transition name="fade">
      <div v-if="tourActive" class="tour-overlay" @click.self="endTour" />
    </Transition>
    <Transition name="tooltip">
      <div v-if="tourActive" class="tour-tooltip" :class="`tour-pos-${STEPS[tourStep].pos}`">
        <div class="tour-step-count">{{ tourStep + 1 }} / {{ STEPS.length }}</div>
        <p class="tour-title">{{ STEPS[tourStep].title }}</p>
        <p class="tour-body">{{ STEPS[tourStep].body }}</p>
        <div class="tour-actions">
          <button class="tour-skip" @click="endTour">Skip tour</button>
          <div class="tour-dots">
            <span v-for="(_, i) in STEPS" :key="i" class="tour-dot" :class="{ active: i === tourStep }" />
          </div>
          <button class="tour-next" @click="advanceTour">
            {{ tourStep < STEPS.length - 1 ? 'Next →' : 'Got it ✓' }}
          </button>
        </div>
      </div>
    </Transition>

    <div class="page-header">
      <div class="page-header-left">
        <h1>Sales Agent</h1>
        <p class="subtitle">Research a clinic, score their fit, and generate personalized outreach.</p>
      </div>
      <button class="tour-launch-btn" @click="startTour" title="Start guided tour">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/>
        </svg>
        Tour
      </button>
    </div>

    <!-- Research form -->
    <div class="card research-form" :class="{ 'tour-highlight': tourActive && tourStep === 0 }">
      <div class="form-fields">
        <div class="field">
          <label>Clinic name *</label>
          <input v-model="clinicName" placeholder="Westside Family Dental" @keyup.enter="runResearch" />
        </div>
        <div class="field">
          <label>Website <span class="optional">optional</span></label>
          <input v-model="websiteUrl" placeholder="https://westsidedental.com" />
        </div>
      </div>
      <div class="form-footer">
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button class="btn-primary" @click="runResearch" :disabled="loading || !clinicName.trim()">
          <span v-if="loading" class="spinner"></span>
          {{ loading ? 'Researching...' : 'Research & Draft' }}
        </button>
      </div>
    </div>

    <!-- Result -->
    <div v-if="result" class="result-grid">

      <!-- Left: prospect info -->
      <div class="prospect-info">

        <!-- Fit score -->
        <div class="card fit-card" :class="{ 'tour-highlight': tourActive && tourStep === 2 }">
          <div class="fit-top">
            <div>
              <p class="section-label">Fit Score</p>
              <div class="fit-score" :class="scoreClass">
                {{ result.fit_score }}<span class="score-denom">/100</span>
              </div>
            </div>
            <div class="fit-bar-wrap">
              <div class="fit-bar">
                <div class="fit-bar-fill" :class="scoreClass" :style="{ width: result.fit_score + '%' }"></div>
              </div>
              <p class="fit-reasoning">{{ result.fit_reasoning }}</p>
            </div>
          </div>
        </div>

        <!-- Clinic details -->
        <div class="card details-card">
          <p class="section-label">Clinic Profile</p>
          <div class="details-grid">
            <div class="detail-item">
              <span class="detail-label">Specialty</span>
              <span class="detail-value">{{ result.specialty || '—' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Staff size</span>
              <span class="detail-value">{{ result.staff_size || '—' }}</span>
            </div>
            <div class="detail-item" v-if="result.location">
              <span class="detail-label">Location</span>
              <span class="detail-value">{{ result.location }}</span>
            </div>
            <div class="detail-item" v-if="result.contact_address">
              <span class="detail-label">Address</span>
              <span class="detail-value">{{ result.contact_address }}</span>
            </div>
          </div>

          <div class="contact-info">
            <p class="section-label" style="margin-top:16px">Contact</p>
            <div class="details-grid">
              <div class="detail-item" v-if="result.website_found">
                <span class="detail-label">Website</span>
                <a :href="result.website_found" target="_blank" class="detail-link">
                  {{ result.website_found.replace('https://','').replace('http://','').replace(/\/$/,'') }}
                </a>
              </div>
              <div class="detail-item" v-if="result.contact_phone">
                <span class="detail-label">Phone</span>
                <span class="detail-value">{{ result.contact_phone }}</span>
              </div>
              <div class="detail-item" v-if="result.contact_email">
                <span class="detail-label">Email</span>
                <span class="detail-value">{{ result.contact_email }}</span>
              </div>
              <div v-if="!result.website_found && !result.contact_phone && !result.contact_email" class="detail-item">
                <span class="detail-value muted">Not found</span>
              </div>
            </div>
          </div>

          <div v-if="result.key_findings?.length" class="findings">
            <p class="section-label" style="margin-top:16px">Key findings</p>
            <ul class="findings-list">
              <li v-for="f in result.key_findings" :key="f">{{ f }}</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Right: outreach drafts -->
      <div class="drafts-panel" :class="{ 'tour-highlight': tourActive && tourStep === 3 }">
        <div class="drafts-header">
          <p class="section-label">Outreach Drafts</p>
          <div class="channel-tabs">
            <button class="ch-tab" :class="{ active: channel === 'email' }" @click="channel = 'email'">
              <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
              Email
            </button>
            <button class="ch-tab" :class="{ active: channel === 'whatsapp' }" @click="channel = 'whatsapp'">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
              </svg>
              WhatsApp
              <span class="soon-badge">soon</span>
            </button>
          </div>
        </div>

        <!-- Email draft -->
        <div v-if="channel === 'email'" class="draft-content card">
          <div class="draft-meta">
            <p class="draft-subject">{{ result.email_subject }}</p>
            <div class="draft-actions">
              <span v-if="approved" class="badge badge-green">Approved</span>
              <button v-else class="btn-primary btn-sm" @click="approveDraft">Approve</button>
            </div>
          </div>
          <div class="draft-body">{{ result.email_body }}</div>
          <p class="review-note">Review before approving — no email is sent without your sign-off.</p>
        </div>

        <!-- WhatsApp draft -->
        <div v-if="channel === 'whatsapp'" class="draft-content card">
          <div class="draft-meta">
            <p class="draft-subject">WhatsApp message</p>
            <div class="draft-actions">
              <span class="badge badge-yellow">Not connected</span>
            </div>
          </div>
          <div class="whatsapp-preview">
            <div class="wa-bubble">{{ result.whatsapp_message }}</div>
            <p class="wa-char-count">{{ result.whatsapp_message?.length || 0 }} chars</p>
          </div>
          <p class="review-note">WhatsApp integration coming soon. The message draft is ready when you connect it.</p>
        </div>
      </div>
    </div>

    <!-- Past prospects -->
    <div class="prospects-section" :class="{ 'tour-highlight': tourActive && tourStep === 4 }">
      <div class="section-header">
        <h2>Past prospects</h2>
        <button class="btn-ghost" @click="loadProspects">Refresh</button>
      </div>
      <div v-if="prospects.length === 0" class="empty">No prospects yet. Research a clinic above.</div>
      <div v-else class="prospects-list">
        <div v-for="p in prospects" :key="p.id" class="card prospect-row" @click="loadProspect(p.id)">
          <div class="prospect-left">
            <p class="prospect-name">{{ p.clinic_name }}</p>
            <p class="prospect-url muted">{{ p.website_url || 'no website' }}</p>
          </div>
          <div class="prospect-right">
            <span v-if="p.fit_score !== null" class="badge" :class="prospectScoreClass(p.fit_score)">
              {{ p.fit_score }}/100
            </span>
            <span class="badge badge-blue">{{ p.status }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { sales } from '../api'

// ── Tour ──────────────────────────────────────────────
const STEPS = [
  {
    pos: 'form',
    title: 'Research a clinic',
    body: 'Enter any clinic name — dental, physio, dermatology, etc. Add their website to improve accuracy. The agent will search the public web for you.',
  },
  {
    pos: 'form-btn',
    title: 'One click to start the agent',
    body: 'Clicking "Research & Draft" triggers the Sales Agent. It uses Tavily AI for web search and Claude to analyse findings — typically takes 10–15 seconds.',
  },
  {
    pos: 'score',
    title: 'ICP Fit Score',
    body: 'The agent scores how well the clinic matches your ideal customer profile (0–100) and explains why. Helps you prioritise outreach.',
  },
  {
    pos: 'drafts',
    title: 'Personalized outreach drafts',
    body: 'A tailored email and a WhatsApp message are generated using the research. Nothing is sent until you click Approve — full human-in-the-loop control.',
  },
  {
    pos: 'prospects',
    title: 'Prospect history',
    body: 'Every researched clinic is saved here. Click any row to instantly reload its fit score, profile, and drafts — no need to re-run the agent.',
  },
]

const tourActive = ref(false)
const tourStep = ref(0)

function startTour() {
  tourStep.value = 0
  tourActive.value = true
}

function advanceTour() {
  if (tourStep.value < STEPS.length - 1) {
    tourStep.value++
  } else {
    endTour()
  }
}

function endTour() {
  tourActive.value = false
  localStorage.setItem('salesTourSeen', '1')
}

// ── Data ─────────────────────────────────────────────
const clinicName = ref('')
const websiteUrl = ref('')
const loading = ref(false)
const error = ref('')
const result = ref(null)
const approved = ref(false)
const channel = ref('email')
const prospects = ref([])

onMounted(async () => {
  await loadProspects()
  if (!localStorage.getItem('salesTourSeen')) {
    setTimeout(startTour, 600)
  }
})

async function runResearch() {
  if (!clinicName.value.trim() || loading.value) return
  loading.value = true
  error.value = ''
  result.value = null
  approved.value = false
  channel.value = 'email'
  try {
    const res = await sales.research(clinicName.value.trim(), websiteUrl.value.trim() || null)
    result.value = res.data
    await loadProspects()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Research failed. Please try again.'
  } finally {
    loading.value = false
  }
}

async function approveDraft() {
  if (!result.value?.draft_id) return
  await sales.approveDraft(result.value.draft_id)
  approved.value = true
}

async function loadProspects() {
  const res = await sales.prospects()
  prospects.value = res.data
}

async function loadProspect(id) {
  const res = await sales.prospect(id)
  const p = res.data
  const draft = p.drafts?.[0]
  const rr = p.raw_research || {}
  result.value = {
    prospect_id: p.id,
    draft_id: draft?.id,
    fit_score: p.fit_score,
    fit_reasoning: p.fit_reasoning,
    location: p.location,
    specialty: p.specialty,
    staff_size: p.staff_size,
    key_findings: rr.key_findings || [],
    contact_phone: rr.contact_phone || null,
    contact_email: rr.contact_email || null,
    contact_address: rr.contact_address || null,
    website_found: rr.website_found || p.website_url || null,
    email_subject: draft?.subject,
    email_body: draft?.body,
    whatsapp_message: draft?.whatsapp_message,
  }
  approved.value = draft?.approved || false
  clinicName.value = p.clinic_name
  websiteUrl.value = p.website_url || ''
  channel.value = 'email'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const scoreClass = computed(() => {
  const s = result.value?.fit_score
  if (s >= 70) return 'high'
  if (s >= 40) return 'mid'
  return 'low'
})

function prospectScoreClass(score) {
  if (score >= 70) return 'badge-green'
  if (score >= 40) return 'badge-yellow'
  return 'badge-red'
}
</script>

<style scoped>
.sales {
  padding: 36px;
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header { display: flex; justify-content: space-between; align-items: flex-start; }
.page-header-left {}
.page-header h1 { font-size: 24px; font-weight: 700; }
.subtitle { color: var(--muted); font-size: 14px; margin-top: 4px; }

.tour-launch-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: transparent;
  border: 1px solid var(--border);
  color: var(--muted);
  font-size: 13px;
  font-weight: 500;
  padding: 6px 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s;
  flex-shrink: 0;
}
.tour-launch-btn:hover { border-color: var(--primary); color: var(--primary); }

/* Form */
.research-form { display: flex; flex-direction: column; gap: 16px; }
.form-fields { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 12px; color: var(--muted); font-weight: 500; }
.optional { color: var(--border); font-weight: 400; }
.form-footer { display: flex; justify-content: space-between; align-items: center; }
.error-msg { font-size: 13px; color: var(--danger); }
.btn-sm { padding: 6px 14px; font-size: 13px; }

.spinner {
  display: inline-block;
  width: 12px; height: 12px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  margin-right: 6px;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Result grid */
.result-grid {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 16px;
  align-items: start;
}

.prospect-info { display: flex; flex-direction: column; gap: 14px; }

/* Fit card */
.fit-card {}
.fit-top { display: flex; gap: 16px; align-items: flex-start; }
.section-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px; }
.fit-score { font-size: 48px; font-weight: 800; line-height: 1; }
.fit-score.high { color: var(--success); }
.fit-score.mid { color: #fbbf24; }
.fit-score.low { color: var(--danger); }
.score-denom { font-size: 18px; font-weight: 400; color: var(--muted); }
.fit-bar-wrap { flex: 1; padding-top: 4px; }
.fit-bar { height: 6px; background: var(--border); border-radius: 10px; overflow: hidden; margin-bottom: 10px; }
.fit-bar-fill { height: 100%; border-radius: 10px; transition: width 0.6s ease; }
.fit-bar-fill.high { background: var(--success); }
.fit-bar-fill.mid { background: #fbbf24; }
.fit-bar-fill.low { background: var(--danger); }
.fit-reasoning { font-size: 13px; color: var(--muted); line-height: 1.6; }

/* Details */
.details-grid { display: flex; flex-direction: column; gap: 10px; }
.detail-item { display: flex; justify-content: space-between; align-items: center; }
.detail-label { font-size: 12px; color: var(--muted); }
.detail-value { font-size: 13px; font-weight: 500; text-transform: capitalize; }
.detail-link { font-size: 13px; color: var(--primary); word-break: break-all; }
.detail-link:hover { text-decoration: underline; }
.findings { }
.findings-list { list-style: none; display: flex; flex-direction: column; gap: 7px; margin-top: 8px; }
.findings-list li {
  font-size: 13px;
  color: var(--muted);
  padding-left: 14px;
  position: relative;
  line-height: 1.5;
}
.findings-list li::before {
  content: '·';
  position: absolute;
  left: 0;
  color: var(--primary);
  font-size: 18px;
  line-height: 1.2;
}

/* Drafts panel */
.drafts-panel { display: flex; flex-direction: column; gap: 14px; }
.drafts-header { display: flex; justify-content: space-between; align-items: center; }

.channel-tabs { display: flex; gap: 4px; }
.ch-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 13px;
  color: var(--muted);
  cursor: pointer;
  transition: all 0.15s;
}
.ch-tab:hover { color: var(--text); border-color: var(--primary); }
.ch-tab.active { background: #2d2f50; color: var(--primary); border-color: var(--primary); }

.soon-badge {
  background: var(--border);
  color: var(--muted);
  font-size: 10px;
  padding: 1px 5px;
  border-radius: 4px;
}

.draft-content { display: flex; flex-direction: column; gap: 14px; }
.draft-meta { display: flex; justify-content: space-between; align-items: flex-start; }
.draft-subject { font-size: 15px; font-weight: 600; }
.draft-actions { display: flex; align-items: center; gap: 8px; }
.draft-body {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  font-size: 14px;
  line-height: 1.8;
  white-space: pre-wrap;
  color: var(--text);
  min-height: 200px;
}
.review-note { font-size: 12px; color: var(--muted); }

/* WhatsApp preview */
.whatsapp-preview { display: flex; flex-direction: column; gap: 8px; }
.wa-bubble {
  background: #1a3a2a;
  border: 1px solid #2d5a3d;
  border-radius: 12px 12px 4px 12px;
  padding: 14px 18px;
  font-size: 14px;
  line-height: 1.6;
  color: #d1fae5;
  max-width: 380px;
}
.wa-char-count { font-size: 12px; color: var(--muted); }

/* Prospects list */
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.section-header h2 { font-size: 16px; font-weight: 600; }
.empty { color: var(--muted); font-size: 14px; text-align: center; padding: 32px; }
.prospects-list { display: flex; flex-direction: column; gap: 8px; }
.prospect-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: border-color 0.15s;
}
.prospect-row:hover { border-color: var(--primary); }
.prospect-name { font-weight: 500; font-size: 14px; }
.prospect-url { font-size: 12px; margin-top: 2px; }
.prospect-right { display: flex; gap: 8px; }
.muted { color: var(--muted); }

/* ── Tour ─────────────────────────────────────────── */
.tour-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.52);
  z-index: 300;
  backdrop-filter: blur(1px);
}

.tour-tooltip {
  position: fixed;
  z-index: 400;
  width: 300px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}

.tour-tooltip::before {
  content: '';
  position: absolute;
  width: 10px;
  height: 10px;
  background: var(--surface);
  border: 1px solid var(--border);
  transform: rotate(45deg);
}

/* Positions — anchored to the page layout */
.tour-pos-form      { top: 220px; left: 50%; transform: translateX(-50%); }
.tour-pos-form::before { top: -6px; left: 50%; margin-left: -5px; border-bottom: none; border-right: none; }

.tour-pos-form-btn  { top: 220px; right: 40px; }
.tour-pos-form-btn::before { top: -6px; right: 30px; border-bottom: none; border-right: none; }

.tour-pos-score     { top: 50%; transform: translateY(-50%); left: 50%; margin-left: -20px; }
.tour-pos-score::before { top: 20px; left: -6px; border-top: none; border-right: none; }

.tour-pos-drafts    { top: 50%; transform: translateY(-50%); right: 40px; }
.tour-pos-drafts::before { top: 20px; right: -6px; border-bottom: none; border-left: none; }

.tour-pos-prospects { bottom: 100px; left: 50%; transform: translateX(-50%); }
.tour-pos-prospects::before { bottom: -6px; left: 50%; margin-left: -5px; border-top: none; border-left: none; }

/* Tour tooltip content */
.tour-step-count { font-size: 10px; font-weight: 700; color: var(--primary); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; }
.tour-title { font-size: 15px; font-weight: 700; color: var(--text); margin-bottom: 8px; }
.tour-body  { font-size: 13px; color: var(--muted); line-height: 1.65; margin-bottom: 16px; }

.tour-actions { display: flex; align-items: center; gap: 8px; }
.tour-skip { font-size: 12px; color: var(--muted); background: transparent; padding: 0; border: none; cursor: pointer; }
.tour-skip:hover { color: var(--text); }
.tour-dots { display: flex; gap: 5px; flex: 1; justify-content: center; }
.tour-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--border); transition: background 0.2s; }
.tour-dot.active { background: var(--primary); }
.tour-next { background: var(--primary); color: #fff; font-size: 12px; font-weight: 600; padding: 6px 14px; border-radius: 7px; cursor: pointer; border: none; transition: background 0.15s; }
.tour-next:hover { background: var(--primary-hover); }

/* Highlighted elements */
.tour-highlight {
  position: relative;
  z-index: 350 !important;
  border-radius: 10px;
  animation: tour-pulse 1.5s ease-in-out infinite;
}
@keyframes tour-pulse {
  0%, 100% { box-shadow: 0 0 0 3px rgba(99,102,241,0.5), 0 0 0 7px rgba(99,102,241,0.15); }
  50%       { box-shadow: 0 0 0 5px rgba(99,102,241,0.7), 0 0 0 10px rgba(99,102,241,0.08); }
}

.fade-enter-active, .fade-leave-active     { transition: opacity 0.25s; }
.fade-enter-from,  .fade-leave-to          { opacity: 0; }
.tooltip-enter-active, .tooltip-leave-active { transition: opacity 0.2s, transform 0.2s; }
.tooltip-enter-from, .tooltip-leave-to      { opacity: 0; transform: translateY(6px) scale(0.97); }
</style>
