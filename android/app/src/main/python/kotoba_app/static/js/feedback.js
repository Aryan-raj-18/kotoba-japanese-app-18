/* =====================================================================
   Kotoba — feedback form
   ---------------------------------------------------------------------
   Notes are POSTed to the local Flask process, which appends them to a
   JSON file next to the app's own data. There's no server to reach and
   nothing leaves the device; "Send by email" hands the note to the
   phone's mail app instead, which is the only path off-device and is
   entirely the person's choice.
   ================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('feedback-form');
  if (!form) return;

  const statusEl = document.getElementById('fb-status');
  const messageEl = document.getElementById('fb-message');
  const topicEl = document.getElementById('fb-topic');
  const nameEl = document.getElementById('fb-name');
  const logEl = document.getElementById('feedback-log');
  const entriesEl = document.getElementById('feedback-entries');
  const countEl = document.getElementById('fb-count');

  let rating = 0;

  // ------------------------------------------------------------ rating --
  document.querySelectorAll('#fb-rating .rating-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      rating = Number(btn.dataset.value);
      document.querySelectorAll('#fb-rating .rating-btn').forEach(b => {
        b.setAttribute('aria-pressed', String(Number(b.dataset.value) === rating));
      });
      if (window.Sfx) Sfx.tap();
    });
  });

  function setStatus(kind, text) {
    statusEl.className = 'form-status ' + kind;
    statusEl.textContent = text;
    statusEl.hidden = false;
  }

  // ------------------------------------------------------- the log list --
  function formatWhen(iso) {
    const d = new Date(iso);
    if (isNaN(d)) return iso;
    return d.toLocaleString(undefined, {
      year: 'numeric', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit',
    });
  }

  function renderLog(entries) {
    entriesEl.innerHTML = '';
    if (!entries.length) {
      logEl.hidden = true;
      return;
    }
    logEl.hidden = false;
    countEl.textContent = `(${entries.length})`;

    entries.slice().reverse().forEach(entry => {
      const card = document.createElement('div');
      card.className = 'feedback-entry';

      const head = document.createElement('header');
      const topic = document.createElement('span');
      topic.className = 'fb-topic';
      topic.textContent = entry.topic || 'Note';
      head.appendChild(topic);

      const when = document.createElement('span');
      when.textContent = formatWhen(entry.created_at);
      head.appendChild(when);

      if (entry.rating) {
        const stars = document.createElement('span');
        stars.textContent = `${entry.rating}/5`;
        head.appendChild(stars);
      }
      if (entry.name) {
        const who = document.createElement('span');
        who.textContent = `— ${entry.name}`;
        head.appendChild(who);
      }

      const body = document.createElement('p');
      body.textContent = entry.message;

      card.appendChild(head);
      card.appendChild(body);
      entriesEl.appendChild(card);
    });
  }

  function loadLog() {
    fetch('/api/feedback')
      .then(r => r.json())
      .then(data => renderLog(data.entries || []))
      .catch(() => { /* nothing saved yet, or storage unavailable */ });
  }
  loadLog();

  // --------------------------------------------------------- submitting --
  function payload() {
    return {
      topic: topicEl.value,
      rating: rating,
      message: (messageEl.value || '').trim(),
      name: (nameEl.value || '').trim(),
    };
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const body = payload();

    if (!body.message) {
      setStatus('err', 'Add a note first — even one line helps.');
      messageEl.focus();
      if (window.Sfx) Sfx.incorrect();
      return;
    }

    try {
      const res = await fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (!res.ok || !data.ok) throw new Error(data.error || 'save failed');

      setStatus('ok', 'ありがとう — thanks, that\'s saved.');
      if (window.Sfx) Sfx.complete();
      messageEl.value = '';
      rating = 0;
      document.querySelectorAll('#fb-rating .rating-btn')
        .forEach(b => b.setAttribute('aria-pressed', 'false'));
      renderLog(data.entries || []);
    } catch (err) {
      setStatus('err', 'Could not save that note. Try "Send by email instead".');
      if (window.Sfx) Sfx.incorrect();
    }
  });

  // ------------------------------------------------------------- mailto --
  document.getElementById('fb-email').addEventListener('click', () => {
    const body = payload();
    if (!body.message) {
      setStatus('err', 'Write the note first, then send it.');
      messageEl.focus();
      return;
    }
    const lines = [
      body.message,
      '',
      '—',
      `Topic: ${body.topic}`,
      body.rating ? `Rating: ${body.rating}/5` : '',
      body.name ? `From: ${body.name}` : '',
      `Sent from Kotoba on ${navigator.userAgent}`,
    ].filter(Boolean).join('\n');

    const href = 'mailto:' + (window.FEEDBACK_EMAIL || '') +
      '?subject=' + encodeURIComponent(`Kotoba feedback — ${body.topic}`) +
      '&body=' + encodeURIComponent(lines);
    window.location.href = href;
  });

  // -------------------------------------------------------------- clear --
  const clearBtn = document.getElementById('fb-clear');
  if (clearBtn) {
    clearBtn.addEventListener('click', async () => {
      if (!confirm('Delete every note saved on this device?')) return;
      try {
        await fetch('/api/feedback', { method: 'DELETE' });
        renderLog([]);
        setStatus('ok', 'Cleared.');
      } catch (e) {
        setStatus('err', 'Could not clear those notes.');
      }
    });
  }
});
