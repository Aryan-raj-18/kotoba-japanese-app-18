document.addEventListener('DOMContentLoaded', () => {
  // toggle which reading aids are visible
  document.querySelectorAll('.toggle-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      if (window.Sfx) Sfx.tap();
      btn.classList.toggle('active');
      const on = btn.classList.contains('active');
      document.querySelectorAll('.line-' + btn.dataset.target)
        .forEach(el => { el.hidden = !on; });
    });
  });

  // inline comprehension quiz
  document.querySelectorAll('.quiz-item').forEach(item => {
    const answer = item.dataset.answer;
    const explain = item.querySelector('.quiz-explain');
    item.querySelectorAll('.quiz-choice').forEach(btn => {
      btn.addEventListener('click', () => {
        const right = btn.textContent.trim() === answer;
        item.querySelectorAll('.quiz-choice').forEach(b => {
          b.disabled = true;
          if (b.textContent.trim() === answer) b.classList.add('correct');
        });
        if (!right) btn.classList.add('incorrect');
        explain.hidden = false;
        if (window.KotobaLearn) KotobaLearn.record({kind:'story', id:(location.pathname + ':' + item.querySelector('.quiz-q').textContent), front:item.querySelector('.quiz-q').textContent, prompt:item.querySelector('.quiz-q').textContent, answer:answer, chosen:btn.textContent.trim(), correct:right, quality:right?4:1, explanation:(item.querySelector('.quiz-explain')||{}).textContent||''});
        if (window.Sfx) { right ? Sfx.correct() : Sfx.incorrect(); }
      });
    });
  });
});
