// node _build/check_wordfit.js . 320 390 834 1440  — meldt koppen/knoppen waarin een woord breder is dan het vak, knoppen die omlopen, en horizontale overflow (alle paginas)
const { chromium } = require('playwright');
const http=require('http'),fs=require('fs'),path=require('path');
const [SITE,...widths]=process.argv.slice(2);
function walk(d,out=[]){for(const f of fs.readdirSync(d)){const p=path.join(d,f);if(['_build','shots','node_modules','fonts','images'].includes(f))continue;if(fs.statSync(p).isDirectory())walk(p,out);else if(f.endsWith('.html'))out.push(p)}return out}
const pages=walk(SITE).map(p=>'/'+path.relative(SITE,p).replace(/index\.html$/,''));
const srv=http.createServer((q,r)=>{let f=path.join(SITE,decodeURIComponent(q.url.split('?')[0]));if(fs.existsSync(f)&&fs.statSync(f).isDirectory())f=path.join(f,'index.html');if(!fs.existsSync(f)){r.writeHead(404);return r.end()}const m={'.html':'text/html; charset=utf-8','.woff2':'font/woff2','.svg':'image/svg+xml','.png':'image/png'}[path.extname(f)]||'application/octet-stream';r.writeHead(200,{'content-type':m});r.end(fs.readFileSync(f))}).listen(0,async()=>{
 const b=await chromium.launch();let n=0;
 for(const w of widths){const ctx=await b.newContext({viewport:{width:+w,height:800},isMobile:+w<700,hasTouch:+w<700});
  for(const pg of pages){const p=await ctx.newPage();await p.goto('http://127.0.0.1:'+srv.address().port+pg);
   const res=await p.evaluate(()=>{const out=[];const c=document.createElement('canvas').getContext('2d');
    for(const el of document.querySelectorAll('h1,h2,h3,.btn,.toc a,.chips a,.jump a,.eyebrow,dt,th')){const cs=getComputedStyle(el);if(!el.offsetWidth)continue;
     c.font=cs.fontWeight+' '+cs.fontSize+' '+cs.fontFamily;c.letterSpacing=cs.letterSpacing;
     let avail=el.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);if(el.matches('.btn')){const bs=getComputedStyle(el,'::before');if(bs.display!=='none'&&bs.content!=='none')avail-=parseFloat(bs.width)+parseFloat(cs.columnGap||0);const lh=parseFloat(cs.lineHeight)||parseFloat(cs.fontSize)*1.2;const inner=el.clientHeight-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom);const rg=document.createRange();rg.selectNodeContents(el);const hh=rg.getBoundingClientRect().height;if(hh>lh*1.6)out.push('WRAP '+el.className+' "'+el.textContent.trim().slice(0,30)+'" '+Math.round(el.offsetWidth)+'px');}
     for(const word of el.textContent.trim().split(/\s+/)){const m=c.measureText(word).width;if(m>avail+0.5){out.push(el.tagName+'.'+el.className+' "'+word+'" '+Math.round(m)+'>'+Math.round(avail));break}}}
    const sw=document.documentElement.scrollWidth;if(sw>innerWidth+1)out.push('OVERFLOW '+sw);
    return out});
   if(res.length){n+=res.length;console.log(w+' '+pg+'\n   '+res.join('\n   '))}
   await p.close();}
  await ctx.close();}
 console.log(n?n+' problemen':'alle woorden passen ('+pages.length+' pagina\'s x '+widths.length+' breedtes)');
 await b.close();srv.close();});
