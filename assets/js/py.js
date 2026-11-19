/* ============================================================
   py.js — تشغيل كود بايثون داخل المتصفح (Pyodide في Web Worker)
   - لا يُحمَّل Pyodide إلا عند أول ضغطة «شغّل» (حفاظاً على سرعة الموقع).
   - التشغيل في Worker منفصل: الصفحة لا تتجمد، ونستطيع إيقاف الحلقات اللانهائية.
   - كل تشغيل في مجلد مؤقت جديد، فلا تتداخل ملفات الأمثلة.
   ============================================================ */
(function () {
  "use strict";
  const TIMEOUT_MS = 15000;            // مهلة التنفيذ بعد اكتمال التحميل
  let worker = null, ready = false, seq = 0;
  const pending = new Map();           // id → {resolve, timer}
  const listeners = new Set();         // من يريد معرفة حالة التحميل

  function status(s) { listeners.forEach(fn => fn(s)); }

  function spawn() {
    worker = new Worker("assets/js/py-worker.js");
    ready = false;
    status("loading");
    worker.onmessage = e => {
      const m = e.data;
      if (m.type === "ready") { ready = true; status("ready"); return; }
      if (m.type === "load-error") { status("error"); failAll("تعذّر تحميل بايثون. تأكد من اتصالك بالإنترنت ثم أعد المحاولة."); return; }
      if (m.type === "started") {        // بدأ التنفيذ فعلاً (بعد تثبيت المكتبات): نبدأ عدّ المهلة
        const p = pending.get(m.id);
        if (p) p.timer = setTimeout(() => timeout(m.id), TIMEOUT_MS);
        return;
      }
      if (m.type === "result") {
        const p = pending.get(m.id);
        if (!p) return;
        clearTimeout(p.timer); pending.delete(m.id); p.resolve(m);
      }
    };
    worker.onerror = () => { status("error"); failAll("حدث خطأ في محرك بايثون. أعد المحاولة."); restart(); };
  }

  function failAll(msg) {
    pending.forEach(p => { clearTimeout(p.timer); p.resolve({ out: "", err: msg, errName: "LoadError", figs: [] }); });
    pending.clear();
  }

  function restart() { if (worker) worker.terminate(); worker = null; ready = false; }

  function timeout(id) {
    const p = pending.get(id);
    if (!p) return;
    pending.delete(id);
    restart();          // الطريقة الوحيدة لإيقاف حلقة لا نهائية دون ترويسات خاصة على الخادم
    p.resolve({ out: "", errName: "Timeout", figs: [],
      err: "توقف التنفيذ بعد " + TIMEOUT_MS / 1000 + " ثانية. غالباً هناك حلقة لا نهائية (while شرطها لا يصبح False)." });
  }

  /** تشغيل كود؛ يرجع وعداً بـ {out, err, errName, figs} */
  function run(code, stdin, files) {
    if (!worker) spawn();
    const id = ++seq;
    return new Promise(resolve => {
      pending.set(id, { resolve, timer: null });
      worker.postMessage({ id, code, stdin: stdin || "", files: files || null });
    });
  }

  window.PY = { run, onStatus: fn => listeners.add(fn), isReady: () => ready, preload: () => { if (!worker) spawn(); } };
})();
