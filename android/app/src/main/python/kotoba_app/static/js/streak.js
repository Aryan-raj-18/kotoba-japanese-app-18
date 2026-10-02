document.addEventListener('DOMContentLoaded', async () => {
  const res = await fetch('/api/streak');
  const data = await res.json();
  const activeSet = new Set(data.active_dates || []);

  document.getElementById('streak-current-num').textContent = data.current;
  document.getElementById('streak-longest').textContent = data.longest;
  document.getElementById('streak-total').textContent = data.total_days;
  document.getElementById('streak-flame-big').classList.toggle('streak-cold', data.current === 0);
  document.getElementById('streak-empty-note').hidden = data.total_days > 0;

  const cal = document.getElementById('streak-calendar');
  const today = new Date();
  const dayNames = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];

  // header row of weekday initials
  dayNames.forEach(d => {
    const el = document.createElement('span');
    el.className = 'streak-day-label';
    el.textContent = d;
    cal.appendChild(el);
  });

  // 30 days ago through today, padded at the front so the grid lines
  // up under the correct weekday column
  const start = new Date(today);
  start.setDate(start.getDate() - 29);
  const pad = start.getDay();
  for (let i = 0; i < pad; i++) {
    const el = document.createElement('span');
    el.className = 'streak-day streak-day-empty';
    cal.appendChild(el);
  }

  for (let i = 0; i < 30; i++) {
    const d = new Date(start);
    d.setDate(d.getDate() + i);
    const iso = d.toISOString().slice(0, 10);
    const el = document.createElement('span');
    const isToday = iso === today.toISOString().slice(0, 10);
    el.className = 'streak-day' + (activeSet.has(iso) ? ' streak-day-active' : '') + (isToday ? ' streak-day-today' : '');
    el.textContent = d.getDate();
    el.title = iso;
    cal.appendChild(el);
  }
});
