/* ═══════════════════════════════════════════════════════════ */
/* CacheLab intro — Heavy JS Animations & Content           */
/* ═══════════════════════════════════════════════════════════ */

// ═══ Canvas Background (Connected Nodes) ═══
(function() {
  const c = document.getElementById('bgCanvas');
  const ctx = c.getContext('2d');
  let w, h, nodes = [];

  function resize() {
    w = c.width = innerWidth;
    h = c.height = innerHeight;
    const count = Math.min(90, Math.floor(w * h / 14000));
    nodes = Array.from({ length: count }, () => ({
      x: Math.random() * w, y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      r: 1 + Math.random() * 2,
      c: ['#6c63ff', '#00d26a', '#00bcd4', '#ffc107', '#ff6b6b', '#e040fb'][Math.floor(Math.random() * 6)]
    }));
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x, dy = nodes[i].y - nodes[j].y;
        const d = Math.sqrt(dx * dx + dy * dy);
        if (d < 140) {
          ctx.beginPath();
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.strokeStyle = `rgba(108,99,255,${0.12 * (1 - d / 140)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
      const n = nodes[i];
      n.x += n.vx; n.y += n.vy;
      if (n.x < 0 || n.x > w) n.vx *= -1;
      if (n.y < 0 || n.y > h) n.vy *= -1;
      ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
      ctx.fillStyle = n.c; ctx.globalAlpha = 0.5;
      ctx.fill(); ctx.globalAlpha = 1;
    }
    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', resize);
  resize(); draw();
})();

// ═══ Glow Blob follows Cursor ═══
(function() {
  const g = document.getElementById('glowBlob');
  document.addEventListener('mousemove', e => {
    g.style.left = e.clientX + 'px';
    g.style.top = e.clientY + 'px';
  });
})();

// ═══ Mouse Trail Particles ═══
(function() {
  let last = 0;
  document.addEventListener('mousemove', e => {
    const now = Date.now();
    if (now - last < 40) return;
    last = now;
    const t = document.createElement('div');
    const s = 6 + Math.random() * 10;
    t.style.cssText = `position:fixed;width:${s}px;height:${s}px;border-radius:50%;pointer-events:none;z-index:1;left:${e.clientX - s / 2}px;top:${e.clientY - s / 2}px;background:${['#6c63ff', '#00d26a', '#00bcd4', '#ffc107', '#ff6b6b'][Math.floor(Math.random() * 5)]};opacity:0.6;animation:trailFade 1s ease-out forwards;`;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 1000);
  });
})();

const style = document.createElement('style');
style.textContent = '@keyframes trailFade{0%{opacity:.6;transform:scale(1)}100%{opacity:0;transform:scale(0)}}';
document.head.appendChild(style);

// ═══ Scroll Reveal ═══
const revealObs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('vis'); });
}, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));

// ═══ Smooth Scroll ═══
window.scrollTo = id => document.getElementById(id).scrollIntoView({ behavior: 'smooth' });

// ═══ Counter Animation ═══
const counterObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const el = e.target;
      const target = +el.dataset.count;
      let cur = 0;
      const step = Math.max(1, Math.floor(target / 40));
      const timer = setInterval(() => {
        cur += step;
        if (cur >= target) { cur = target; clearInterval(timer); }
        el.textContent = cur;
      }, 30);
      counterObs.unobserve(el);
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-num').forEach(el => counterObs.observe(el));

// ═══ 3D Tilt on Feature Cards ═══
document.querySelectorAll('.fcard').forEach(card => {
  card.addEventListener('mousemove', e => {
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    card.style.transform = `translateY(-10px) scale(1.02) perspective(1000px) rotateX(${-y * 8}deg) rotateY(${x * 8}deg)`;
  });
  card.addEventListener('mouseleave', () => card.style.transform = '');
});

// ═══ Code Line Reveal ═══
const codeObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.querySelectorAll('.code-line').forEach((line, i) => {
        line.style.animationDelay = (i * 0.06) + 's';
        line.classList.add('show');
      });
    }
  });
}, { threshold: 0.3 });
document.querySelectorAll('.code-win').forEach(el => codeObs.observe(el));

// ═══ Build Feature Cards ═══
const features = [
  { icon: '⚡', title: 'Cache Decorator', desc: 'دکوریتور @cache با 17 پارامتر — TTL, compression, stampede, sliding و...', color: '#6c63ff' },
  { icon: '🧠', title: 'Memory Backend', desc: 'LRU eviction, thread-safe, پیش‌فرض و سریع‌ترین بک‌اند', color: '#00d26a' },
  { icon: '💿', title: 'Disk Backend', desc: 'دائمی روی دیسک با رمزنگاری AES-256-GCM و cleanup پس‌زمینه', color: '#ffc107' },
  { icon: '☁️', title: 'Redis Backend', desc: 'Connection pooling, retry, cluster mode, pipeline, SCAN', color: '#00bcd4' },
  { icon: '🏗', title: 'Multi-Tier', desc: 'L1 → L2 fallback خودکار, TTL jitter, backfill خودکار', color: '#ff6b6b' },
  { icon: '🎯', title: 'Stampede Protection', desc: 'Lock هوشمند — فقط یک thread محاسبه می‌کنه', color: '#6c63ff' },
  { icon: '🔄', title: 'Background Refresh', desc: 'تازه‌سازی خودکار قبل از انقضا بدون downtime', color: '#00d26a' },
  { icon: '📊', title: 'Cache Statistics', desc: 'hits, misses, hit_rate, reset, export — همه لحظه‌ای', color: '#00bcd4' },
  { icon: '🫠', title: 'Sliding TTL', desc: 'TTL با هر access ریست می‌شه — عالی برای sessions', color: '#e040fb' },
  { icon: '📦', title: 'Compression', desc: 'zlib compression با 1-9 levels — صرفه‌وری تا 80%', color: '#ffc107' },
  { icon: '🔗', title: 'Request Coalescing', desc: 'چندین درخواست تکراری → یک fetch واحد', color: '#ff6b6b' },
  { icon: '💀', title: 'Negative Cache', desc: 'کش کردن نتایج None — جلوگیری از query تکراری', color: '#6c63ff' },
];

const fw = document.getElementById('featuresWall');
features.forEach((f, i) => {
  fw.innerHTML += `<div class="fcard reveal d${Math.min(4, i % 4 + 1)}">
    <span class="fc-num">String${String(i + 1).padStart(2, '0')}</span>
    <div class="fc-icon" style="background:${f.color}15;color:${f.color}">${f.icon}</div>
    <h3>${f.title}</h3><p>${f.desc}</p>
  </div>`;
});

// ═══ Build Architecture ═══
const layers = [
  { label: 'Application Layer', cls: 'l1', items: ['Flask', 'Django', 'FastAPI', 'Async', 'Any Python'] },
  { label: 'Pattern Layer (20)', cls: 'l2', items: ['Stampede', 'Coalescing', 'Adaptive TTL', 'Graceful Deg.', 'Write-Behind'] },
  { label: 'Core Layer', cls: 'l3', items: ['@cache', 'CacheStats', 'Serializer', 'Key Builder', 'TTL Parser'] },
  { label: 'Backend Layer', cls: 'l4', items: ['Memory', 'Disk', 'Redis', 'Multi-Tier', 'Custom ABC'] },
  { label: 'Storage', cls: 'l5', items: ['RAM', 'SSD/HDD', 'Redis Server', 'TmpFS', 'Cloud'] },
];

const aw = document.getElementById('archWrap');
layers.forEach(l => {
  let html = `<div class="arch-label">${l.label}</div><div class="arch-layer">`;
  l.items.forEach(item => html += `<div class="arch-box ${l.cls}">${item}</div>`);
  html += '</div>';
  if (l !== layers[layers.length - 1]) html += '<div class="arch-arrow">⬇</div>';
  aw.innerHTML += html;
});

// ═══ Build Code Section ═══
document.getElementById('codeRow').innerHTML = `
<div class="code-win">
  <div class="code-head"><div class="dot dr"></div><div class="dot dy"></div><div class="dot dg"></div><span style="margin-right:12px;font-size:12px;color:var(--text2)">example.py</span></div>
  <pre><span class="code-line"><span class="cm"># نصب</span></span>
<span class="code-line">pip install recall-cache</span>
<span class="code-line"></span>
<span class="code-line"><span class="kw">from</span> recall <span class="kw">import</span> cache</span>
<span class="code-line"></span>
<span class="code-line"><span class="dc">@cache</span>(ttl=<span class="st">"1h"</span>, maxsize=<span class="nm">1000</span>)</span>
<span class="code-line"><span class="kw">def</span> <span class="fn">get_user</span>(user_id):</span>
<span class="code-line">    <span class="kw">return</span> db.query(user_id)</span>
<span class="code-line"></span>
<span class="code-line"><span class="cm"># اولین فراخوانی: ~2 ثانیه</span></span>
<span class="code-line">result = get_user(<span class="nm">42</span>)</span>
<span class="code-line"><span class="cm"># فراخوانی بعدی: فوری! ⚡</span></span>
<span class="code-line">result = get_user(<span class="nm">42</span>)</span>
<span class="code-line"></span>
<span class="code-line"><span class="cm"># مدیریت کش</span></span>
<span class="code-line">get_user.cache_clear()</span>
<span class="code-line">get_user.cache_delete(<span class="nm">42</span>)</span>
<span class="code-line">get_user.cache_set(<span class="st">"custom"</span>, <span class="nm">99</span>)</span>
<span class="code-line"></span>
<span class="code-line"><span class="cm"># آمار و مانیتورینگ</span></span>
<span class="code-line">stats = get_user.cache_stats</span>
<span class="code-line"><span class="bi">print</span>(<span class="st">f"Hit rate: </span><span class="nm">{stats.hit_rate}</span><span class="st">"</span>)</span></pre>
</div>
<div class="steps">
  <div class="step"><div class="step-n">۱</div><div><h4>نصب</h4><p><code>pip install recall-cache</code><br>بدون وابستگی اجباری</p></div></div>
  <div class="step"><div class="step-n">۲</div><div><h4>دکوریتور</h4><p>روی هر تابعی<br><code>@cache(ttl="1h")</code> بزنید</p></div></div>
  <div class="step"><div class="step-n">۳</div><div><h4>Backend انتخاب</h4><p>Memory, Disk, Redis<br>یا Multi-Tier</p></div></div>
  <div class="step"><div class="step-n">۴</div><div><h4>CacheLab</h4><p>تست، بنچمارک<br>و مانیتور لحظه‌ای</p></div></div>
</div>`;

// ═══ Build Patterns Grid ═══
const patterns = [
  { icon: '🔗', title: 'Request Coalescing', desc: 'ترکیب درخواست‌های تکراری همزمان به یک fetch' },
  { icon: '🎲', title: 'Probabilistic Early Expiration', desc: 'انقضا احتمالی زودهنگام (روش فیسبوک)' },
  { icon: '💀', title: 'Negative Cache', desc: 'کش کردن None و خطاها برای جلوگیری از درخواست تکراری' },
  { icon: '📚', title: 'Cache Patterns', desc: 'Read-Through, Write-Through, Write-Behind' },
  { icon: '🕸', title: 'Dependency Invalidation', desc: 'ابطال زنجیره‌ای کلیدهای وابسته' },
  { icon: '💳', title: 'Transaction Integration', desc: 'commit/rollback روی عملیات کش' },
  { icon: '📋', title: 'Schema Versioning', desc: 'نسخه‌بندی کلید برای invalidation گروهی' },
  { icon: '🌐', title: 'HTTP Cache (ETag)', desc: 'کش HTTP با ETag و Cache-Control' },
  { icon: '🎛', title: 'Cache-Control', desc: 'max-age, stale-while-revalidate, must-revalidate' },
  { icon: '📈', title: 'Adaptive TTL', desc: 'تنظیم خودکار TTL بر اساس hit rate' },
  { icon: '🔥', title: 'Hot Key Detection', desc: 'شناسایی کلیدهای پرتکرار' },
  { icon: '⚖️', title: 'Large Key Detection', desc: 'شناسایی کلیدهای حجیم' },
  { icon: '🗜', title: 'Compression Monitoring', desc: 'ردیابی نرخ فشرده‌سازی' },
  { icon: '🧩', title: 'Memory Fragmentation', desc: 'ردیابی تکه‌تکه شدن حافظه' },
  { icon: '🏚', title: 'Stale Data Detection', desc: 'شناسایی داده‌های کهنه' },
  { icon: '🌡', title: 'Startup Warmer', desc: 'گرم کردن کش در زمان شروع' },
  { icon: '🛡', title: 'Graceful Degradation', desc: 'سرویس‌دهی با داده قدیمی هنگام خطا' },
  { icon: '🆔', title: 'Idempotency Key', desc: ' جلوگیری از تکرار عملیات (پرداخت)' },
  { icon: '🔁', title: 'Request Deduplication', desc: 'حذف درخواست‌های تکراری در بازه زمانی' },
  { icon: '📊', title: 'Cache Efficiency', desc: 'ردیابی hit rate در طول زمان' },
];

const pg = document.getElementById('patternsGrid');
patterns.forEach(p => {
  pg.innerHTML += `<div class="pcard reveal d${Math.floor(Math.random() * 4) + 1}">
    <div class="pc-top"><div class="pc-icon">${p.icon}</div><h4>${p.title}</h4></div>
    <p>${p.desc}</p>
  </div>`;
});

// ═══ Build Backend Cards ═══
const backends = [
  { icon: '🧠', title: 'Memory Backend', tag: 'پیش‌فرض · سریع‌ترین', color: '#6c63ff', desc: 'LRU eviction, thread-safe, TTL, compression — برای کش درون‌‌حافظه‌ای با بالاترین سرعت. پیش‌فرض دکوریتور @cache.' },
  { icon: '💿', title: 'Disk Backend', tag: 'دائمی · رمزنگاری', color: '#ffc107', desc: 'ذخیره روی فایل با AES-256-GCM encryption, background cleanup, size limit — برای کش بین restart ها.' },
  { icon: '☁️', title: 'Redis Backend', tag: 'توزیعه · Cluster', color: '#00bcd4', desc: 'Connection pooling, retry logic, pipeline, SCAN, cluster mode, key hash — برای سرورهای توزیع‌شده.' },
  { icon: '🏗', title: 'Multi-Tier Backend', tag: 'L1 → L2', color: '#ff6b6b', desc: 'L1 (Memory) + L2 (Disk/Redis) با fallback خودکار, TTL jitter, backfill خودکار — بهترین performance.' },
];

const bc = document.getElementById('backendCards');
backends.forEach(b => {
  bc.innerHTML += `<div class="bcard reveal">
    <div class="bc-icon" style="background:${b.color}15;color:${b.color}">${b.icon}</div>
    <h3>${b.title}</h3><p>${b.desc}</p>
    <span class="bc-tag">${b.tag}</span>
  </div>`;
});

// ═══ Build Monitor ═══
const monitors = [
  { id: 'm1', cls: 'pu', label: 'Memory Keys', val: 0 },
  { id: 'm2', cls: 'gr', label: 'Hit Rate', val: 0, suffix: '%' },
  { id: 'm3', cls: 'cy', label: 'Ops/sec', val: 0 },
  { id: 'm4', cls: 'ye', label: 'Uptime', val: 0, suffix: 's' },
];

const mw = document.getElementById('monitorWrap');
monitors.forEach(m => {
  mw.innerHTML += `<div class="mcard reveal">
    <h4><span class="live-dot"></span> ${m.label}</h4>
    <div class="mval ${m.cls}" id="${m.id}">0${m.suffix || ''}</div>
    <div class="spark" id="spark${m.id.slice(1)}"></div>
  </div>`;
});

// ═══ Build Benchmark ═══
const benchData = [
  { val: '~180K', h: 200, c: '#6c63ff', lbl: 'Memory\nRead' },
  { val: '~140K', h: 160, c: '#00d26a', lbl: 'Memory\nWrite' },
  { val: '~95K', h: 110, c: '#00bcd4', lbl: 'Redis\nLocal' },
  { val: '~75K', h: 85, c: '#ffc107', lbl: 'Memory+\nCompress' },
  { val: '~38K', h: 45, c: '#ff6b6b', lbl: 'Disk\nSSD' },
];

const bw = document.getElementById('benchWrap');
let benchHtml = '<div class="bars">';
benchData.forEach(b => {
  benchHtml += `<div class="bar-col"><div class="bar-val">${b.val}</div><div class="bar" style="height:${b.h}px;background:linear-gradient(180deg,${b.c},${b.c}88)"></div><div class="bar-lbl">${b.lbl}</div></div>`;
});
benchHtml += '</div>';
bw.innerHTML = benchHtml;

// ═══ Build Comparison ═══
document.getElementById('compareWrap').innerHTML = `<table class="cmp">
<thead><tr><th>قابلیت</th><th>recall</th><th>lru_cache</th><th>cachetools</th><th>dogpile</th></tr></thead>
<tbody>
<tr><td>TTL</td><td class="rec"><span class="ck">✓</span></td><td><span class="cx">✗</span></td><td><span class="ck">✓</span></td><td><span class="ck">✓</span></td></tr>
<tr><td>Disk Backend</td><td class="rec"><span class="ck">✓</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td><td><span class="ck">✓</span></td></tr>
<tr><td>Redis Built-in</td><td class="rec"><span class="ck">✓</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td><td><span class="ck">✓</span></td></tr>
<tr><td>Multi-Tier</td><td class="rec"><span class="ck">✓</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td></tr>
<tr><td>Stampede Protection</td><td class="rec"><span class="ck">✓</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td></tr>
<tr><td>Async Support</td><td class="rec"><span class="ck">✓</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td></tr>
<tr><td>20 Advanced Patterns</td><td class="rec"><span class="ck">✓</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td></tr>
<tr><td>Background Refresh</td><td class="rec"><span class="ck">✓</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td></tr>
<tr><td>Compression</td><td class="rec"><span class="ck">✓</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td></tr>
<tr><td>Custom Key Function</td><td class="rec"><span class="ck">✓</span></td><td><span class="cx">✗</span></td><td><span class="ck">✓</span></td><td><span class="cx">✗</span></td></tr>
<tr><td>Namespacing / Prefix</td><td class="rec"><span class="ck">✓</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td></tr>
<tr><td>Bulk Operations</td><td class="rec"><span class="ck">✓</span></td><td><span class="cx">✗</span></td><td><span class="ck">✓</span></td><td><span class="cx">✗</span></td></tr>
<tr><td>Encryption (AES-256)</td><td class="rec"><span class="ck">✓</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td><td><span class="cx">✗</span></td></tr>
<tr><td>Thread-safe</td><td class="rec"><span class="ck">✓</span></td><td><span class="ck">✓</span></td><td><span class="ck">✓</span></td><td><span class="ck">✓</span></td></tr>
</tbody></table>`;

// ═══ Animated Monitor ═══
(function() {
  let v1 = 0, v2 = 0, v3 = 0, v4 = 0;
  function tick() {
    v1 = Math.floor(80 + Math.random() * 900);
    v2 = Math.floor(68 + Math.random() * 30);
    v3 = Math.floor(12000 + Math.random() * 80000);
    v4++;
    const e1 = document.getElementById('m1'), e2 = document.getElementById('m2'), e3 = document.getElementById('m3'), e4 = document.getElementById('m4');
    if (e1) e1.textContent = v1.toLocaleString();
    if (e2) e2.textContent = v2 + '%';
    if (e3) e3.textContent = v3.toLocaleString();
    if (e4) e4.textContent = v4 + 's';

    document.querySelectorAll('.spark i').forEach(bar => {
      if (Math.random() > 0.6) bar.style.height = (4 + Math.random() * 40) + 'px';
    });
    setTimeout(tick, 1200 + Math.random() * 800);
  }
  tick();
})();

// ═══ Sparklines ═══
['1', '2', '3', '4'].forEach(n => {
  const c = document.getElementById('spark' + n);
  if (!c) return;
  const colors = ['#6c63ff', '#00d26a', '#00bcd4', '#ffc107'];
  for (let i = 0; i < 22; i++) {
    const bar = document.createElement('i');
    bar.style.height = (5 + Math.random() * 35) + 'px';
    bar.style.background = colors[+n - 1];
    bar.style.opacity = 0.4 + Math.random() * 0.6;
    c.appendChild(bar);
  }
});

// ═══ Bar Chart Animation ═══
const barObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.querySelectorAll('.bar').forEach((b, i) => {
        setTimeout(() => b.style.opacity = '1', i * 200);
      });
    }
  });
}, { threshold: 0.3 });
const barEl = document.querySelector('.bars');
if (barEl) {
  barEl.querySelectorAll('.bar').forEach(b => b.style.opacity = '0');
  barObs.observe(barEl);
}

// ═══ Stat Bar Fill ═══
setTimeout(() => {
  document.querySelectorAll('.stat-bar i').forEach(el => {
    el.style.width = el.style.getPropertyValue('--w');
  });
}, 500);

// ═══ Code Typing Effect (first line) ═══
setTimeout(() => {
  const firstLine = document.querySelector('.code-line');
  if (firstLine) firstLine.classList.add('show');
}, 300);

