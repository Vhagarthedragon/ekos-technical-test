<template>
  <!-- Support view is a full-screen embedded widget demo — no shell needed -->
  <RouterView v-if="route.path === '/support'" />

  <div v-else class="layout">
    <nav class="sidebar">
      <div class="logo">ClinicDesk <span>AI</span></div>
      <RouterLink to="/support" class="nav-item">
        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        Support Agent
      </RouterLink>
      <RouterLink to="/sales" class="nav-item">
        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
        Sales Agent
      </RouterLink>
      <RouterLink to="/admin" class="nav-item">
        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
        Admin
      </RouterLink>
      <button class="theme-toggle" @click="toggle" :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'">
        <!-- sun -->
        <svg v-if="isDark" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
          <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
        </svg>
        <!-- moon -->
        <svg v-else width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
        {{ isDark ? 'Light mode' : 'Dark mode' }}
      </button>
    </nav>
    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useTheme } from './composables/useTheme'

const route = useRoute()
const { isDark, toggle } = useTheme()
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 220px;
  background: var(--surface);
  border-right: 1px solid var(--border);
  padding: 28px 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex-shrink: 0;
}

.logo {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 24px;
  padding-left: 10px;
  color: var(--text);
}
.logo span { color: var(--primary); }

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  color: var(--muted);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.15s;
}
.nav-item:hover { background: var(--border); color: var(--text); }
.nav-item.router-link-active { background: #2d2f50; color: var(--primary); }

.content {
  flex: 1;
  overflow: auto;
}

.theme-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 12px;
  border-radius: 8px;
  background: transparent;
  border: none;
  color: var(--muted);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  margin-top: auto;
  transition: all 0.15s;
  width: 100%;
}
.theme-toggle:hover { background: var(--border); color: var(--text); }
</style>
