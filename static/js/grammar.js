document.addEventListener('DOMContentLoaded',()=>{
 const input=document.getElementById('grammar-filter'),cards=[...document.querySelectorAll('.grammar-card')];let level='all';
 function apply(){const q=(input.value||'').trim().toLowerCase();cards.forEach(c=>c.hidden=(level!=='all'&&c.dataset.level!==level)||(q&&!c.dataset.search.includes(q)));}
 input&&input.addEventListener('input',apply);document.querySelectorAll('#grammar-levels [data-level]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('#grammar-levels [data-level]').forEach(x=>x.classList.remove('active'));b.classList.add('active');level=b.dataset.level;apply();}));
});
