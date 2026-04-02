<template>
  <div class="layout">
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
    </nav>
    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

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
</style>
