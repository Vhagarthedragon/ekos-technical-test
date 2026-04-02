<template>
  <div class="admin">
    <div class="admin-header">
      <h1>Admin Dashboard</h1>
      <div class="tabs">
        <button v-for="t in tabs" :key="t.id" class="tab" :class="{ active: tab === t.id }" @click="tab = t.id">
          {{ t.label }}
        </button>
      </div>
    </div>

    <!-- Overview -->
    <div v-if="tab === 'overview'" class="tab-content">
      <div class="stats-grid">
        <div class="card stat-card">
          <p class="stat-label">Support Sessions</p>
          <p class="stat-value">{{ stats.total_sessions ?? '—' }}</p>
        </div>
        <div class="card stat-card">
          <p class="stat-label">Escalations</p>
          <p class="stat-value escalated">{{ stats.escalations ?? '—' }}</p>
        </div>
        <div class="card stat-card">
          <p class="stat-label">Prospects Researched</p>
          <p class="stat-value">{{ stats.prospects ?? '—' }}</p>
        </div>
        <div class="card stat-card">
          <p class="stat-label">Drafts Pending Approval</p>
          <p class="stat-value pending">{{ stats.drafts_pending_approval ?? '—' }}</p>
        </div>
        <div class="card stat-card">
          <p class="stat-label">Knowledge Articles</p>
          <p class="stat-value">{{ stats.knowledge_articles ?? '—' }}</p>
        </div>
      </div>
    </div>

    <!-- Sessions -->
    <div v-if="tab === 'sessions'" class="tab-content">
      <div v-if="sessions.length === 0" class="empty">No sessions yet.</div>
      <div v-else class="table-wrap card">
        <table>
          <thead>
            <tr>
              <th>User</th>
              <th>Status</th>
              <th>Messages</th>
              <th>Started</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in sessions" :key="s.id">
              <td>{{ s.user_identifier }}</td>
              <td><span class="badge" :class="statusBadge(s.status)">{{ s.status }}</span></td>
              <td>{{ s.message_count }}</td>
              <td>{{ formatDate(s.created_at) }}</td>
              <td><button class="btn-ghost btn-sm" @click="openSession(s.id)">View</button></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Session detail drawer -->
      <div v-if="activeSession" class="drawer">
        <div class="drawer-header">
          <div>
            <p class="drawer-title">{{ activeSession.user_identifier }}</p>
            <span class="badge" :class="statusBadge(activeSession.status)">{{ activeSession.status }}</span>
          </div>
          <button class="btn-ghost" @click="activeSession = null">✕</button>
        </div>
        <div class="drawer-messages">
          <div v-for="(m, i) in activeSession.messages" :key="i" class="dm" :class="m.role">
            <div class="dm-bubble">{{ m.content }}</div>
            <span class="dm-time">{{ formatDate(m.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Escalations -->
    <div v-if="tab === 'escalations'" class="tab-content">
      <div v-if="escalations.length === 0" class="empty">No escalations.</div>
      <div v-else class="table-wrap card">
        <table>
          <thead>
            <tr>
              <th>User</th>
              <th>Messages</th>
              <th>Escalated at</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="e in escalations" :key="e.id">
              <td>{{ e.user_identifier }}</td>
              <td>{{ e.message_count }}</td>
              <td>{{ formatDate(e.updated_at) }}</td>
              <td><button class="btn-ghost btn-sm" @click="openSession(e.id)">View</button></td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="activeSession" class="drawer">
        <div class="drawer-header">
          <div>
            <p class="drawer-title">{{ activeSession.user_identifier }}</p>
            <span class="badge badge-yellow">escalated</span>
          </div>
          <button class="btn-ghost" @click="activeSession = null">✕</button>
        </div>
        <div class="drawer-messages">
          <div v-for="(m, i) in activeSession.messages" :key="i" class="dm" :class="m.role">
            <div class="dm-bubble">{{ m.content }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Knowledge Base -->
    <div v-if="tab === 'kb'" class="tab-content">
      <div class="kb-header">
        <span class="muted">{{ articles.length }} articles</span>
        <button class="btn-primary" @click="showNewArticle = true">+ New article</button>
      </div>

      <div v-if="showNewArticle" class="card new-article-form">
        <h3>New article</h3>
        <input v-model="newArticle.title" placeholder="Title" style="margin-bottom:10px" />
        <div style="display:flex;gap:10px;margin-bottom:10px">
          <select v-model="newArticle.category" style="flex:1;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);color:var(--text);padding:10px 14px;font-size:14px">
            <option value="billing">Billing</option>
            <option value="scheduling">Scheduling</option>
            <option value="insurance">Insurance</option>
            <option value="general">General</option>
          </select>
        </div>
        <textarea v-model="newArticle.content" rows="6" placeholder="Article content..." style="margin-bottom:10px" />
        <div style="display:flex;gap:10px;justify-content:flex-end">
          <button class="btn-ghost" @click="showNewArticle = false">Cancel</button>
          <button class="btn-primary" @click="saveArticle">Save</button>
        </div>
      </div>

      <div class="table-wrap card" v-if="articles.length > 0">
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Category</th>
              <th>Tags</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in articles" :key="a.id">
              <td>{{ a.title }}</td>
              <td><span class="badge badge-blue">{{ a.category }}</span></td>
              <td class="muted" style="font-size:12px">{{ a.tags?.join(', ') }}</td>
              <td><button class="btn-ghost btn-sm" @click="deleteArticle(a.id)">Delete</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { admin } from '../api'

const tab = ref('overview')
const tabs = [
  { id: 'overview', label: 'Overview' },
  { id: 'sessions', label: 'Sessions' },
  { id: 'escalations', label: 'Escalations' },
  { id: 'kb', label: 'Knowledge Base' },
]

const stats = ref({})
const sessions = ref([])
const escalations = ref([])
const articles = ref([])
const activeSession = ref(null)
const showNewArticle = ref(false)
const newArticle = ref({ title: '', content: '', category: 'billing' })

onMounted(() => loadTab('overview'))

watch(tab, (t) => loadTab(t))

async function loadTab(t) {
  if (t === 'overview') stats.value = (await admin.stats()).data
  if (t === 'sessions') sessions.value = (await admin.sessions()).data
  if (t === 'escalations') escalations.value = (await admin.escalations()).data
  if (t === 'kb') articles.value = (await admin.articles()).data
}

async function openSession(id) {
  activeSession.value = (await admin.session(id)).data
}

async function saveArticle() {
  await admin.createArticle(newArticle.value)
  newArticle.value = { title: '', content: '', category: 'billing' }
  showNewArticle.value = false
  articles.value = (await admin.articles()).data
  stats.value = (await admin.stats()).data
}

async function deleteArticle(id) {
  await admin.deleteArticle(id)
  articles.value = articles.value.filter(a => a.id !== id)
  stats.value = (await admin.stats()).data
}

function statusBadge(status) {
  if (status === 'escalated') return 'badge-yellow'
  if (status === 'resolved') return 'badge-green'
  return 'badge-blue'
}

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.admin { padding: 36px; max-width: 1000px; margin: 0 auto; }

.admin-header { margin-bottom: 28px; }
.admin-header h1 { font-size: 24px; font-weight: 700; margin-bottom: 16px; }

.tabs { display: flex; gap: 4px; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 4px; width: fit-content; }
.tab { background: transparent; color: var(--muted); padding: 7px 16px; border-radius: 7px; font-size: 13px; font-weight: 500; }
.tab:hover { color: var(--text); }
.tab.active { background: var(--border); color: var(--text); }

.tab-content { display: flex; flex-direction: column; gap: 16px; }

.stats-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 14px; }
.stat-card { text-align: center; padding: 24px 16px; }
.stat-label { font-size: 12px; color: var(--muted); margin-bottom: 8px; }
.stat-value { font-size: 36px; font-weight: 800; color: var(--text); }
.stat-value.escalated { color: #fbbf24; }
.stat-value.pending { color: var(--primary); }

.table-wrap { padding: 0; overflow: hidden; }
table { width: 100%; border-collapse: collapse; }
th { font-size: 12px; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border); }
td { padding: 12px 16px; font-size: 14px; border-bottom: 1px solid var(--border); }
tr:last-child td { border-bottom: none; }
tr:hover td { background: rgba(255,255,255,0.02); }

.btn-sm { padding: 4px 10px; font-size: 12px; }
.muted { color: var(--muted); }
.empty { color: var(--muted); font-size: 14px; text-align: center; padding: 40px; }

.drawer { margin-top: 16px; background: var(--surface); border: 1px solid var(--primary); border-radius: var(--radius); overflow: hidden; }
.drawer-header { display: flex; justify-content: space-between; align-items: flex-start; padding: 16px 20px; border-bottom: 1px solid var(--border); }
.drawer-title { font-weight: 600; margin-bottom: 4px; }
.drawer-messages { padding: 16px 20px; display: flex; flex-direction: column; gap: 12px; max-height: 400px; overflow-y: auto; }
.dm { display: flex; flex-direction: column; max-width: 75%; }
.dm.user { align-self: flex-end; align-items: flex-end; }
.dm.assistant { align-self: flex-start; }
.dm-bubble { padding: 10px 14px; border-radius: 12px; font-size: 13px; line-height: 1.6; white-space: pre-wrap; }
.user .dm-bubble { background: var(--primary); color: #fff; }
.assistant .dm-bubble { background: var(--border); }
.dm-time { font-size: 11px; color: var(--muted); margin-top: 3px; }

.kb-header { display: flex; justify-content: space-between; align-items: center; }
.new-article-form { display: flex; flex-direction: column; margin-bottom: 0; }
.new-article-form h3 { font-size: 15px; font-weight: 600; margin-bottom: 14px; }
</style>
