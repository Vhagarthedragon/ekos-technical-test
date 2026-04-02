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
    <div class="demo-banner">
      <div class="demo-banner-left">
        <span class="demo-badge">DEMO</span>
        <span class="demo-banner-text">This is a simulated ClinicDesk environment — the widget is embedded live</span>
      </div>
      <div class="demo-banner-nav">
        <RouterLink to="/support" class="demo-switcher-link">Support Agent</RouterLink>
        <RouterLink to="/sales" class="demo-switcher-link">Sales Agent</RouterLink>
        <RouterLink to="/admin" class="demo-switcher-link">Admin</RouterLink>
      </div>
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

    <!-- ── Chat widget ───────────────────────────────── -->

    <!-- Launcher button -->
    <button class="chat-launcher" @click="toggleChat" :class="{ open: isOpen }">
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
        <div class="widget-header">
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
        <div v-if="!sessionId" class="widget-start">
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
            <div class="wm-bubble">
              Hi{{ userName }}! How can I help you today?
            </div>
          </div>

          <div v-for="(msg, i) in messages" :key="i" class="wm" :class="`wm-${msg.role}`">
            <div class="wm-bubble">{{ msg.content }}</div>
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
            <button class="widget-send" @click="sendMessage" :disabled="loading || !input.trim() || escalated">
              <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                <line x1="22" y1="2" x2="11" y2="13"/>
                <polygon points="22 2 15 22 11 13 2 9 22 2"/>
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
import { ref, computed, nextTick } from 'vue'
import { support } from '../api'
import { useTheme } from '../composables/useTheme'

const { isDark, toggle } = useTheme()

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
  padding: 14px 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.wm { display: flex; flex-direction: column; max-width: 85%; }
.wm-user { align-self: flex-end; align-items: flex-end; }
.wm-assistant { align-self: flex-start; }

.wm-bubble {
  padding: 9px 13px;
  border-radius: 14px;
  font-size: 13px;
  line-height: 1.6;
  white-space: pre-wrap;
}
.wm-user .wm-bubble { background: #6366f1; color: #fff; border-bottom-right-radius: 4px; }
.wm-assistant .wm-bubble { background: var(--bg); border: 1px solid var(--border); border-bottom-left-radius: 4px; color: var(--text); }

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
  background: var(--primary);
  border-radius: 7px;
  display: flex; align-items: center; justify-content: center;
  color: #fff; flex-shrink: 0;
  transition: background 0.15s;
}
.widget-send:hover:not(:disabled) { background: var(--primary-hover); }
.widget-send:disabled { opacity: 0.4; cursor: not-allowed; }
.widget-powered { font-size: 10px; color: var(--muted); text-align: center; margin-top: 6px; }
</style>
