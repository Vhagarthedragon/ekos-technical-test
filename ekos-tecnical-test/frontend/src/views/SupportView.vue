<template>
  <!-- Simulated ClinicDesk app page (the host app) -->
  <div class="demo-page">
    <div class="demo-topbar">
      <span class="demo-logo">ClinicDesk</span>
      <div class="demo-nav">
        <span class="demo-nav-item active">Dashboard</span>
        <span class="demo-nav-item">Patients</span>
        <span class="demo-nav-item">Schedule</span>
        <span class="demo-nav-item">Billing</span>
      </div>
      <div class="demo-user">Dr. Johnson</div>
    </div>

    <div class="demo-content">
      <div class="demo-sidebar">
        <div class="demo-menu-item active">
          <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
          Overview
        </div>
        <div class="demo-menu-item">
          <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
          Patients
        </div>
        <div class="demo-menu-item">
          <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          Schedule
        </div>
        <div class="demo-menu-item">
          <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
          Billing
        </div>
      </div>

      <div class="demo-main">
        <h2 class="demo-title">Good morning, Dr. Johnson</h2>
        <p class="demo-subtitle">Wednesday, April 2 · 14 appointments today</p>
        <div class="demo-cards">
          <div class="demo-card">
            <p class="demo-card-label">Today's patients</p>
            <p class="demo-card-value">14</p>
          </div>
          <div class="demo-card">
            <p class="demo-card-label">Pending claims</p>
            <p class="demo-card-value">7</p>
          </div>
          <div class="demo-card">
            <p class="demo-card-label">Unread messages</p>
            <p class="demo-card-value">3</p>
          </div>
          <div class="demo-card">
            <p class="demo-card-label">Open invoices</p>
            <p class="demo-card-value">$4,280</p>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Demo banner ───────────────────────────────── -->
    <div class="demo-banner" :class="{ 'tour-highlight': tourActive && tourStep === 0 }">
      <div class="demo-banner-left">
        <span class="demo-badge">DEMO</span>
        <span class="demo-banner-text">This is a simulated ClinicDesk environment — the widget is embedded live</span>
      </div>
      <div class="demo-banner-nav">
        <RouterLink to="/support" class="demo-switcher-link">Support Agent</RouterLink>
        <RouterLink to="/sales" class="demo-switcher-link">Sales Agent</RouterLink>
        <RouterLink to="/admin" class="demo-switcher-link">Admin</RouterLink>
      </div>
      <button class="demo-tour-btn" @click="startTour" title="Start guided tour">
        <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/>
        </svg>
        Tour
      </button>
      <button class="demo-theme-btn" @click="toggle" :title="isDark ? 'Light mode' : 'Dark mode'">
        <svg v-if="isDark" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
          <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
        </svg>
        <svg v-else width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
      </button>
    </div>

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

    <!-- ── Chat widget ───────────────────────────────── -->

    <!-- Launcher button -->
    <button class="chat-launcher" @click="toggleChat" :class="{ open: isOpen, 'tour-highlight': tourActive && tourStep === 1 }">
      <svg v-if="!isOpen" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
      <svg v-else width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
        <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
      </svg>
      <span v-if="unread > 0 && !isOpen" class="launcher-badge">{{ unread }}</span>
    </button>

    <!-- Chat panel -->
    <Transition name="widget">
      <div v-if="isOpen" class="chat-widget">

        <!-- Widget header -->
        <div class="widget-header" :class="{ 'tour-highlight-inner': tourActive && tourStep === 2 }">
          <div class="widget-header-left">
            <div class="widget-avatar">AI</div>
            <div>
              <p class="widget-title">ClinicDesk Support</p>
              <p class="widget-status">
                <span class="status-dot" :class="{ escalated }"></span>
                {{ escalated ? 'Escalated' : 'Online' }}
              </p>
            </div>
          </div>
          <button class="widget-close" @click="isOpen = false">
            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
              <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <!-- Start screen inside widget -->
        <div v-if="!sessionId" class="widget-start" :class="{ 'tour-highlight-inner': tourActive && tourStep === 3 }">
          <p class="widget-greeting">Hi there! 👋</p>
          <p class="widget-desc">Ask anything about ClinicDesk — billing, scheduling, insurance, or your account.</p>
          <input
            v-model="userIdentifier"
            placeholder="Your email or name"
            class="widget-input"
            @keyup.enter="startSession"
          />
          <button class="widget-btn" @click="startSession" :disabled="!userIdentifier.trim()">
            Start conversation
          </button>
          <div class="widget-suggestions">
            <p class="suggestions-label">Common questions</p>
            <button v-for="q in suggestions" :key="q" class="suggestion-chip" @click="quickStart(q)">
              {{ q }}
            </button>
          </div>
        </div>

        <!-- Messages -->
        <div v-else class="widget-messages" ref="messagesEl">
          <div class="wm wm-assistant">
            <div class="wm-bubble" v-html="md('Hi' + userName + '! How can I help you today?')"></div>
          </div>

          <div v-for="(msg, i) in messages" :key="i" class="wm" :class="`wm-${msg.role}`">
            <div class="wm-bubble" v-html="md(msg.content)"></div>
            <div v-if="msg.escalated" class="wm-escalated">
              ⚠ Escalated to a human agent
            </div>
          </div>

          <div v-if="loading" class="wm wm-assistant">
            <div class="wm-bubble wm-typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div v-if="sessionId" class="widget-input-area">
          <div v-if="escalated" class="widget-escalated-note">
            A human will follow up with you shortly.
          </div>
          <div class="widget-input-row">
            <input
              v-model="input"
              placeholder="Type a message..."
              class="widget-text-input"
              @keyup.enter="sendMessage"
              :disabled="loading || escalated"
              ref="inputEl"
            />
            <button class="widget-send" @click="sendMessage" :disabled="loading || !input.trim() || escalated" :class="{ 'widget-send-active': input.trim() && !loading && !escalated }">
              <!-- paper-plane send icon, all fill -->
              <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path d="M3.4 20.4l17.45-7.48a1 1 0 000-1.84L3.4 3.6a1 1 0 00-1.39 1.06L3.5 11h8.5a.5.5 0 010 1H3.5l-1.49 6.34A1 1 0 003.4 20.4z"/>
              </svg>
            </button>
          </div>
          <p class="widget-powered">Powered by ClinicDesk AI</p>
        </div>

      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'
import { support } from '../api'
import { useTheme } from '../composables/useTheme'

const { isDark, toggle } = useTheme()

// ── Tour ──────────────────────────────────────────────
const STEPS = [
  {
    pos: 'banner',
    title: 'Simulated host app',
    body: 'This dashboard mimics a real ClinicDesk installation. In production the widget loads via a single <script> tag — no changes to the host app needed.',
  },
  {
    pos: 'launcher',
    title: 'The chat launcher',
    body: 'A floating button injected into the bottom-right corner of any page. Click it to open the support widget. Unread replies show a badge.',
  },
  {
    pos: 'widget-top',
    title: 'Widget header',
    body: 'Shows the agent name and live status. Turns amber when a conversation is escalated to a human agent.',
  },
  {
    pos: 'widget-body',
    title: 'Patient-facing chat',
    body: 'Patients type a question or pick a suggestion. The AI searches the knowledge base using RAG and replies in under 2 seconds.',
  },
]

const tourActive = ref(false)
const tourStep = ref(0)

function startTour() {
  tourStep.value = 0
  tourActive.value = true
  // make sure widget is closed so step 1 (launcher) is visible
  isOpen.value = false
}

function advanceTour() {
  if (tourStep.value < STEPS.length - 1) {
    tourStep.value++
    // auto-open widget when reaching widget steps
    if (tourStep.value >= 2) isOpen.value = true
  } else {
    endTour()
  }
}

function endTour() {
  tourActive.value = false
  localStorage.setItem('tourSeen', '1')
}

onMounted(() => {
  if (!localStorage.getItem('tourSeen')) {
    setTimeout(startTour, 800)
  }
})

// ── Chat ─────────────────────────────────────────────
const suggestions = [
  'How do I submit a claim?',
  'Set up a payment plan',
  'Verify insurance eligibility',
]

const isOpen = ref(false)
const unread = ref(0)
const userIdentifier = ref('')
const sessionId = ref(null)
const messages = ref([])
const input = ref('')
const loading = ref(false)
const escalated = ref(false)
const messagesEl = ref(null)

const userName = computed(() => {
  const id = userIdentifier.value
  if (!id) return ''
  return ` ${id.includes('@') ? id.split('@')[0] : id.split(' ')[0]}`
})

function toggleChat() {
  isOpen.value = !isOpen.value
  if (isOpen.value) unread.value = 0
}

async function startSession() {
  if (!userIdentifier.value.trim()) return
  const res = await support.startSession(userIdentifier.value.trim())
  sessionId.value = res.data.session_id
}

async function quickStart(question) {
  if (!userIdentifier.value.trim()) userIdentifier.value = 'guest'
  await startSession()
  input.value = question
  await sendMessage()
}

async function sendMessage() {
  const text = input.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true
  await scrollDown()

  try {
    const res = await support.chat(sessionId.value, text)
    messages.value.push({ role: 'assistant', content: res.data.reply, escalated: res.data.escalated })
    if (res.data.escalated) escalated.value = true
    if (!isOpen.value) unread.value++
  } catch {
    messages.value.push({ role: 'assistant', content: 'Something went wrong. Please try again.' })
  } finally {
    loading.value = false
    await scrollDown()
  }
}

async function scrollDown() {
  await nextTick()
  if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight
}

// Lightweight markdown → HTML (bold, italic, code, numbered + bullet lists, line breaks)
function md(text) {
  if (!text) return ''

  // Escape HTML first to prevent XSS
  let s = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

  // Block: numbered list  (1. item\n2. item)
  s = s.replace(/((?:^\d+\..+\n?)+)/gm, (block) => {
    const items = block.trim().split('\n').map(l => `<li>${l.replace(/^\d+\.\s*/, '')}</li>`).join('')
    return `<ol>${items}</ol>`
  })

  // Block: bullet list  (- item or * item)
  s = s.replace(/((?:^[-*]\s.+\n?)+)/gm, (block) => {
    const items = block.trim().split('\n').map(l => `<li>${l.replace(/^[-*]\s/, '')}</li>`).join('')
    return `<ul>${items}</ul>`
  })

  // Inline: **bold**
  s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')

  // Inline: *italic*
  s = s.replace(/\*(.+?)\*/g, '<em>$1</em>')

  // Inline: `code`
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>')

  // Line breaks (not inside list tags)
  s = s.replace(/\n/g, '<br>')

  return s
}
</script>

<style scoped>
/* ── Demo page (simulated ClinicDesk) ─────────── */
.demo-page {
  width: 100%;
  height: 100vh;
  padding-top: 36px; /* banner height */
  background: var(--bg);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.demo-topbar {
  height: 52px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 0 20px;
  gap: 32px;
  flex-shrink: 0;
}
.demo-logo { font-weight: 700; font-size: 15px; color: var(--text); }
.demo-nav { display: flex; gap: 4px; }
.demo-nav-item { padding: 5px 12px; border-radius: 6px; font-size: 13px; color: var(--muted); cursor: default; }
.demo-nav-item.active { background: var(--border); color: var(--text); }
.demo-user { margin-left: auto; font-size: 13px; color: var(--muted); }

.demo-content { display: flex; flex: 1; overflow: hidden; }

.demo-sidebar {
  width: 200px;
  background: var(--surface);
  border-right: 1px solid var(--border);
  padding: 16px 10px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex-shrink: 0;
}
.demo-menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 12px;
  border-radius: 7px;
  font-size: 13px;
  color: var(--muted);
  cursor: default;
}
.demo-menu-item.active { background: var(--border); color: var(--text); }

.demo-main { flex: 1; padding: 32px; }
.demo-title { font-size: 22px; font-weight: 700; color: var(--text); }
.demo-subtitle { font-size: 13px; color: var(--muted); margin-top: 4px; margin-bottom: 28px; }
.demo-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
.demo-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px 20px;
}
.demo-card-label { font-size: 12px; color: var(--muted); margin-bottom: 8px; }
.demo-card-value { font-size: 28px; font-weight: 700; color: var(--text); }

/* ── Demo banner ──────────────────────────────── */
.demo-banner {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 36px;
  background: #6366f1;
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 14px;
  z-index: 200;
  flex-shrink: 0;
}

.demo-banner-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 0;
}

.demo-badge {
  background: rgba(255,255,255,0.25);
  color: #fff;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.12em;
  padding: 2px 8px;
  border-radius: 4px;
  flex-shrink: 0;
}

.demo-banner-text {
  font-size: 12px;
  color: rgba(255,255,255,0.85);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.demo-banner-nav {
  display: flex;
  align-items: center;
  gap: 2px;
  flex-shrink: 0;
}

.demo-switcher-link {
  font-size: 12px;
  font-weight: 500;
  color: rgba(255,255,255,0.7);
  padding: 4px 10px;
  border-radius: 6px;
  transition: all 0.15s;
  text-decoration: none;
}
.demo-switcher-link:hover { color: #fff; background: rgba(255,255,255,0.15); }
.demo-switcher-link.router-link-active { color: #fff; background: rgba(255,255,255,0.2); font-weight: 600; }

.demo-theme-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: transparent;
  border: none;
  color: rgba(255,255,255,0.75);
  padding: 0;
  cursor: pointer;
  transition: all 0.15s;
  flex-shrink: 0;
}
.demo-theme-btn:hover { background: rgba(255,255,255,0.15); color: #fff; }

.demo-tour-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  background: rgba(255,255,255,0.18);
  border: 1px solid rgba(255,255,255,0.3);
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s;
  flex-shrink: 0;
}
.demo-tour-btn:hover { background: rgba(255,255,255,0.28); }

/* ── Launcher button ──────────────────────────── */
.chat-launcher {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #6366f1;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.5);
  transition: transform 0.2s, background 0.2s;
  z-index: 100;
  cursor: pointer;
}
.chat-launcher:hover { transform: scale(1.08); background: #4f52d4; }
.chat-launcher.open { background: #3d3f6e; }

.launcher-badge {
  position: absolute;
  top: -3px;
  right: -3px;
  background: #ef4444;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ── Chat widget panel ────────────────────────── */
.chat-widget {
  position: fixed;
  bottom: 88px;
  right: 24px;
  width: 360px;
  height: 520px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 99;
}

.widget-enter-active, .widget-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}
.widget-enter-from, .widget-leave-to {
  opacity: 0;
  transform: translateY(16px) scale(0.97);
}

/* Widget header */
.widget-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  background: #6366f1;
  flex-shrink: 0;
}
.widget-header-left { display: flex; align-items: center; gap: 10px; }
.widget-avatar {
  width: 34px; height: 34px;
  background: rgba(255,255,255,0.2);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 700; color: #fff;
}
.widget-title { font-size: 14px; font-weight: 600; color: #fff; }
.widget-status { font-size: 11px; color: rgba(255,255,255,0.75); display: flex; align-items: center; gap: 4px; margin-top: 1px; }
.status-dot { width: 6px; height: 6px; background: #4ade80; border-radius: 50%; }
.status-dot.escalated { background: #fbbf24; }
.widget-close { color: rgba(255,255,255,0.8); background: transparent; padding: 4px; border-radius: 6px; }
.widget-close:hover { background: rgba(255,255,255,0.1); color: #fff; }

/* Start screen */
.widget-start {
  flex: 1;
  padding: 20px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
}
.widget-greeting { font-size: 18px; font-weight: 700; color: var(--text); }
.widget-desc { font-size: 13px; color: var(--muted); line-height: 1.6; }
.widget-input {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text);
  font-size: 13px;
  padding: 9px 12px;
  width: 100%;
  outline: none;
  margin-top: 4px;
}
.widget-input:focus { border-color: var(--primary); }
.widget-btn {
  background: #6366f1;
  color: #fff;
  border-radius: 8px;
  padding: 10px;
  font-size: 13px;
  font-weight: 600;
  width: 100%;
  cursor: pointer;
  transition: background 0.15s;
}
.widget-btn:hover:not(:disabled) { background: #4f52d4; }
.widget-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.widget-suggestions { margin-top: 4px; }
.suggestions-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px; }
.suggestion-chip {
  display: block;
  width: 100%;
  text-align: left;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 12px;
  color: var(--text);
  margin-bottom: 6px;
  cursor: pointer;
  transition: border-color 0.15s;
}
.suggestion-chip:hover { border-color: var(--primary); color: var(--primary); }

/* Messages */
.widget-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px 14px 8px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.wm { display: flex; flex-direction: column; max-width: 88%; }
.wm-user { align-self: flex-end; align-items: flex-end; }
.wm-assistant { align-self: flex-start; }

.wm-bubble {
  padding: 10px 14px;
  border-radius: 14px;
  font-size: 13px;
  line-height: 1.65;
}
.wm-user .wm-bubble { background: #6366f1; color: #fff; border-bottom-right-radius: 4px; }
.wm-assistant .wm-bubble { background: var(--bg); border: 1px solid var(--border); border-bottom-left-radius: 4px; color: var(--text); }

/* Markdown inside assistant bubbles */
.wm-assistant .wm-bubble strong { font-weight: 700; color: var(--text); }
.wm-assistant .wm-bubble em { font-style: italic; }
.wm-assistant .wm-bubble code {
  background: var(--border);
  border-radius: 4px;
  padding: 1px 6px;
  font-family: ui-monospace, monospace;
  font-size: 11.5px;
}
.wm-assistant .wm-bubble ol,
.wm-assistant .wm-bubble ul {
  padding-left: 20px;
  margin: 8px 0 4px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.wm-assistant .wm-bubble ol { list-style: decimal; }
.wm-assistant .wm-bubble ul { list-style: disc; }
.wm-assistant .wm-bubble li { line-height: 1.55; padding-left: 2px; }
/* Space after a heading-like bold before a list */
.wm-assistant .wm-bubble br + ol,
.wm-assistant .wm-bubble br + ul { margin-top: 4px; }

.wm-escalated { font-size: 11px; color: #d97706; margin-top: 4px; padding-left: 2px; }

.wm-typing { display: flex; gap: 4px; align-items: center; padding: 12px 14px; }
.wm-typing span {
  width: 6px; height: 6px; background: var(--muted);
  border-radius: 50%; animation: bounce 1s infinite;
}
.wm-typing span:nth-child(2) { animation-delay: 0.15s; }
.wm-typing span:nth-child(3) { animation-delay: 0.3s; }
@keyframes bounce { 0%,60%,100% { transform: translateY(0); } 30% { transform: translateY(-5px); } }

/* Input area */
.widget-input-area {
  border-top: 1px solid var(--border);
  padding: 10px 12px 8px;
  flex-shrink: 0;
}
.widget-escalated-note {
  background: color-mix(in srgb, #f59e0b 12%, transparent);
  border: 1px solid color-mix(in srgb, #f59e0b 30%, transparent);
  color: #d97706;
  font-size: 11px;
  padding: 6px 10px;
  border-radius: 6px;
  margin-bottom: 8px;
  text-align: center;
}
.widget-input-row {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 7px 8px 7px 12px;
}
.widget-input-row:focus-within { border-color: var(--primary); }
.widget-text-input {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--text);
  font-size: 13px;
  outline: none;
}
.widget-send {
  width: 30px; height: 30px;
  background: var(--border);
  border-radius: 7px;
  display: flex; align-items: center; justify-content: center;
  color: var(--muted); flex-shrink: 0;
  transition: all 0.15s;
  cursor: not-allowed;
}
.widget-send-active {
  background: var(--primary) !important;
  color: #fff !important;
  cursor: pointer !important;
}
.widget-send-active:hover { background: var(--primary-hover) !important; transform: scale(1.05); }
.widget-powered { font-size: 10px; color: var(--muted); text-align: center; margin-top: 6px; }

/* ── Tour ─────────────────────────────────────────── */
.tour-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  z-index: 300;
  backdrop-filter: blur(1px);
}

/* Tooltip card */
.tour-tooltip {
  position: fixed;
  z-index: 400;
  width: 300px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}

/* Arrow shared */
.tour-tooltip::before {
  content: '';
  position: absolute;
  width: 10px;
  height: 10px;
  background: var(--surface);
  border: 1px solid var(--border);
  transform: rotate(45deg);
}

/* Positions */
.tour-pos-banner    { top: 52px; left: 50%; transform: translateX(-50%); }
.tour-pos-banner::before { top: -6px; left: 50%; margin-left: -5px; border-bottom: none; border-right: none; }

.tour-pos-launcher  { bottom: 108px; right: 24px; }
.tour-pos-launcher::before { bottom: -6px; right: 30px; border-top: none; border-left: none; }

.tour-pos-widget-top { bottom: 420px; right: 396px; }
.tour-pos-widget-top::before { top: 20px; right: -6px; border-bottom: none; border-left: none; }

.tour-pos-widget-body { bottom: 200px; right: 396px; }
.tour-pos-widget-body::before { bottom: 30px; right: -6px; border-bottom: none; border-left: none; }

/* Content */
.tour-step-count {
  font-size: 10px;
  font-weight: 700;
  color: var(--primary);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 8px;
}
.tour-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 8px;
}
.tour-body {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.65;
  margin-bottom: 16px;
}
.tour-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}
.tour-skip {
  font-size: 12px;
  color: var(--muted);
  background: transparent;
  padding: 0;
  border: none;
  cursor: pointer;
}
.tour-skip:hover { color: var(--text); }
.tour-dots {
  display: flex;
  gap: 5px;
  flex: 1;
  justify-content: center;
}
.tour-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--border);
  transition: background 0.2s;
}
.tour-dot.active { background: var(--primary); }
.tour-next {
  background: var(--primary);
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 7px;
  cursor: pointer;
  border: none;
  transition: background 0.15s;
}
.tour-next:hover { background: var(--primary-hover); }

/* Highlighted elements float above overlay */
.tour-highlight {
  position: relative;
  z-index: 350 !important;
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.6), 0 0 0 8px rgba(99, 102, 241, 0.2);
  border-radius: 4px;
  animation: tour-pulse 1.5s ease-in-out infinite;
}
.tour-highlight-inner {
  position: relative;
  z-index: 350 !important;
  outline: 3px solid rgba(99, 102, 241, 0.7);
  outline-offset: -1px;
  animation: tour-pulse 1.5s ease-in-out infinite;
}
@keyframes tour-pulse {
  0%, 100% { box-shadow: 0 0 0 4px rgba(99,102,241,0.5), 0 0 0 8px rgba(99,102,241,0.15); }
  50%       { box-shadow: 0 0 0 6px rgba(99,102,241,0.7), 0 0 0 12px rgba(99,102,241,0.1); }
}

/* Transitions */
.fade-enter-active, .fade-leave-active   { transition: opacity 0.25s; }
.fade-enter-from,  .fade-leave-to        { opacity: 0; }
.tooltip-enter-active, .tooltip-leave-active { transition: opacity 0.2s, transform 0.2s; }
.tooltip-enter-from, .tooltip-leave-to   { opacity: 0; transform: translateY(6px) scale(0.97); }
</style>
