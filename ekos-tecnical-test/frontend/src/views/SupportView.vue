<template>
  <!-- Start screen -->
  <div v-if="!sessionId" class="start-screen">
    <div class="start-card">
      <div class="brand-icon">
        <svg width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
      </div>
      <h1>ClinicDesk Support</h1>
      <p>Ask anything about scheduling, billing, insurance, or your account.</p>
      <div class="start-form">
        <input
          v-model="userIdentifier"
          placeholder="Your email or name"
          @keyup.enter="startSession"
          autofocus
        />
        <button class="btn-primary" @click="startSession" :disabled="!userIdentifier.trim()">
          Start chat
        </button>
      </div>
      <div class="suggestions">
        <p class="suggestions-label">Common questions</p>
        <div class="chips">
          <button class="chip" v-for="q in suggestions" :key="q" @click="quickStart(q)">{{ q }}</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Chat screen -->
  <div v-else class="chat-layout">
    <!-- Chat header -->
    <div class="chat-header">
      <div class="chat-header-left">
        <div class="agent-avatar">AI</div>
        <div>
          <p class="agent-name">ClinicDesk Support</p>
          <p class="agent-status">
            <span class="status-dot" :class="{ escalated }"></span>
            {{ escalated ? 'Escalated to human agent' : 'Online' }}
          </p>
        </div>
      </div>
      <button class="btn-ghost new-chat-btn" @click="resetChat">
        <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path d="M12 5v14M5 12h14"/>
        </svg>
        New chat
      </button>
    </div>

    <!-- Messages -->
    <div class="messages" ref="messagesEl">
      <!-- Welcome message -->
      <div class="message assistant">
        <div class="avatar">AI</div>
        <div class="bubble-wrap">
          <div class="bubble">
            Hi{{ userIdentifier ? ` ${userIdentifier.split('@')[0]}` : '' }}! I'm your ClinicDesk support assistant.
            What can I help you with today?
          </div>
        </div>
      </div>

      <div v-for="(msg, i) in messages" :key="i" class="message" :class="msg.role">
        <div v-if="msg.role === 'assistant'" class="avatar">AI</div>
        <div class="bubble-wrap">
          <div class="bubble">{{ msg.content }}</div>
          <div v-if="msg.escalated" class="escalation-tag">
            <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
            Escalated to human agent
          </div>
        </div>
        <div v-if="msg.role === 'user'" class="avatar user-avatar">{{ initials }}</div>
      </div>

      <!-- Typing indicator -->
      <div v-if="loading" class="message assistant">
        <div class="avatar">AI</div>
        <div class="bubble-wrap">
          <div class="bubble typing">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Input area -->
    <div class="input-area">
      <div v-if="escalated" class="escalated-banner">
        A human agent will follow up with you shortly.
      </div>
      <div class="input-row">
        <textarea
          v-model="input"
          placeholder="Message ClinicDesk Support..."
          rows="1"
          @keydown.enter.exact.prevent="sendMessage"
          @input="autoResize"
          ref="inputEl"
          :disabled="loading || escalated"
        />
        <button class="send-btn" @click="sendMessage" :disabled="loading || !input.trim() || escalated">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
            <line x1="22" y1="2" x2="11" y2="13"/>
            <polygon points="22 2 15 22 11 13 2 9 22 2"/>
          </svg>
        </button>
      </div>
      <p class="input-hint">Press Enter to send · Shift+Enter for new line</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { support } from '../api'

const suggestions = [
  'How do I submit an insurance claim?',
  'Set up a payment plan',
  'Verify patient eligibility',
  'Schedule a new patient',
]

const userIdentifier = ref('')
const sessionId = ref(null)
const messages = ref([])
const input = ref('')
const loading = ref(false)
const escalated = ref(false)
const messagesEl = ref(null)
const inputEl = ref(null)

const initials = computed(() => {
  const id = userIdentifier.value
  if (!id) return 'U'
  if (id.includes('@')) return id[0].toUpperCase()
  return id.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
})

async function startSession() {
  if (!userIdentifier.value.trim()) return
  const res = await support.startSession(userIdentifier.value.trim())
  sessionId.value = res.data.session_id
}

async function quickStart(question) {
  if (!userIdentifier.value.trim()) {
    userIdentifier.value = 'guest'
  }
  await startSession()
  input.value = question
  await sendMessage()
}

async function sendMessage() {
  const text = input.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', content: text })
  input.value = ''
  if (inputEl.value) inputEl.value.style.height = 'auto'
  loading.value = true
  await scrollDown()

  try {
    const res = await support.chat(sessionId.value, text)
    messages.value.push({ role: 'assistant', content: res.data.reply, escalated: res.data.escalated })
    if (res.data.escalated) escalated.value = true
  } catch {
    messages.value.push({ role: 'assistant', content: 'Something went wrong. Please try again.' })
  } finally {
    loading.value = false
    await scrollDown()
  }
}

function resetChat() {
  sessionId.value = null
  messages.value = []
  input.value = ''
  escalated.value = false
  userIdentifier.value = ''
}

function autoResize(e) {
  const el = e.target
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 140) + 'px'
}

async function scrollDown() {
  await nextTick()
  if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight
}
</script>

<style scoped>
/* ── Start screen ─────────────────────────────── */
.start-screen {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 24px;
}

.start-card {
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 8px;
}

.brand-icon {
  width: 56px;
  height: 56px;
  background: #2d2f50;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
  margin-bottom: 8px;
}

.start-card h1 { font-size: 26px; font-weight: 700; }
.start-card p { color: var(--muted); font-size: 15px; margin-bottom: 8px; }

.start-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 8px;
}
.start-form .btn-primary { padding: 12px; font-size: 15px; }

.suggestions { width: 100%; margin-top: 24px; }
.suggestions-label { font-size: 12px; color: var(--muted); margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.06em; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }
.chip {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 13px;
  color: var(--text);
  cursor: pointer;
  transition: all 0.15s;
}
.chip:hover { border-color: var(--primary); color: var(--primary); }

/* ── Chat layout ──────────────────────────────── */
.chat-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 24px;
  border-bottom: 1px solid var(--border);
  background: var(--surface);
  flex-shrink: 0;
}

.chat-header-left { display: flex; align-items: center; gap: 12px; }

.agent-avatar {
  width: 38px;
  height: 38px;
  background: var(--primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
}

.agent-name { font-size: 14px; font-weight: 600; }
.agent-status { font-size: 12px; color: var(--muted); display: flex; align-items: center; gap: 5px; margin-top: 1px; }

.status-dot {
  width: 7px; height: 7px;
  background: var(--success);
  border-radius: 50%;
}
.status-dot.escalated { background: #fbbf24; }

.new-chat-btn { font-size: 13px; display: flex; align-items: center; gap: 6px; }

/* ── Messages ─────────────────────────────────── */
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 28px 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  max-width: 76%;
}
.message.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}
.message.assistant { align-self: flex-start; }

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.user-avatar { background: #3d4060; }

.bubble-wrap { display: flex; flex-direction: column; gap: 4px; }

.bubble {
  padding: 11px 16px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.65;
  white-space: pre-wrap;
}
.user .bubble {
  background: var(--primary);
  color: #fff;
  border-bottom-right-radius: 5px;
}
.assistant .bubble {
  background: var(--surface);
  border: 1px solid var(--border);
  border-bottom-left-radius: 5px;
}

.escalation-tag {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #fbbf24;
  padding-left: 4px;
}

.typing { display: flex; gap: 5px; align-items: center; padding: 14px 18px; }
.typing span {
  width: 7px; height: 7px;
  background: var(--muted);
  border-radius: 50%;
  animation: bounce 1.1s infinite ease-in-out;
}
.typing span:nth-child(2) { animation-delay: 0.18s; }
.typing span:nth-child(3) { animation-delay: 0.36s; }
@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
  30% { transform: translateY(-6px); opacity: 1; }
}

/* ── Input area ───────────────────────────────── */
.input-area {
  border-top: 1px solid var(--border);
  background: var(--surface);
  padding: 14px 20px 10px;
  flex-shrink: 0;
}

.escalated-banner {
  background: #422006;
  border: 1px solid #78350f;
  color: #fbbf24;
  font-size: 13px;
  padding: 8px 14px;
  border-radius: 8px;
  margin-bottom: 10px;
  text-align: center;
}

.input-row {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 10px 10px 10px 16px;
  transition: border-color 0.15s;
}
.input-row:focus-within { border-color: var(--primary); }

textarea {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--text);
  font-family: var(--font);
  font-size: 14px;
  line-height: 1.6;
  resize: none;
  outline: none;
  padding: 0;
  max-height: 140px;
  width: 0;
}

.send-btn {
  width: 36px;
  height: 36px;
  background: var(--primary);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #fff;
  transition: background 0.15s, transform 0.1s;
}
.send-btn:hover:not(:disabled) { background: var(--primary-hover); }
.send-btn:active:not(:disabled) { transform: scale(0.93); }
.send-btn:disabled { opacity: 0.4; cursor: not-allowed; }

.input-hint { font-size: 11px; color: var(--muted); margin-top: 7px; text-align: center; }
</style>
