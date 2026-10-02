(function () {
  async function post(url, payload) {
    try {
      const r = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload || {})});
      if (!r.ok) return null;
      return await r.json();
    } catch (_) { return null; }
  }

  async function record(payload) {
    if (!payload) return null;
    return post('/api/learner/record', payload);
  }
  async function action(name, amount) {
    return post('/api/learner/action', {action:name, amount:amount || 1});
  }
  async function favorite(item, list) {
    return post('/api/favorites/toggle', {item, list:list || 'Favorites'});
  }

  function toast(message) {
    let el = document.getElementById('kotoba-toast');
    if (!el) {
      el = document.createElement('div'); el.id='kotoba-toast'; el.className='kotoba-toast';
      document.body.appendChild(el);
    }
    el.textContent=message; el.classList.add('show');
    clearTimeout(el._t); el._t=setTimeout(()=>el.classList.remove('show'),1800);
  }

  function wireFavorites(root) {
    (root || document).querySelectorAll('.favorite-btn:not([data-fav-wired])').forEach(btn => {
      btn.dataset.favWired='1';
      btn.addEventListener('click', async () => {
        const item={
          kind:btn.dataset.favoriteKind || 'item', id:btn.dataset.favoriteId || btn.dataset.favoriteFront,
          front:btn.dataset.favoriteFront || '', reading:btn.dataset.favoriteReading || '',
          meaning:btn.dataset.favoriteMeaning || '', url:btn.dataset.favoriteUrl || location.pathname,
        };
        const data=await favorite(item, btn.dataset.favoriteList || 'Favorites');
        if (data) { btn.classList.toggle('saved', !!data.added); btn.textContent=data.added ? '★ Saved' : '☆ Save'; toast(data.added ? 'Saved to Favorites' : 'Removed from Favorites'); }
      });
    });
  }

  window.KotobaLearn={record,action,favorite,toast,wireFavorites};
  document.addEventListener('DOMContentLoaded',()=>wireFavorites(document));
})();
