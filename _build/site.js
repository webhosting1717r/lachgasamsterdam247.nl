// Progressieve verfijning (max. 4 kB inline). Alles werkt ook zonder dit script.
// Regels die met // beginnen worden bij het bouwen weggelaten; sluit elke regel af met ; of een blok.
(function(){
var d=document,w=window;
// 1. Licht dat de muis volgt op glazen tegels (alleen muis/trackpad).
if(w.matchMedia&&matchMedia("(hover:hover) and (pointer:fine)").matches){
d.addEventListener("pointermove",function(e){
var t=e.target.closest?e.target.closest(".card,.area,.strip>div,.toc a,.points,.cta-box"):0,b;
if(!t)return;
b=t.getBoundingClientRect();
t.style.setProperty("--mx",(e.clientX-b.left)+"px");
t.style.setProperty("--my",(e.clientY-b.top)+"px");
},{passive:true});
}
// 2. Scroll-spy voor de navigatie "Op deze pagina": markeert de sectie die nu in beeld is.
var n=d.querySelector(".pagetoc"),c,io;
if(n&&"IntersectionObserver" in w){
io=new IntersectionObserver(function(es){
es.forEach(function(e){
if(e.isIntersecting){
if(c)c.classList.remove("on");
c=e.target._a;
c.classList.add("on");
}
});
},{rootMargin:"-32% 0px -67% 0px"});
[].forEach.call(n.querySelectorAll('a[href^="#"]'),function(a){
var h=d.getElementById(a.getAttribute("href").slice(1)),s=h&&h.closest("section");
if(s){s._a=a;io.observe(s);}
});
}
// 3. Hoofdmenu op de telefoon: schuif de rij naar de huidige pagina, zonder de pagina zelf te verplaatsen.
var k=d.querySelector(".jump:not(.pagetoc) [aria-current],.jump:not(.pagetoc) .on"),u=k&&k.closest("ul");
if(u&&u.scrollWidth>u.clientWidth)u.scrollLeft+=k.getBoundingClientRect().left-u.getBoundingClientRect().left-(u.clientWidth-k.offsetWidth)/2;
// 4. iOS Safari toont :active pas als er een touchstart-luisteraar bestaat.
d.addEventListener("touchstart",function(){},{passive:true});
})();
