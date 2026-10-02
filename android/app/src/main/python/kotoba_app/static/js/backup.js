document.addEventListener('DOMContentLoaded',()=>{
 const status=document.getElementById('backup-status');
 document.getElementById('backup-export').addEventListener('click',async()=>{
  status.textContent='Preparing backup…';const r=await fetch('/api/backup/data'),data=await r.json();
  data.browser_settings={};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k&&k.startsWith('kotoba:'))data.browser_settings[k]=localStorage.getItem(k);}
  const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=`kotoba-backup-${new Date().toISOString().slice(0,10)}.json`;a.click();URL.revokeObjectURL(a.href);status.textContent='Backup created.';
 });
 document.getElementById('backup-import').addEventListener('click',async()=>{
  const f=document.getElementById('backup-file').files[0];if(!f){status.textContent='Choose a backup file first.';return;}
  try{const data=JSON.parse(await f.text());if(data.browser_settings)Object.entries(data.browser_settings).forEach(([k,v])=>{if(k.startsWith('kotoba:'))localStorage.setItem(k,String(v));});const r=await fetch('/api/backup/data',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const out=await r.json();if(!r.ok)throw new Error(out.error||'Restore failed');status.textContent='Backup restored. Reloading…';setTimeout(()=>location.href='/',900);}catch(e){status.textContent=e.message||'Could not read that backup.';}
 });
});
