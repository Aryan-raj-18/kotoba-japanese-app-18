// Live date/time/day for Japan (Asia/Tokyo), written out in Japanese, shown
// on the home page. Runs entirely client-side so it always reflects the
// visitor's actual current time, converted to Japan's timezone.
document.addEventListener('DOMContentLoaded', () => {
  const timeEl = document.getElementById('jp-clock-time');
  const dateEl = document.getElementById('jp-clock-date');
  if (!timeEl || !dateEl) return;

  let dateFmt, timeFmt;
  try {
    dateFmt = new Intl.DateTimeFormat('ja-JP', {
      timeZone: 'Asia/Tokyo',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      weekday: 'short',
    });
    timeFmt = new Intl.DateTimeFormat('ja-JP', {
      timeZone: 'Asia/Tokyo',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false,
    });
  } catch (e) {
    // Very old browsers without Intl / timeZone support: hide the widget
    // rather than show something wrong.
    const clock = document.getElementById('jp-clock');
    if (clock) clock.hidden = true;
    return;
  }

  function tick() {
    const now = new Date();
    dateEl.textContent = dateFmt.format(now);
    timeEl.textContent = timeFmt.format(now);
  }

  tick();
  setInterval(tick, 1000);
});
