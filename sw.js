/* ============================================================
   sw.js — عامل الخدمة: يجعل الموقع يعمل دون إنترنت بعد أول زيارة.
   - الهيكل (HTML/CSS/JS/الأيقونات + core.json): يُخزَّن عند التثبيت.
   - ملفات الوحدات uNN.json: تُعرض من المخزن فوراً ثم تُحدَّث في الخلفية.
   - Pyodide (محرك بايثون من CDN): يُخزَّن عند أول استخدام، فيعمل التشغيل دون إنترنت لاحقاً.
   VERSION يحدّثه tools/build_data.py تلقائياً عند تغيّر أي ملف.
   ============================================================ */
const VERSION = "pm-4a27585500";
const SHELL = VERSION + "-shell";
const DATA = VERSION + "-data";
const RUNTIME = "pm-runtime";        // Pyodide والخطوط: لا تتغير بتغيّر المحتوى

const SHELL_FILES = [
  "./", "index.html", "404.html", "manifest.webmanifest",
  "assets/css/tokens.css", "assets/css/app.css", "assets/css/learn.css",
  "assets/js/config.js", "assets/js/app.js", "assets/js/py.js", "assets/js/py-worker.js",
  "assets/img/logo.svg", "assets/img/icon-192.png", "assets/img/icon-512.png",
  "assets/data/core.json", "assets/data/search.json",
];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(SHELL).then(c => c.addAll(SHELL_FILES)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(
    keys.filter(k => k !== SHELL && k !== DATA && k !== RUNTIME).map(k => caches.delete(k))
  )).then(() => self.clients.claim()));
});

function staleWhileRevalidate(req, cacheName) {
  return caches.open(cacheName).then(cache => cache.match(req).then(hit => {
    const net = fetch(req).then(res => { if (res.ok) cache.put(req, res.clone()); return res; }).catch(() => hit);
    return hit || net;
  }));
}

function cacheFirst(req, cacheName) {
  return caches.open(cacheName).then(cache => cache.match(req).then(hit => hit || fetch(req).then(res => {
    if (res.ok || res.type === "opaque") cache.put(req, res.clone());
    return res;
  })));
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  if (url.hostname === "cdn.jsdelivr.net" || url.hostname === "files.pythonhosted.org" || url.hostname === "fonts.gstatic.com") {
    e.respondWith(cacheFirst(req, RUNTIME));
    return;
  }
  if (url.hostname === "fonts.googleapis.com") { e.respondWith(staleWhileRevalidate(req, RUNTIME)); return; }
  if (url.origin !== location.origin) return;

  if (req.mode === "navigate") {                // الصفحة نفسها: الشبكة أولاً، ثم النسخة المخزنة
    e.respondWith(fetch(req).catch(() => caches.match("index.html")));
    return;
  }
  if (url.pathname.includes("/assets/data/")) { e.respondWith(staleWhileRevalidate(req, DATA)); return; }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req)));
});
