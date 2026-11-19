/* ============================================================
   app.js — تطبيق «دليل إتقان بايثون» (صفحة واحدة، توجيه بالـ hash)
   المحتويات:
     1) الحالة والتخزين        6) البطاقات (Leitner)      11) تقدّمي + نقاط الضعف
     2) أدوات عامة              7) التدريب الفوري          12) الشهادة + التحقق
     3) البوابات والنقاط        8) اختبار الإتقان           13) البحث، الخطة، المصادر
     4) الصفحة الرئيسية         9) التمارين                  14) التشغيل (Pyodide)
     5) الوحدة والدرس          10) الاختبار الشامل           15) الموجّه والأحداث
   ============================================================ */
(function () {
  "use strict";
  const CFG = window.PM_CONFIG;
  const DATA = "assets/data/";
  let D = null;                        // core.json
  const UNITS = {};                    // uNN.json بعد تحميلها
  const LETTERS = ["أ", "ب", "ج", "د"];
  const TF = ["صح", "خطأ"];
  const LEITNER_DAYS = [0, 1, 3, 7, 16];  // الفاصل بالأيام للصناديق 1..5

  /* ============================================================
     1) الحالة والتخزين (localStorage على جهاز الطالب فقط)
     ============================================================ */
  const STORE_KEY = "pm_state_v2";
  const OLD_KEY = "aau_python_mastery_v1";
  const SALT = "aau-camS-2026";
  function blank() {
    return { v: 2, student: null, units: {}, final: null, lessons: {}, cards: {}, ex: {}, plan: {},
             weak: {}, xp: 0, days: [], badges: {}, reviewed: 0, teacher: false };
  }
  function load() {
    try {
      const s = JSON.parse(localStorage.getItem(STORE_KEY));
      if (s && s.v === 2) return Object.assign(blank(), s);
      // ترحيل تقدّم النسخة الأولى من الموقع (الوحدات المُتقنة والاسم)
      const old = JSON.parse(localStorage.getItem(OLD_KEY));
      if (old && old.v === 1) {
        const n = blank();
        n.student = old.student; n.units = old.units || {}; n.final = old.final; n.ex = old.ex || {}; n.plan = old.plan || {};
        Object.values(n.units).forEach(u => { delete u.cur; delete u.last; });
        return n;
      }
    } catch (e) { /* تخزين غير متاح: نعمل بالذاكرة فقط */ }
    return blank();
  }
  let S = load();
  function save() { try { localStorage.setItem(STORE_KEY, JSON.stringify(S)); } catch (e) { /* وضع خاص */ } }

  /* ============================================================
     2) أدوات عامة
     ============================================================ */
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const pct = x => Math.round(x * 100) + "%";
  const today = () => { const d = new Date(); return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); };
  const addDays = (iso, n) => { const d = new Date(iso + "T12:00:00"); d.setDate(d.getDate() + n); return d.toISOString().slice(0, 10); };
  function shuffle(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
  const unitMeta = n => D.units.find(u => u.n === n);
  const unitIdx = n => D.units.findIndex(u => u.n === n);
  const courseLabel = c => c === "P1" ? "البرمجة 1" : "البرمجة 2";
  const lessonId = (n, i) => n + ":" + i;
  function announce(msg) { const el = $("#live"); el.textContent = ""; setTimeout(() => { el.textContent = msg; }, 30); }

  async function getJSON(name) {
    const r = await fetch(DATA + name);
    if (!r.ok) throw new Error(name);
    return r.json();
  }
  async function unitData(n) {
    if (!UNITS[n]) UNITS[n] = await getJSON("u" + n + ".json");
    return UNITS[n];
  }

  // أيقونات SVG صغيرة (مرسومة يدوياً، بلا مكتبات)
  const ICON = {
    sun: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg>',
    moon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a7 7 0 0 0 10.5 10.5z"/></svg>',
    contrast: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 3v18a9 9 0 0 0 0-18z" fill="currentColor"/></svg>',
    lock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>',
    gh: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .5a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1.1-.8.1-.7.1-.7 1.2.1 1.9 1.2 1.9 1.2 1.1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0C17.3 4.7 18.3 5 18.3 5c.7 1.7.3 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .5z"/></svg>',
    in: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.4 20.5h-3.6v-5.6c0-1.3 0-3-1.8-3s-2.1 1.4-2.1 2.9v5.7H9.3V9h3.4v1.6c.5-.9 1.6-1.8 3.4-1.8 3.6 0 4.3 2.4 4.3 5.5v6.2zM5.3 7.4a2.1 2.1 0 1 1 0-4.2 2.1 2.1 0 0 1 0 4.2zM7.1 20.5H3.5V9h3.6v11.5zM22.2 0H1.8C.8 0 0 .8 0 1.7v20.6c0 .9.8 1.7 1.8 1.7h20.4c1 0 1.8-.8 1.8-1.7V1.7C24 .8 23.2 0 22.2 0z"/></svg>',
    mail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    scholar: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3 1 9.5l11 6.5 9-5.3V17h2V9.5L12 3zm-6 10.6V17c0 1.7 2.7 4 6 4s6-2.3 6-4v-3.4l-6 3.5-6-3.5z"/></svg>',
    say: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/></svg>',
    check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
    brain: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M9 4a3 3 0 0 0-3 3v.3A3 3 0 0 0 4 10a3 3 0 0 0 1 2.2A3 3 0 0 0 6 17a3 3 0 0 0 3 3V4zM15 4a3 3 0 0 1 3 3v.3A3 3 0 0 1 20 10a3 3 0 0 1-1 2.2A3 3 0 0 1 18 17a3 3 0 0 1-3 3V4z"/></svg>',
    play: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l12-7.5z"/></svg>',
    gate: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 21V9l8-6 8 6v12M9 21v-7h6v7"/></svg>',
    dna: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M7 3c10 4-0 13 10 18M17 3C7 7 17 16 7 21M8 8h8M8 16h8"/></svg>',
  };

  /* ============================================================
     3) البوابات، النقاط، الأوسمة
     ============================================================ */
  const TH = () => D.threshold;
  const mastered = n => !!(S.units[n] && S.units[n].mastered);
  const isOpen = n => S.teacher || unitIdx(n) === 0 || mastered(D.units[unitIdx(n) - 1].n);
  const lessonsOpen = n => !CFG.lockLessons || isOpen(n);
  const finalOpen = () => S.teacher || D.units.every(u => mastered(u.n));
  const finalPassed = () => !!(S.final && S.final.mastered);
  const masteredCount = () => D.units.filter(u => mastered(u.n)).length;
  const currentUnit = () => D.units.find(u => !mastered(u.n)) || D.units[D.units.length - 1];
  const uState = n => (S.units[n] = S.units[n] || { mastered: false, best: 0, attempts: 0 });
  const doneCount = n => { const m = unitMeta(n); let c = 0; for (let i = 0; i < m.count; i++) if (S.lessons[lessonId(n, i)]) c++; return c; };

  // التحقق من الإجابة بنفس معادلة ملف Excel (الإجابة الصحيحة غير مكتوبة في البيانات)
  const answerNo = (q, choice) => q.o ? choice + 1 : TF.indexOf(choice) + 5;
  const isCorrect = (q, choice) => (q.id * 37 + answerNo(q, choice) * 101) % 997 === q.code;
  const correctChoice = q => q.o ? q.o.findIndex((_, i) => isCorrect(q, i)) : TF.find(t => isCorrect(q, t));

  const LEVEL_XP = 250;
  const BADGES = [
    { id: "first_lesson", icon: "🌱", t: "الخطوة الأولى", d: "أنهيت أول درس", ok: () => Object.keys(S.lessons).length >= 1 },
    { id: "lessons50", icon: "📚", t: "قارئ مثابر", d: "أنهيت 50 درساً", ok: () => Object.keys(S.lessons).length >= 50 },
    { id: "first_unit", icon: "🔓", t: "أول بوابة", d: "أتقنت أول وحدة", ok: () => masteredCount() >= 1 },
    { id: "streak3", icon: "🔥", t: "ثلاثة أيام متتالية", d: "تعلّمت 3 أيام متتالية", ok: () => streak() >= 3 },
    { id: "streak7", icon: "⚡", t: "أسبوع كامل", d: "تعلّمت 7 أيام متتالية", ok: () => streak() >= 7 },
    { id: "cards100", icon: "🧠", t: "ذاكرة قوية", d: "راجعت 100 بطاقة", ok: () => S.reviewed >= 100 },
    { id: "ex10", icon: "🛠️", t: "مبرمج عملي", d: "حللت 10 تمارين", ok: () => Object.values(S.ex).filter(v => v === "solved").length >= 10 },
    { id: "p1", icon: "🎯", t: "أتقنت البرمجة 1", d: "أتقنت الوحدات 01 إلى 10", ok: () => D.units.filter(u => u.course === "P1").every(u => mastered(u.n)) },
    { id: "all", icon: "🏅", t: "كل البوابات", d: "أتقنت الوحدات الـ 13", ok: () => masteredCount() === D.units.length },
    { id: "final", icon: "🎓", t: "متقن بايثون", d: "اجتزت الاختبار الشامل", ok: () => finalPassed() },
  ];
  function streak() {
    const days = new Set(S.days);
    let n = 0, d = today();
    if (!days.has(d)) d = addDays(d, -1);        // اليوم لم يبدأ بعد: نعدّ حتى الأمس
    while (days.has(d)) { n++; d = addDays(d, -1); }
    return n;
  }
  function gain(xp, why) {
    S.xp += xp;
    if (!S.days.includes(today())) S.days.push(today());
    if (S.days.length > 400) S.days = S.days.slice(-400);
    const fresh = BADGES.filter(b => !S.badges[b.id] && b.ok());
    fresh.forEach(b => { S.badges[b.id] = today(); });
    save();
    if (fresh.length) toast(`${fresh[0].icon} وسام جديد: ${fresh[0].t}`);
    else if (why) toast(`+${xp} نقطة · ${why}`, true);
    paintXp();
  }
  function paintXp() {
    const el = $("#xp-chip");
    if (el) el.innerHTML = `<b>${S.xp}</b> نقطة · مستوى ${Math.floor(S.xp / LEVEL_XP) + 1}${streak() ? ` · 🔥 ${streak()}` : ""}`;
  }
  let toastTimer;
  function toast(msg, quiet) {
    let t = $("#toast");
    if (!t) { t = document.createElement("div"); t.id = "toast"; t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    t.textContent = msg; t.classList.toggle("quiet", !!quiet); t.classList.add("show");
    clearTimeout(toastTimer); toastTimer = setTimeout(() => t.classList.remove("show"), 2600);
  }

  function statusPill(n) {
    if (mastered(n)) return `<span class="pill p-ok">مُتقَنة ${pct(S.units[n].best)}</span>`;
    if (!isOpen(n)) return `<span class="pill p-lock">${ICON.lock} مقفلة</span>`;
    const s = S.units[n];
    if (s && s.attempts) return `<span class="pill p-bad">${pct(s.best)} · أعد الاختبار</span>`;
    return `<span class="pill p-warn">متاحة</span>`;
  }

  /* ============================================================
     4) الصفحة الرئيسية
     ============================================================ */
  function viewHome() {
    const mc = masteredCount(), total = D.units.length, cur = currentUnit();
    const C = 2 * Math.PI * 80, off = C * (1 - mc / total);
    const started = mc > 0 || Object.keys(S.lessons).length > 0;
    const strand = D.units.map(u => {
      const cls = mastered(u.n) ? "done" : u.n === cur.n && isOpen(u.n) ? "now" : "";
      return `<li><a class="node ${cls} ${u.course === "P2" ? "p2" : ""}" href="#/u/${u.n}" aria-label="الوحدة ${u.n}: ${esc(u.title)}${mastered(u.n) ? " (مُتقنة)" : isOpen(u.n) ? "" : " (مقفلة)"}">${u.n}</a>
        <span class="node-cap">${esc(u.title)}</span></li>`;
    }).join("");
    const unitRows = course => D.units.filter(u => u.course === course).map(u => {
      const done = doneCount(u.n), p = done / u.count;
      return `<li><a class="unit-row ${isOpen(u.n) ? "" : "locked"}" href="#/u/${u.n}">
        <span class="u-num">${u.n}</span>
        <span><span class="u-title">${esc(u.title)}</span><span class="u-en" dir="ltr">${esc(u.en)}</span></span>
        <span class="u-meter"><span class="meter" role="img" aria-label="أنهيت ${done} من ${u.count} درساً"><i style="width:${Math.round(p * 100)}%"></i></span>
          <span class="meter-cap">${done} / ${u.count} درساً</span></span>
        <span class="u-status">${statusPill(u.n)}</span></a></li>`;
    }).join("");
    const st = D.stats;
    return `
    <section class="hero" aria-labelledby="hero-t"><div class="wrap">
      <div class="hero-grid">
        <div>
          <p class="hero-kicker">${esc(CFG.university)}</p>
          <h1 id="hero-t">أتقِن بايثون وحدةً بعد وحدة، ولا تنتقل قبل أن تُتقن.</h1>
          <p class="lead">كل مفهوم يُشرح بالترتيب نفسه: مثال من حياتك، ثم المعنى، ثم كود صحيح وخاطئ تشغّله بنفسك، ثم ثلاثة تمارين. أمثلة من المعلوماتية الحيوية والصحية: تسلسلات DNA، وسجلات المرضى، ومؤشر BMI.</p>
          <div class="row">
            <a class="btn gold" href="#/u/${cur.n}">${started ? "تابع من الوحدة " + cur.n : "ابدأ الوحدة 01"}</a>
            <a class="btn on-dark" href="#/plan">خطة 30 يوماً</a>
          </div>
        </div>
        <div class="ring" role="img" aria-label="أتقنت ${mc} من ${total} وحدة">
          <svg viewBox="0 0 180 180"><circle class="track" cx="90" cy="90" r="80" fill="none" stroke-width="12"/>
          <circle class="value" cx="90" cy="90" r="80" fill="none" stroke-width="12" stroke-linecap="round" stroke-dasharray="${C}" stroke-dashoffset="${off}"/></svg>
          <div class="ring-label"><b>${mc}/${total}</b><span>وحدة مُتقنة</span></div>
        </div>
      </div>
      <div class="strand">
        <div class="strand-title"><h2>مسار الإتقان</h2><span class="small">كل عقدة بوابة: تنفتح بعد إتقان ما قبلها بنسبة ${pct(TH())} على الأقل</span></div>
        <ol>${strand}</ol>
        <div class="strand-legend"><span><i style="background:#2E9E64"></i>مُتقنة</span><span><i style="background:var(--py-yellow)"></i>الحالية</span><span><i style="background:var(--ink-2);border:2px solid #34506E"></i>مقفلة</span><span><i style="border:2px dashed #8EA3B9"></i>البرمجة 2</span></div>
      </div>
    </div></section>

    <div class="facts" role="list">
      <div class="fact" role="listitem"><b>${st.lessons}</b><span>درساً بـ 12 نقطة</span></div>
      <div class="fact" role="listitem"><b>${st.questions}</b><span>سؤالاً للتدريب والإتقان</span></div>
      <div class="fact" role="listitem"><b>${st.cards}</b><span>بطاقة تذكّر</span></div>
      <div class="fact" role="listitem"><b>${st.exercises}</b><span>تمريناً تطبيقياً</span></div>
    </div>

    <form class="home-search" role="search" data-search><label class="sr-only" for="q-home">ابحث في الدروس</label>
      <input id="q-home" type="search" name="q" placeholder="ابحث عن مفهوم: append، try، BMI، FASTA…" autocomplete="off">
      <button class="btn" type="submit">ابحث</button></form>

    <div class="course-head"><h2>البرمجة 1</h2><span class="muted">الوحدات 01 – 10</span></div>
    <ol class="units">${unitRows("P1")}</ol>
    <div class="course-head"><h2>البرمجة 2</h2><span class="muted">الوحدات 11 – 13، ثم الاختبار الشامل</span></div>
    <ol class="units">${unitRows("P2")}</ol>

    <h2>كيف تتعلّم هنا؟</h2>
    <ol class="steps">
      <li><h3>اقرأ الدرس</h3><p>اثنتا عشرة نقطة بالترتيب: من المثال اليومي إلى الكود. شغّل كل مثال بنفسك داخل الصفحة.</p></li>
      <li><h3>حلّ التمارين الثلاثة</h3><p>فسّر ناتج كود، واكتب كوداً، وأصلح خطأً. الإجابة النموذجية بعد محاولتك.</p></li>
      <li><h3>راجع بالبطاقات</h3><p>صناديق ليتنر تعيد عليك ما نسيته أكثر مما تعرفه، في الوقت المناسب.</p></li>
      <li><h3>اجتز بوابة الإتقان</h3><p>${pct(TH())} في اختبار الوحدة تفتح التالية. الأخطاء تقودك إلى الدرس المحدد لمراجعته.</p></li>
    </ol>

    <h2>لماذا هذا الدليل؟</h2>
    <div class="why">
      <div>${ICON.gate}<div><h3>الإتقان قبل الانتقال</h3><p>لا تُبنى معرفة على أساس ناقص؛ كل وحدة تُفتح بعد إثبات إتقان السابقة.</p></div></div>
      <div>${ICON.play}<div><h3>بايثون حقيقية داخل المتصفح</h3><p>كل مثال قابل للتشغيل والتعديل دون تثبيت أي برنامج، حتى من الهاتف.</p></div></div>
      <div>${ICON.dna}<div><h3>أمثلة من تخصصك</h3><p>نسبة GC، ملفات FASTA، سجلات المرضى، مؤشر BMI: البرمجة في خدمة المعلوماتية الحيوية والصحية.</p></div></div>
      <div>${ICON.brain}<div><h3>كل خطأ يقودك إلى درس</h3><p>بعد كل سؤال خاطئ تعرف الدرس الذي تحتاجه، وتجمع صفحة «تقدّمي» نقاط ضعفك.</p></div></div>
    </div>

    <h2>أسئلة شائعة</h2>
    <div class="faq">
      <details><summary>هل أحتاج إلى تثبيت بايثون؟</summary><p>لا. الأمثلة تعمل داخل المتصفح. أول تشغيل يحمّل بايثون (حوالي 10 ميغابايت) مرة واحدة، ثم يصبح فورياً. وننصحك بتثبيت بايثون على حاسوبك لاحقاً للمشاريع الكبيرة.</p></details>
      <details><summary>أين يُحفظ تقدّمي؟</summary><p>في متصفحك على هذا الجهاز فقط، ولا يُرسل إلى أي خادم. لنقله إلى جهاز آخر استخدم «تصدير التقدم» من صفحة تقدّمي.</p></details>
      <details><summary>كيف يعرف المدرس أنني أتقنت الوحدات؟</summary><p>من صفحة «تقدّمي» تنسخ رمز الإتمام وترسله. الرمز موقّع؛ أي تعديل عليه يجعله غير صالح، ويستطيع المدرس التحقق منه من صفحة التحقق.</p></details>
      <details><summary>رسبت في اختبار الإتقان، ماذا أفعل؟</summary><p>اقرأ الدروس المذكورة تحت أسئلتك الخاطئة، وتدرّب عليها في قسم «تدريب»، ثم أعد الاختبار. تتغير الأسئلة وترتيب الخيارات في كل محاولة.</p></details>
      <details><summary>هل يعمل الموقع دون إنترنت؟</summary><p>نعم، بعد أول زيارة تُحفظ الصفحات والدروس التي فتحتها. ويمكنك تثبيته كتطبيق من قائمة المتصفح («إضافة إلى الشاشة الرئيسية»).</p></details>
    </div>`;
  }

  /* ============================================================
     5) الوحدة والدرس
     ============================================================ */
  function unitHeader(u, tab) {
    const m = unitMeta(u.n), i = unitIdx(u.n);
    const tabs = [["", "الدروس"], ["cards", "البطاقات"], ["practice", "تدريب"], ["exercises", "التمارين"], ["test", "اختبار الإتقان"]];
    return `<nav class="crumbs" aria-label="مسار التنقل"><ol><li><a href="#/">الرئيسية</a></li><li>${courseLabel(m.course)}</li><li aria-current="page">الوحدة ${u.n}</li></ol></nav>
      <div class="unit-head"><h1>الوحدة ${u.n}: ${esc(u.title)}</h1><p class="en" dir="ltr">${esc(u.en)}</p>
      <div class="row">${statusPill(u.n)}<span class="pill p-c">${m.count} درساً</span>
      ${i < D.units.length - 1 && mastered(u.n) ? `<a class="btn sm ghost" href="#/u/${D.units[i + 1].n}">الوحدة التالية</a>` : ""}</div></div>
      <nav class="tabs" aria-label="أقسام الوحدة">${tabs.map(([t, l]) => `<a href="#/u/${u.n}${t ? "/" + t : ""}" ${t === tab ? 'aria-current="page"' : ""}>${l}</a>`).join("")}</nav>`;
  }
  function lockedBox(n) {
    const prev = D.units[unitIdx(n) - 1];
    return `<div class="panel lockbox">${ICON.lock}<h2>هذه الوحدة مقفلة</h2>
      <p>تنفتح بعد إتقان الوحدة ${prev.n} (${esc(prev.title)}) بنسبة ${pct(TH())} على الأقل في اختبار الإتقان.</p>
      <a class="btn" href="#/u/${prev.n}/test">اذهب إلى اختبار الوحدة ${prev.n}</a></div>`;
  }
  function viewUnit(u) {
    const n = u.n;
    let h = unitHeader(u, "");
    if (!lessonsOpen(n)) return h + lockedBox(n);
    const done = doneCount(n);
    const firstOpen = u.lessons.findIndex((_, i) => !S.lessons[lessonId(n, i)]);
    h += `<div class="unit-intro panel">
      <div><h2>ابدأ بمقدمة الوحدة</h2><p class="muted">المفهوم العام قبل التفاصيل، بالنقاط الـ 12 نفسها.</p></div>
      <div class="row"><a class="btn" href="#/u/${n}/intro">اقرأ المقدمة</a>
      ${firstOpen >= 0 ? `<a class="btn ghost" href="#/u/${n}/l/${firstOpen}">${done ? "تابع من حيث توقفت" : "ابدأ الدرس الأول"}</a>` : `<a class="btn ghost" href="#/u/${n}/test">كل الدروس منتهية: اختبر نفسك</a>`}</div>
      <div class="meter" role="img" aria-label="أنهيت ${done} من ${u.lessons.length} درساً"><i style="width:${Math.round(done / u.lessons.length * 100)}%"></i></div>
      <p class="meter-cap">أنهيت ${done} من ${u.lessons.length} درساً</p></div>`;
    h += u.groups.map(g => {
      const items = u.lessons.map((l, i) => [l, i]).filter(([l]) => l.g === g.id);
      return `<section class="lgroup"><h2>${esc(g.title)} <small>(${items.length})</small></h2><p class="muted">${esc(g.desc)}</p>
        <ul class="chips">${items.map(([l, i]) => `<li><a href="#/u/${n}/l/${i}" class="chip ${l.kc} ${S.lessons[lessonId(n, i)] ? "done" : ""}" dir="${l.kd}">${S.lessons[lessonId(n, i)] ? `<span class="sr-only">(منتهٍ) </span>` : ""}${l.kh}</a></li>`).join("")}</ul></section>`;
    }).join("");
    return h;
  }
  function lessonToc(u, active) {
    const wide = window.matchMedia("(min-width: 961px)").matches;   // على الجوال يُطوى الفهرس حتى لا يسبق الدرس
    return `<details class="toc-wrap" ${wide ? "open" : ""}><summary>فهرس دروس الوحدة ${u.n}</summary><nav class="toc" aria-label="دروس الوحدة ${u.n}"><a class="toc-intro ${active === "intro" ? "on" : ""}" href="#/u/${u.n}/intro">مقدمة الوحدة</a>` +
      u.groups.map(g => `<b>${esc(g.title)}</b><div>` + u.lessons.map((l, i) => [l, i]).filter(([l]) => l.g === g.id)
        .map(([l, i]) => `<a href="#/u/${u.n}/l/${i}" class="${l.kc} ${S.lessons[lessonId(u.n, i)] ? "done" : ""} ${active === i ? "on" : ""}" dir="${l.kd}" ${active === i ? 'aria-current="page"' : ""}>${l.kh}</a>`).join("") + "</div>").join("") + "</nav></details>";
  }
  function viewLesson(u, i) {
    const n = u.n;
    if (!lessonsOpen(n) && i !== "intro") return unitHeader(u, "") + lockedBox(n);
    const intro = i === "intro";
    const L = intro ? null : u.lessons[i];
    if (!intro && !L) return view404();
    const id = intro ? null : lessonId(n, i);
    const prev = intro ? null : (i === 0 ? `#/u/${n}/intro` : `#/u/${n}/l/${i - 1}`);
    const next = intro ? `#/u/${n}/l/0` : (i < u.lessons.length - 1 ? `#/u/${n}/l/${i + 1}` : `#/u/${n}/test`);
    const head = intro
      ? `<h1 class="lesson-title">${esc(u.intro.key)}</h1><p class="muted">مقدمة الوحدة ${n}: المفهوم العام قبل التفاصيل.</p>`
      : `<div class="kw-head"><h1 class="lesson-title ${L.kc}" dir="${L.kd}">${L.kh}</h1>
         <button class="say" type="button" data-say="${esc(L.key)}" aria-label="استمع إلى نطق ${esc(L.key)}">${ICON.say}</button>
         <span class="lvl">${esc(L.lvl)}</span></div>
         ${L.reused ? `<p class="small muted">هذا الدرس مشترك مع الوحدة ${esc(L.reused)}، ويُعرض هنا لأنه جزء أساسي من هذه الوحدة أيضاً.</p>` : ""}`;
    return `<nav class="crumbs" aria-label="مسار التنقل"><ol><li><a href="#/">الرئيسية</a></li><li><a href="#/u/${n}">الوحدة ${n}: ${esc(u.title)}</a></li><li aria-current="page">${intro ? "المقدمة" : esc(L.key)}</li></ol></nav>
      <div class="layout">${lessonToc(u, intro ? "intro" : i)}
      <article class="lesson">${head}${intro ? u.intro.html : L.html}
        <div class="lesson-foot">
          ${intro ? "" : `<button class="btn ${S.lessons[id] ? "ok-btn" : ""}" type="button" data-act="done" data-id="${id}" aria-pressed="${!!S.lessons[id]}">
            ${S.lessons[id] ? ICON.check + " أنهيت هذا الدرس" : "أنهيت هذا الدرس (+5)"}</button>`}
          <div class="row pager">${prev ? `<a class="btn ghost" href="${prev}" rel="prev">السابق</a>` : ""}<a class="btn ghost" href="${next}" rel="next">${next.endsWith("/test") ? "إلى اختبار الإتقان" : "التالي"}</a></div>
        </div></article></div>`;
  }

  /* ============================================================
     6) البطاقات: صناديق ليتنر + قلب ثلاثي الأبعاد + نطق
     ============================================================ */
  let cardSession = null;     // {n, queue:[i...], pos, flipped}
  function cardState(n, i) { return S.cards[lessonId(n, i)] || { b: 0, due: today() }; }
  function dueCards(n, u) { return u.cards.map((_, i) => i).filter(i => cardState(n, i).due <= today()).sort((a, b) => cardState(n, a).b - cardState(n, b).b); }
  function viewCards(u) {
    const n = u.n;
    let h = unitHeader(u, "cards");
    if (!lessonsOpen(n)) return h + lockedBox(n);
    const boxes = [0, 0, 0, 0, 0, 0];
    u.cards.forEach((_, i) => { boxes[cardState(n, i).b]++; });
    const due = dueCards(n, u);
    if (!cardSession || cardSession.n !== n) cardSession = { n, queue: due, pos: 0, flipped: false, all: false };
    const boxBar = `<div class="boxes" role="list" aria-label="توزيع البطاقات على صناديق ليتنر">
      <div role="listitem"><b>${boxes[0]}</b><span>جديدة</span></div>
      ${[1, 2, 3, 4, 5].map(b => `<div role="listitem"><b>${boxes[b]}</b><span>صندوق ${b}</span></div>`).join("")}</div>
      <p class="small muted">كل بطاقة تعرفها تنتقل إلى الصندوق التالي وتعود بعد مدة أطول (يوم، 3، 7، 16 يوماً). البطاقة التي لا تعرفها تعود إلى الصندوق 1 وتتكرر اليوم.</p>`;
    const s = cardSession;
    if (s.pos >= s.queue.length) {
      return h + boxBar + `<div class="panel lockbox"><h2>${s.queue.length ? "أنهيت جلسة اليوم" : "لا بطاقات مستحقة اليوم"}</h2>
        <p class="muted">${due.length ? `بقيت ${due.length} بطاقة مستحقة.` : "عُد غداً لمراجعة ما يستحق."}</p>
        <div class="row" style="justify-content:center">${due.length ? `<button class="btn" data-act="cards-restart">تابع المراجعة</button>` : ""}
        <button class="btn ghost" data-act="cards-all">راجع كل بطاقات الوحدة الآن</button></div></div>`;
    }
    const i = s.queue[s.pos], c = u.cards[i];
    return h + boxBar + `<div class="flash">
      <p class="small muted" aria-live="polite">البطاقة ${s.pos + 1} من ${s.queue.length} · صندوق ${cardState(n, i).b || "جديد"}</p>
      <div class="flip ${s.flipped ? "flipped" : ""}" id="flip">
        <button class="flip-inner" type="button" data-act="flip" aria-pressed="${s.flipped}">
          <span class="face front" aria-hidden="${s.flipped}"><span class="ask">ما هو؟ وكيف يُكتب؟</span><span class="term">${c.f}</span><span class="hint small">اضغط أو اضغط مسافة للقلب</span></span>
          <span class="face back" aria-hidden="${!s.flipped}"><span class="term small-term">${c.f}</span><span class="ans">${c.b}</span></span>
        </button>
      </div>
      <div class="row flash-act">
        <button class="btn ghost sm" type="button" data-act="say-card" data-side="${s.flipped ? "b" : "f"}">${ICON.say} استمع</button>
        <a class="btn ghost sm" href="#/u/${n}/l/${i}">افتح الدرس</a>
      </div>
      ${s.flipped ? `<div class="row grade"><button class="btn danger" data-act="grade" data-v="0">لم أعرفها <kbd>1</kbd></button>
        <button class="btn" data-act="grade" data-v="1">عرفتها <kbd>2</kbd></button></div>` : ""}
    </div>`;
  }
  function gradeCard(known) {
    const s = cardSession, n = s.n, i = s.queue[s.pos], st = cardState(n, i);
    if (known) { st.b = Math.min(5, st.b + 1); st.due = addDays(today(), LEITNER_DAYS[st.b - 1]); }
    else { st.b = 1; st.due = today(); S.weak[lessonId(n, i)] = (S.weak[lessonId(n, i)] || 0) + 1; }
    S.cards[lessonId(n, i)] = st; S.reviewed++;
    if (!known && st.due === today()) s.queue.push(i);    // تتكرر في الجلسة نفسها
    s.pos++; s.flipped = false;
    gain(known ? 1 : 0);
    render();
  }
  function speak(text) {
    if (!("speechSynthesis" in window)) { toast("المتصفح لا يدعم القراءة الصوتية"); return; }
    speechSynthesis.cancel();
    const latin = /^[\x00-\x7F]+$/.test(text.replace(/\s/g, ""));
    const ut = new SpeechSynthesisUtterance(text);
    ut.lang = latin ? "en-US" : "ar-SA";
    ut.rate = latin ? 0.85 : 0.95;
    speechSynthesis.speak(ut);
  }

  /* ============================================================
     7) التدريب الفوري: تغذية راجعة لحظية + رابط الدرس
     ============================================================ */
  let practice = null;   // {n, q, picked}
  function qBlock(q, inner, num) {
    return `<div class="q-card"><div class="qh">${num ? `<b>${num}.</b>` : ""}<span>${esc(q.k)}</span><span>· ${esc(q.d)}</span></div>
      <p class="qt">${q.t}</p>${q.cp || ""}<div class="opts" role="group" aria-label="الخيارات">${inner}</div></div>`;
  }
  function lessonLink(u, q) {
    if (q.l === null || q.l === undefined) return `<a href="#/u/${u.n}/intro">مقدمة الوحدة ${u.n}</a>`;
    const L = u.lessons[q.l];
    return `<a href="#/u/${u.n}/l/${q.l}"><span dir="${L.kd}" class="${L.kc}">${L.kh}</span></a>`;
  }
  function viewPractice(u) {
    const n = u.n;
    let h = unitHeader(u, "practice");
    if (!lessonsOpen(n)) return h + lockedBox(n);
    const pool = u.bank.concat(u.gen);
    if (!practice || practice.n !== n) practice = { n, q: pool[Math.floor(Math.random() * pool.length)], picked: null, right: 0, total: 0 };
    const p = practice, q = p.q, answered = p.picked !== null;
    const correct = answered ? correctChoice(q) : null;
    const opts = (q.o ? q.o.map((o, i) => [i, o]) : TF.map(t => [t, t])).map(([v, text], pos) => {
      let cls = "";
      if (answered) cls = String(v) === String(correct) ? "is-right" : String(v) === String(p.picked) ? "is-wrong" : "";
      return `<button class="opt ${cls}" type="button" data-act="practice-pick" data-v="${esc(v)}" ${answered ? "disabled" : ""}>
        <span class="l">${q.o ? LETTERS[pos] : ""}</span><span class="ot">${esc(text)}</span></button>`;
    }).join("");
    let fb = "";
    if (answered) {
      const ok = String(p.picked) === String(correct);
      fb = `<div class="feedback ${ok ? "ok" : "bad"}" role="status">${ok ? "إجابة صحيحة. +2" : "ليست الإجابة الصحيحة؛ الصحيحة مظللة بالأخضر."}
        <span>الدرس المرتبط: ${lessonLink(u, q)}</span></div>
        <div class="row"><button class="btn" data-act="practice-next" autofocus>السؤال التالي</button></div>`;
    }
    return h + `<p class="muted">أسئلة غير محسوبة في الإتقان، مع تصحيح فوري. ${pool.length} سؤالاً في هذه الوحدة؛ تُختار عشوائياً.
      ${p.total ? `نتيجتك في هذه الجلسة: <b>${p.right} من ${p.total}</b>.` : ""}</p>` + qBlock(q, opts) + fb;
  }
  function practicePick(v) {
    const p = practice, q = p.q;
    p.picked = q.o ? Number(v) : v;
    p.total++;
    const ok = isCorrect(q, p.picked);
    if (ok) { p.right++; gain(2); }
    else { const key = lessonId(p.n, q.l ?? "intro"); S.weak[key] = (S.weak[key] || 0) + 1; save(); }
    announce(ok ? "إجابة صحيحة" : "إجابة خاطئة");
    render();
  }

  /* ============================================================
     8) اختبار الإتقان (النتيجة بعد التسليم فقط)
     ============================================================ */
  function testState(kind, n) {
    if (kind === "final") return (S.final = S.final || { mastered: false, best: 0, attempts: 0 });
    return uState(n);
  }
  function testPool(kind, u) {
    if (kind === "final") return D.final;
    return u.bank.concat(u.gen);
  }
  function startAttempt(kind, u) {
    const st = testState(kind, u ? u.n : null);
    let ids;
    if (kind === "final") ids = D.final.map(q => q.id);
    else ids = shuffle(u.bank).slice(0, u.test.original).concat(shuffle(u.gen).slice(0, u.test.generated)).map(q => q.id);
    st.cur = { order: shuffle(ids), opt: {}, ans: {} };
    testPool(kind, u).filter(q => ids.includes(q.id) && q.o).forEach(q => { st.cur.opt[q.id] = shuffle(q.o.map((_, i) => i)); });
    st.last = null; save();
  }
  function viewTestBody(kind, u) {
    if (!S.student) return studentForm(`أدخل اسمك ورقمك الجامعي قبل ${kind === "final" ? "الاختبار الشامل" : "اختبار الإتقان"}؛ يظهران في رمز الإتمام والشهادة.`);
    const n = u ? u.n : "final";
    const st = testState(kind, u ? u.n : null), pool = testPool(kind, u), byId = Object.fromEntries(pool.map(q => [q.id, q]));
    const unitOf = q => kind === "final" ? null : u;
    let h = "";
    if (st.last) {
      const L = st.last, pass = L.score >= TH();
      const i = u ? unitIdx(u.n) : -1;
      h += `<div class="banner ${pass ? "ok" : "warn"}" role="status">${pass ? "أحسنت! " : "لم تبلغ حد الإتقان بعد. "}
        نتيجتك ${pct(L.score)} (${L.right} من ${L.total}) · حد الإتقان ${pct(TH())}.
        ${pass ? (kind === "final" ? "أتقنت لغة بايثون! شهادتك جاهزة." : "انفتحت الوحدة التالية.") : "راجع الدروس المرتبطة بأسئلتك الخاطئة، ثم أعد الاختبار؛ ستتغير الأسئلة وترتيب الخيارات."}</div>
        <div class="row"><button class="btn" data-act="retake" data-kind="${kind}" data-n="${n}">إعادة الاختبار</button>
        ${pass && kind === "unit" && i < D.units.length - 1 ? `<a class="btn ghost" href="#/u/${D.units[i + 1].n}">الوحدة التالية</a>` : ""}
        ${pass && kind === "unit" && i === D.units.length - 1 ? `<a class="btn ghost" href="#/final">الاختبار الشامل</a>` : ""}
        ${pass && kind === "final" ? `<a class="btn gold" href="#/certificate">اعرض الشهادة</a>` : ""}</div>`;
      const wrong = L.order.filter(id => !L.res[id]);
      if (wrong.length && kind === "unit") {
        const lessonsToReview = [...new Set(wrong.map(id => byId[id] && byId[id].l))];
        h += `<div class="panel"><h2>ما الذي تراجعه؟</h2><ul class="review">${lessonsToReview.map(l => `<li>${lessonLink(u, { l })}</li>`).join("")}</ul></div>`;
      }
      h += L.order.map((id, k) => {
        const q = byId[id]; if (!q) return "";
        const ok = L.res[id];
        let refLink = "";
        if (!ok) {
          if (kind === "final") refLink = `<a href="#/u/${q.u}${q.l !== null ? "/l/" + q.l : "/intro"}">الدرس المرتبط في الوحدة ${q.u}</a>`;
          else refLink = lessonLink(unitOf(q), q);
        }
        return `<div class="q-card ${ok ? "res-ok" : "res-bad"}"><div class="qh"><b>${k + 1}.</b> ${ok ? "صحيحة" : "خاطئة"}</div>
          <p class="qt">${q.t}</p>${q.cp || ""}
          <p class="small">إجابتك: <bdi class="mono-inline">${esc(L.your[id])}</bdi></p>
          ${ok ? "" : `<p class="small">راجع: ${refLink}</p>`}</div>`;
      }).join("");
      return h;
    }
    if (st.mastered && !st.cur)
      h += `<div class="banner ok">اجتزت هذا الاختبار بنسبة ${pct(st.best)} بعد ${st.attempts} محاولة. يمكنك إعادته للتدريب دون أن يتأثر إتقانك.</div>`;
    if (!st.cur) {
      const count = kind === "final" ? D.final.length : u.test.original + u.test.generated;
      return h + `<div class="panel"><h2>${kind === "final" ? "الاختبار الشامل" : "اختبار إتقان الوحدة " + u.n}</h2>
        <p>${count} سؤالاً · حد الإتقان ${pct(TH())} · النتيجة والتصحيح بعد التسليم فقط. ${kind === "unit" ? "تُختار الأسئلة من بنك الوحدة، فتختلف من محاولة لأخرى." : ""}</p>
        <button class="btn" data-act="retake" data-kind="${kind}" data-n="${n}">ابدأ الاختبار</button></div>`;
    }
    const cur = st.cur, answered = Object.keys(cur.ans).length;
    h += cur.order.map((id, k) => {
      const q = byId[id];
      const opts = q.o
        ? cur.opt[id].map((oi, pos) => `<button class="opt" type="button" aria-pressed="${cur.ans[id] === oi}" data-act="pick" data-kind="${kind}" data-n="${n}" data-id="${id}" data-v="${oi}"><span class="l">${LETTERS[pos]}</span><span class="ot">${esc(q.o[oi])}</span></button>`).join("")
        : TF.map(t => `<button class="opt" type="button" aria-pressed="${cur.ans[id] === t}" data-act="pick" data-kind="${kind}" data-n="${n}" data-id="${id}" data-v="${t}"><span class="ot">${t}</span></button>`).join("");
      return `<div id="q${id}">${qBlock(q, opts, k + 1)}</div>`;
    }).join("");
    h += `<div class="submit-bar"><span id="cnt">أجبت عن ${answered} من ${cur.order.length}</span>
      <button class="btn" id="submit" data-act="submit" data-kind="${kind}" data-n="${n}" ${answered < cur.order.length ? "disabled" : ""}>تسليم الاختبار</button></div>`;
    return h;
  }
  function submitTest(kind, u) {
    const st = testState(kind, u ? u.n : null), cur = st.cur;
    if (!cur || Object.keys(cur.ans).length < cur.order.length) return;
    const byId = Object.fromEntries(testPool(kind, u).map(q => [q.id, q]));
    const res = {}, your = {};
    let right = 0;
    for (const id of cur.order) {
      const q = byId[id], a = cur.ans[id];
      res[id] = isCorrect(q, a);
      if (res[id]) right++;
      else { const key = lessonId(q.u, q.l ?? "intro"); S.weak[key] = (S.weak[key] || 0) + 1; }
      your[id] = q.o ? q.o[a] : a;
    }
    const score = right / cur.order.length;
    st.attempts = (st.attempts || 0) + 1;
    st.best = Math.max(st.best || 0, score);
    const first = score >= TH() && !st.mastered;
    if (first) { st.mastered = true; st.date = today(); }
    st.last = { score, right, total: cur.order.length, res, your, order: cur.order };
    st.cur = null; save();
    if (first) gain(kind === "final" ? 200 : 50, kind === "final" ? "أتقنت بايثون" : "أتقنت الوحدة " + u.n);
    else gain(0);
    render(); window.scrollTo(0, 0);
    announce(`نتيجتك ${pct(score)}`);
  }
  function viewTest(u) {
    let h = unitHeader(u, "test");
    if (!isOpen(u.n)) return h + lockedBox(u.n);
    return h + viewTestBody("unit", u);
  }

  /* ============================================================
     9) التمارين التطبيقية (محرر + تلميح + حل بعد المحاولة)
     ============================================================ */
  function viewExercises(u) {
    let h = unitHeader(u, "exercises");
    if (!lessonsOpen(u.n)) return h + lockedBox(u.n);
    const list = D.exercises.filter(e => e.u === u.n);
    if (!list.length) return h + `<p class="muted">لا توجد تمارين تطبيقية كبيرة في هذه الوحدة؛ تمارين كل درس (التفسير، الكتابة، إيجاد الخطأ) موجودة داخل الدروس.</p>`;
    return h + `<p class="muted">مسائل من واقع المختبر والعيادة. اكتب حلك وشغّله، ثم سجّل حالتك. الحل النموذجي يظهر بعد أن تحاول.</p>` + list.map(e => {
      const st = S.ex[e.n] || "none";
      const btn = (v, l) => `<button class="btn sm ${st === v ? "" : "ghost"}" type="button" data-act="ex" data-n="${e.n}" data-v="${v}" aria-pressed="${st === v}">${l}</button>`;
      return `<article class="exercise"><header><h2>تمرين ${e.n}: ${esc(e.t)}</h2>
        <div class="row"><span class="pill p-c">${courseLabel(e.c)}</span><span class="pill p-c">${esc(e.tr)}</span><span class="pill p-warn">${esc(e.lvl)}</span></div></header>
        <p>${esc(e.d)}</p>
        <details class="hint"><summary>تلميح</summary><p>المهارات التي تحتاجها: ${esc(e.hint)}</p></details>
        ${e.files ? `<details class="files"><summary>ملفات تجريبية جاهزة في مجلد التشغيل: ${Object.keys(e.files).map(f => `<bdi dir="ltr">${esc(f)}</bdi>`).join("، ")}</summary>
          ${Object.entries(e.files).map(([f, c]) => `<p class="small"><bdi dir="ltr">${esc(f)}</bdi></p><pre dir="ltr">${esc(c)}</pre>`).join("")}</details>` : ""}
        <div class="editor" data-files="${e.files ? esc(JSON.stringify(e.files)) : ""}"><textarea dir="ltr" spellcheck="false" rows="7" aria-label="اكتب حل التمرين ${e.n}" data-ex="${e.n}">${esc(S.exCode && S.exCode[e.n] || "")}</textarea>
          ${e.stdin ? `<label class="stdin-box"><span>المُدخلات: كل سطر قيمة يقرؤها <bdi dir="ltr">input()</bdi> بالترتيب</span>
            <textarea dir="ltr" rows="${e.stdin.split("\n").length}" spellcheck="false">${esc(e.stdin.trim())}</textarea></label>` : ""}
          <button class="run" type="button" data-run-editor><span aria-hidden="true">▶</span> شغّل كودك</button></div>
        <div class="row ex-status" role="group" aria-label="حالة التمرين">${btn("none", "لم أحاول")}${btn("tried", "حاولت")}${btn("solved", "حللته (+10)")}</div>
        ${st === "none" ? `<p class="small muted">${ICON.lock} الحل النموذجي يظهر بعد أن تسجّل أنك حاولت.</p>`
          : `<details><summary>اعرض الحل النموذجي</summary><div class="code" data-files="${e.files ? esc(JSON.stringify(e.files)) : ""}"><pre dir="ltr"><code>${esc(e.sol)}</code></pre><button class="run" type="button" data-run data-stdin="${esc(e.stdin)}"><span aria-hidden="true">▶</span> شغّل</button></div></details>`}
      </article>`;
    }).join("");
  }

  /* ============================================================
     10) الاختبار الشامل
     ============================================================ */
  function viewFinal() {
    let h = `<h1>الاختبار الشامل</h1><p class="muted">${D.final.length} سؤالاً من الوحدات الـ 13، لم تظهر في اختبارات الوحدات.</p>`;
    if (!finalOpen()) return h + `<div class="panel lockbox">${ICON.lock}<h2>مقفل</h2>
      <p>ينفتح بعد إتقان الوحدات الـ ${D.units.length}. أتقنت حتى الآن ${masteredCount()} وحدة.</p>
      <a class="btn" href="#/u/${currentUnit().n}">تابع الوحدة ${currentUnit().n}</a></div>`;
    return h + viewTestBody("final", null);
  }

  /* ============================================================
     11) تقدّمي: النقاط، الأوسمة، نقاط الضعف، رمز الإتمام
     ============================================================ */
  function studentForm(msg) {
    return `<form class="panel" data-student><h2>بيانات الطالب</h2>${msg ? `<p class="muted">${msg}</p>` : ""}
      <div class="form-row"><label>الاسم الكامل<input type="text" name="name" required autocomplete="name" value="${esc(S.student ? S.student.name : "")}"></label>
      <label>الرقم الجامعي<input type="text" name="id" required inputmode="numeric" dir="ltr" value="${esc(S.student ? S.student.id : "")}"></label>
      <button class="btn" type="submit">حفظ</button></div></form>`;
  }
  function weakList() {
    return Object.entries(S.weak).filter(([, c]) => c > 0).sort((a, b) => b[1] - a[1]).slice(0, 12).map(([key, c]) => {
      const [n, i] = key.split(":"), m = unitMeta(n);
      if (!m) return "";
      const label = i === "intro" ? "مقدمة الوحدة" : (m.lessons[+i] || [""])[0];
      const href = i === "intro" ? `#/u/${n}/intro` : `#/u/${n}/l/${i}`;
      return `<li><a href="${href}"><span class="pill p-c">${n}</span> <bdi>${esc(label)}</bdi></a><span class="pill p-bad">${c} ${c === 1 ? "خطأ" : "أخطاء"}</span></li>`;
    }).join("");
  }
  function hash(s) { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return (h >>> 0).toString(36); }
  const b64 = s => btoa(unescape(encodeURIComponent(s)));
  const unb64 = s => decodeURIComponent(escape(atob(s)));
  function completionCode() {
    const att = D.units.reduce((a, u) => a + ((S.units[u.n] || {}).attempts || 0), 0);
    const p = [S.student.id, S.student.name, masteredCount(), finalPassed() ? Math.round(S.final.best * 100) : -1, att, today()];
    const body = b64(JSON.stringify(p));
    return "PYM-" + body + "-" + hash(body + SALT);
  }
  function viewMe() {
    const lvl = Math.floor(S.xp / LEVEL_XP) + 1, into = S.xp % LEVEL_XP;
    let h = `<h1>تقدّمي</h1>`;
    h += S.student ? `<div class="panel me-head"><div><h2>${esc(S.student.name)}</h2><p class="mono-inline" dir="ltr">${esc(S.student.id)}</p></div>
      <button class="btn sm ghost" data-act="edit-student">تعديل البيانات</button></div>` : studentForm("أدخل بياناتك لتظهر في رمز الإتمام والشهادة.");
    h += `<div class="stats">
      <div><b>${S.xp}</b><span>نقطة</span></div>
      <div><b>${lvl}</b><span>المستوى</span><span class="meter" role="img" aria-label="${into} من ${LEVEL_XP} نقطة للمستوى التالي"><i style="width:${into / LEVEL_XP * 100}%"></i></span></div>
      <div><b>${streak()}</b><span>أيام متتالية</span></div>
      <div><b>${Object.keys(S.lessons).length}</b><span>درساً منتهياً</span></div>
      <div><b>${S.reviewed}</b><span>بطاقة مراجَعة</span></div></div>`;
    h += `<h2>الأوسمة</h2><ul class="badges">${BADGES.map(b => `<li class="${S.badges[b.id] ? "got" : ""}"><span class="b-ic" aria-hidden="true">${b.icon}</span><b>${b.t}</b><span class="small">${b.d}</span>${S.badges[b.id] ? `<span class="sr-only">(حصلت عليه)</span>` : `<span class="sr-only">(لم تحصل عليه بعد)</span>`}</li>`).join("")}</ul>`;
    const wl = weakList();
    h += `<h2>نقاط الضعف</h2><p class="muted">الدروس التي أخطأت في أسئلتها أو بطاقاتها أكثر من غيرها. ابدأ مراجعتك من أعلى القائمة.</p>
      ${wl ? `<ol class="weak">${wl}</ol><button class="btn sm ghost" data-act="clear-weak">مسح القائمة بعد المراجعة</button>` : `<p class="panel muted">لا توجد نقاط ضعف مسجلة بعد. أسئلة التدريب والاختبارات والبطاقات تملأ هذه القائمة.</p>`}`;
    h += `<h2>الوحدات</h2><div class="table-wrap"><table class="t"><caption class="sr-only">حالة الوحدات</caption><thead><tr><th scope="col">الوحدة</th><th scope="col">الدروس</th><th scope="col">الحالة</th><th scope="col">أفضل نتيجة</th><th scope="col">المحاولات</th><th scope="col">تاريخ الإتقان</th></tr></thead><tbody>`;
    for (const u of D.units) {
      const s = S.units[u.n] || {};
      h += `<tr><td><a href="#/u/${u.n}">${u.n} · ${esc(u.title)}</a></td><td>${doneCount(u.n)} / ${u.count}</td><td>${statusPill(u.n)}</td><td>${s.attempts ? pct(s.best) : "—"}</td><td>${s.attempts || 0}</td><td>${s.date || "—"}</td></tr>`;
    }
    const f = S.final || {};
    h += `<tr><th scope="row">الاختبار الشامل</th><td>—</td><td>${finalPassed() ? `<span class="pill p-ok">مجتاز</span>` : finalOpen() ? `<span class="pill p-warn">متاح</span>` : `<span class="pill p-lock">مقفل</span>`}</td>
      <td>${f.attempts ? pct(f.best) : "—"}</td><td>${f.attempts || 0}</td><td>${f.date || "—"}</td></tr></tbody></table></div>`;
    h += `<h2>رمز الإتمام</h2><div class="panel">`;
    if (!S.student) h += `<p class="muted">أدخل اسمك ورقمك الجامعي أولاً.</p>`;
    else h += `<p class="small muted">أرسل هذا الرمز إلى مدرّسك. يحتوي: رقمك واسمك، عدد الوحدات المُتقنة، نتيجة الاختبار الشامل، عدد المحاولات، والتاريخ. أي تعديل عليه يجعله غير صالح.</p>
      <div class="codebox" id="ccode">${esc(completionCode())}</div>
      <div class="row" style="margin-top:8px"><button class="btn sm" data-act="copy">نسخ الرمز</button>${finalPassed() ? `<a class="btn sm gold" href="#/certificate">الشهادة</a>` : ""}</div>`;
    h += `</div><h2>حفظ التقدم ونقله</h2><div class="panel">
      <p class="small muted">يُحفظ تقدّمك في هذا المتصفح على هذا الجهاز فقط. لنقله إلى جهاز آخر: صدّره هنا ثم استورده هناك.</p>
      <div class="row"><button class="btn sm" data-act="export">تصدير التقدم</button>
      <label class="btn sm ghost">استيراد التقدم<input type="file" id="imp" accept=".json,application/json" class="sr-only"></label>
      <button class="btn sm danger" data-act="reset">مسح كل التقدم</button></div></div>`;
    return h;
  }

  /* ============================================================
     12) الشهادة (مع رمز QR) + صفحة التحقق للمدرس
     ============================================================ */
  function loadScript(src) {
    return new Promise((res, rej) => { const s = document.createElement("script"); s.src = src; s.onload = res; s.onerror = rej; document.head.appendChild(s); });
  }
  function viewCertificate() {
    if (!finalPassed() || !S.student) return `<h1>الشهادة</h1><div class="panel lockbox">${ICON.lock}<h2>لم تُصدر بعد</h2>
      <p>تظهر الشهادة بعد اجتياز الاختبار الشامل${S.student ? "" : " وإدخال بياناتك في صفحة تقدّمي"}.</p><a class="btn" href="#/final">الاختبار الشامل</a></div>`;
    const code = completionCode();
    const url = CFG.siteUrl + "#/verify?c=" + encodeURIComponent(code);
    setTimeout(async () => {
      const box = $("#qr");
      if (!box) return;
      try {
        if (!window.qrcode) await loadScript("https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.min.js");
        const qr = window.qrcode(0, "M"); qr.addData(url); qr.make();
        box.innerHTML = qr.createSvgTag({ cellSize: 3, margin: 0, scalable: true });
      } catch (e) { box.textContent = "تعذّر إنشاء رمز QR دون اتصال."; }
    }, 0);
    return `<div class="no-print row" style="justify-content:space-between"><h1>الشهادة</h1><button class="btn" data-act="print">طباعة / حفظ PDF</button></div>
      <section class="certificate" aria-label="شهادة إتمام">
        <img src="assets/img/logo.svg" alt="" width="64" height="64">
        <p class="cert-org">${esc(CFG.university)}</p>
        <h2>شهادة إتقان لغة بايثون</h2>
        <p>تشهد بأن</p>
        <p class="cert-name">${esc(S.student.name)}</p>
        <p>الرقم الجامعي <bdi dir="ltr">${esc(S.student.id)}</bdi></p>
        <p>أتقن الوحدات الـ ${D.units.length} في «${esc(CFG.siteName)}»، واجتاز الاختبار الشامل بنسبة <b>${pct(S.final.best)}</b> بتاريخ <bdi dir="ltr">${esc(S.final.date)}</bdi>.</p>
        <div class="cert-foot"><div id="qr" class="qr" role="img" aria-label="رمز QR للتحقق من الشهادة"></div>
          <div><p class="small">للتحقق امسح الرمز، أو الصق رمز الإتمام في صفحة التحقق.</p><p class="cert-sign" dir="ltr">${esc(CFG.author.name)}</p></div></div>
      </section>`;
  }
  function viewVerify(params) {
    const c = params.get("c") || "";
    setTimeout(() => { if (c) { $("#vcode").value = c; $("#vout").innerHTML = verifyCode(c); } }, 0);
    return `<h1>التحقق من رمز الإتمام</h1><p class="muted">للمدرس: الصق رمز الطالب للتحقق من صحته وقراءة محتواه.</p>
      <div class="panel"><label for="vcode" class="sr-only">رمز الإتمام</label><textarea id="vcode" rows="3" dir="ltr" placeholder="PYM-..."></textarea>
      <div class="row" style="margin-top:8px"><button class="btn" data-act="verify">تحقّق</button></div><div id="vout" aria-live="polite"></div></div>
      <h2>وضع المدرس</h2><div class="panel"><p class="small muted">يفتح كل الوحدات على هذا المتصفح لمراجعة المحتوى دون اجتياز الاختبارات.</p>
      ${S.teacher ? `<p class="banner ok">وضع المدرس مفعّل.</p><button class="btn sm ghost" data-act="teacher-off">إيقاف وضع المدرس</button>`
        : `<form class="form-row" data-teacher><label>كلمة مرور المدرس<input type="password" name="pw" autocomplete="current-password" dir="ltr"></label><button class="btn" type="submit">تفعيل</button></form>`}</div>`;
  }
  function verifyCode(code) {
    const m = /^PYM-([A-Za-z0-9+/=]+)-([a-z0-9]+)$/.exec(code.trim());
    if (!m) return `<div class="banner warn">صيغة الرمز غير صحيحة.</div>`;
    if (hash(m[1] + SALT) !== m[2]) return `<div class="banner must">الرمز غير صالح (عُدّل أو نُسخ ناقصاً).</div>`;
    try {
      const [id, name, mc, fin, att, date] = JSON.parse(unb64(m[1]));
      return `<div class="banner ok">رمز صالح</div><table class="t"><tbody>
        <tr><th scope="row">الاسم</th><td>${esc(name)}</td></tr><tr><th scope="row">الرقم الجامعي</th><td dir="ltr">${esc(id)}</td></tr>
        <tr><th scope="row">الوحدات المُتقنة</th><td>${mc} من ${D.units.length}</td></tr>
        <tr><th scope="row">الاختبار الشامل</th><td>${fin < 0 ? "لم يُجتز بعد" : fin + "%"}</td></tr>
        <tr><th scope="row">مجموع محاولات اختبارات الوحدات</th><td>${att}</td></tr><tr><th scope="row">تاريخ إصدار الرمز</th><td dir="ltr">${esc(date)}</td></tr></tbody></table>`;
    } catch (e) { return `<div class="banner warn">تعذّرت قراءة الرمز.</div>`; }
  }

  /* ============================================================
     13) البحث، الخطة، المصادر، 404
     ============================================================ */
  let SEARCH = null;
  const norm = s => s.toLowerCase().replace(/[ً-ْ]/g, "").replace(/[أإآ]/g, "ا").replace(/ة/g, "ه").replace(/ى/g, "ي");
  function viewSearch(params) {
    const q = (params.get("q") || "").trim();
    let h = `<h1>البحث في الدروس</h1><form class="home-search" role="search" data-search><label class="sr-only" for="q-page">كلمة البحث</label>
      <input id="q-page" type="search" name="q" value="${esc(q)}" placeholder="مثال: append، حلقة، FASTA" autocomplete="off"><button class="btn" type="submit">ابحث</button></form>`;
    if (!q) return h;
    if (!SEARCH) { getJSON("search.json").then(d => { SEARCH = d; render(); }); return h + `<p class="muted">جارٍ التحميل…</p>`; }
    const nq = norm(q);
    const hits = SEARCH.filter(([, , key, what]) => norm(key).includes(nq) || norm(what).includes(nq))
      .sort((a, b) => (norm(b[2]).includes(nq) ? 1 : 0) - (norm(a[2]).includes(nq) ? 1 : 0)).slice(0, 60);
    h += `<p class="muted" role="status">${hits.length ? hits.length + " نتيجة" : "لا نتائج. جرّب كلمة أقصر أو بالإنجليزية."}</p><ul class="results">` +
      hits.map(([n, i, key, what]) => `<li><a href="#/u/${n}/l/${i}"><b><bdi>${esc(key)}</bdi></b> <span class="pill p-c">الوحدة ${n}</span></a><p class="small muted">${esc(what)}…</p>${isOpen(n) || !CFG.lockLessons ? "" : `<span class="pill p-lock">مقفلة</span>`}</li>`).join("") + "</ul>";
    return h;
  }
  function viewPlan() {
    const rows = D.plan.map(p => {
      let st;
      if (p.u === "final") st = finalPassed() ? `<span class="pill p-ok">منجز</span>` : finalOpen() ? `<span class="pill p-warn">متاح</span>` : `<span class="pill p-lock">مقفل</span>`;
      else if (p.u) st = mastered(p.u) ? `<span class="pill p-ok">منجز</span>` : isOpen(p.u) ? `<span class="pill p-warn">متاح</span>` : `<span class="pill p-lock">مقفل</span>`;
      else st = `<label><input type="checkbox" data-act="plan" data-d="${p.day}" ${S.plan[p.day] ? "checked" : ""}> منجز</label>`;
      const topic = p.u && p.u !== "final" ? `<a href="#/u/${p.u}">${esc(p.topic)}</a>` : p.u === "final" ? `<a href="#/final">${esc(p.topic)}</a>` : esc(p.topic);
      return `<tr><th scope="row">اليوم ${p.day}</th><td>${topic}</td><td>${esc(p.act)}</td><td>${st}</td></tr>`;
    }).join("");
    return `<h1>خطة 30 يوماً</h1><p class="muted">حالة أيام الوحدات تتحدث تلقائياً من نتائج اختبارات الإتقان.</p>
      <div class="table-wrap"><table class="t"><caption class="sr-only">خطة الدراسة اليومية</caption><thead><tr><th scope="col">اليوم</th><th scope="col">الموضوع</th><th scope="col">النشاط</th><th scope="col">الحالة</th></tr></thead><tbody>${rows}</tbody></table></div>`;
  }
  function viewResources() {
    return `<h1>المصادر الموصى بها</h1><ul class="resources">` + D.resources.map(r => `<li><div class="row">
      <a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.name)}</a>
      <span class="pill ${r.level === "إلزامي" ? "p-bad" : r.level === "موصى به" ? "p-warn" : "p-c"}">${esc(r.level)}</span></div>
      <p class="muted">${esc(r.desc)}</p></li>`).join("") + "</ul>";
  }
  function view404() {
    return `<div class="panel lockbox"><h1>الصفحة غير موجودة</h1><p>الرابط الذي فتحته غير صحيح أو قديم.</p>
      <div class="row" style="justify-content:center"><a class="btn" href="#/">الصفحة الرئيسية</a><a class="btn ghost" href="#/search">ابحث عن درس</a></div></div>`;
  }

  /* ============================================================
     14) تشغيل الكود: أزرار «شغّل» والمحررات
     ============================================================ */
  // شرح مختصر بالعربية لأشهر الأخطاء (يظهر فوق رسالة بايثون الأصلية)
  const ERR_AR = {
    SyntaxError: "خطأ في الصياغة: بايثون لم تفهم طريقة الكتابة (قوس ناقص، نقطتان :، علامة تنصيص…).",
    IndentationError: "خطأ في الإزاحة: المسافات في بداية السطر غير صحيحة.",
    NameError: "اسم غير معرّف: استخدمت متغيراً أو دالة قبل تعريفها، أو أخطأت في كتابة الاسم.",
    TypeError: "نوع غير مناسب: العملية لا تصلح لهذا النوع من البيانات، أو عدد المدخلات غير صحيح.",
    ValueError: "قيمة غير مناسبة: النوع صحيح لكن القيمة نفسها لا تصلح.",
    IndexError: "فهرس خارج المدى: طلبت موقعاً غير موجود في القائمة أو النص.",
    KeyError: "مفتاح غير موجود في القاموس.",
    AttributeError: "هذا الكائن لا يملك الخاصية أو التابع المطلوب.",
    ZeroDivisionError: "قسمة على صفر.",
    FileNotFoundError: "الملف غير موجود في المجلد الحالي.",
    ModuleNotFoundError: "الوحدة غير موجودة أو غير متاحة في المتصفح.",
    UnboundLocalError: "استخدمت متغيراً محلياً قبل إعطائه قيمة داخل الدالة.",
    RecursionError: "استدعاء ذاتي بلا نهاية: تحقق من شرط التوقف.",
  };
  function outputHtml(r) {
    let h = "";
    if (r.out) h += `<pre dir="ltr" class="ro-out">${esc(r.out)}</pre>`;
    (r.figs || []).forEach(f => { h += `<img class="ro-fig" alt="الرسم البياني الناتج عن الكود" src="data:image/png;base64,${f}">`; });
    if (r.err) {
      const ar = ERR_AR[r.errName];
      h += `<div class="ro-err">${r.errName && r.errName !== "Timeout" ? `<span class="err exc" dir="ltr">${esc(r.errName)}</span> ` : ""}${ar ? esc(ar) : ""}<pre dir="ltr">${esc(r.err)}</pre></div>`;
    }
    if (!h) h = `<p class="small muted">انتهى التنفيذ دون أن يُطبع شيء.</p>`;
    return h;
  }
  async function runFrom(btn) {
    const box = btn.closest(".code, .editor");
    const code = box.classList.contains("editor") ? $("textarea", box).value : $("pre", box).textContent;
    const stdinBox = $(".stdin-box textarea", box);
    const files = box.dataset.files ? JSON.parse(box.dataset.files) : null;
    if (!code.trim()) { toast("اكتب كوداً أولاً"); return; }
    let out = box.nextElementSibling;
    if (!out || !out.classList.contains("run-out")) {
      out = document.createElement("div"); out.className = "run-out"; out.setAttribute("aria-live", "polite"); box.after(out);
    }
    btn.disabled = true;
    out.innerHTML = `<p class="small muted">${window.PY.isReady() ? "يعمل…" : "جارٍ تحميل بايثون في المتصفح (أول مرة فقط، قد يستغرق دقيقة)…"}</p>`;
    const stdin = stdinBox ? stdinBox.value + "\n" : (btn.dataset.stdin || "");
    const r = await window.PY.run(code, stdin, files);
    btn.disabled = false;
    out.innerHTML = (stdin ? `<p class="small muted">المُدخلات المستخدمة: <bdi dir="ltr">${esc(stdin.trim())}</bdi></p>` : "") + outputHtml(r);
    if (box.classList.contains("editor") && !r.err && !S.days.includes(today())) gain(0);
  }

  /* ============================================================
     15) الموجّه والأحداث
     ============================================================ */
  function setNav(route) {
    $$(".main-nav a").forEach(a => {
      const on = a.dataset.nav === route;
      if (on) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
  }
  function title(t) { document.title = t ? t + " – " + CFG.siteName : CFG.siteName + " – تعلّم بايثون بالإتقان المتدرّج"; }

  async function render() {
    const raw = location.hash.replace(/^#/, "") || "/";
    const [path, qs] = raw.split("?");
    const params = new URLSearchParams(qs || "");
    const parts = path.split("/").filter(Boolean);
    const app = $("#app");
    let html, nav = "", t = "";
    try {
      if (!parts.length) { html = viewHome(); nav = "home"; }
      else if (parts[0] === "u" && unitMeta(parts[1])) {
        const n = parts[1];
        if (!UNITS[n]) app.innerHTML = `<p class="muted" role="status">جارٍ تحميل الوحدة ${n}…</p>`;
        const u = await unitData(n);
        const sub = parts[2] || "";
        t = "الوحدة " + n + ": " + u.title;
        if (sub === "") html = viewUnit(u);
        else if (sub === "intro") html = viewLesson(u, "intro");
        else if (sub === "l" && /^\d+$/.test(parts[3] || "")) { html = viewLesson(u, +parts[3]); const L = u.lessons[+parts[3]]; if (L) t = L.key + " · " + t; }
        else if (sub === "cards") html = viewCards(u);
        else if (sub === "practice") html = viewPractice(u);
        else if (sub === "exercises") html = viewExercises(u);
        else if (sub === "test") html = viewTest(u);
        else html = view404();
      }
      else if (parts[0] === "plan") { html = viewPlan(); nav = "plan"; t = "خطة 30 يوماً"; }
      else if (parts[0] === "final") { html = viewFinal(); nav = "final"; t = "الاختبار الشامل"; }
      else if (parts[0] === "me") { html = viewMe(); nav = "me"; t = "تقدّمي"; }
      else if (parts[0] === "resources") { html = viewResources(); nav = "resources"; t = "المصادر"; }
      else if (parts[0] === "search") { html = viewSearch(params); nav = "search"; t = "البحث"; }
      else if (parts[0] === "verify") { html = viewVerify(params); t = "التحقق من رمز الإتمام"; }
      else if (parts[0] === "certificate") { html = viewCertificate(); t = "الشهادة"; }
      else { html = view404(); t = "الصفحة غير موجودة"; }
    } catch (e) {
      html = `<div class="panel lockbox"><h1>تعذّر تحميل المحتوى</h1><p>${navigator.onLine ? "تحقق من اتصالك بالإنترنت ثم أعد تحميل الصفحة." : "أنت غير متصل بالإنترنت، وهذه الوحدة لم تُفتح من قبل على هذا الجهاز. الوحدات التي فتحتها سابقاً تعمل دون اتصال."}</p><button class="btn" onclick="location.reload()">إعادة التحميل</button></div>`;
    }
    const isHome = nav === "home";
    document.body.classList.toggle("is-home", isHome);
    app.innerHTML = html;
    setNav(nav); title(t); paintXp();
    makeScrollablesFocusable();
  }

  // كتل الكود الأعرض من الشاشة تقبل التركيز، فيستطيع مستخدم لوحة المفاتيح تمريرها أفقياً (WCAG 2.1.1)
  function makeScrollablesFocusable() {
    $$("#app pre").forEach(p => {
      if (p.scrollWidth > p.clientWidth + 2) { p.tabIndex = 0; p.setAttribute("role", "region"); p.setAttribute("aria-label", "كود قابل للتمرير"); }
    });
  }
  window.addEventListener("resize", () => { clearTimeout(window.__pmRs); window.__pmRs = setTimeout(makeScrollablesFocusable, 200); });

  let lastPath = "";
  function onRoute() {
    const path = location.hash.split("?")[0];
    const changed = path !== lastPath;
    lastPath = path;
    if (cardSession && !path.includes("/cards")) cardSession = null;
    if (practice && !path.includes("/practice")) practice = null;
    if ("speechSynthesis" in window) speechSynthesis.cancel();
    render().then(() => {
      if (changed) {
        window.scrollTo(0, 0);
        const h1 = $("#app h1");
        if (h1) { h1.setAttribute("tabindex", "-1"); h1.focus({ preventScroll: true }); }   // قارئ الشاشة يعلن الصفحة الجديدة
      }
    });
  }

  function onClick(e) {
    const run = e.target.closest("[data-run], [data-run-editor]");
    if (run) { runFrom(run); return; }
    const say = e.target.closest("[data-say]");
    if (say) { speak(say.dataset.say); return; }
    const el = e.target.closest("[data-act]");
    if (!el) return;
    const a = el.dataset.act;
    const n = el.dataset.n;
    const u = n && UNITS[n];
    if (a === "done") {
      const id = el.dataset.id;
      if (S.lessons[id]) { delete S.lessons[id]; save(); render(); }
      else { S.lessons[id] = today(); gain(5, "أنهيت الدرس"); render(); }
    }
    else if (a === "flip") { cardSession.flipped = !cardSession.flipped; render().then(() => { const b = $(".flip-inner"); if (b) b.focus(); }); }
    else if (a === "grade") gradeCard(el.dataset.v === "1");
    else if (a === "cards-restart") { cardSession = null; render(); }
    else if (a === "cards-all") { const un = cardSession.n; cardSession = { n: un, queue: shuffle(UNITS[un].cards.map((_, i) => i)), pos: 0, flipped: false }; render(); }
    else if (a === "say-card") { const un = cardSession.n, c = UNITS[un].cards[cardSession.queue[cardSession.pos]]; speak(el.dataset.side === "b" ? c.sb : c.sf); }
    else if (a === "practice-pick") practicePick(el.dataset.v);
    else if (a === "practice-next") { practice.q = null; const pu = UNITS[practice.n], pool = pu.bank.concat(pu.gen); practice.q = pool[Math.floor(Math.random() * pool.length)]; practice.picked = null; render().then(() => { const q = $(".q-card .qt"); if (q) { q.setAttribute("tabindex", "-1"); q.focus(); } }); }
    else if (a === "retake") { startAttempt(el.dataset.kind, el.dataset.kind === "final" ? null : u); render(); window.scrollTo(0, 0); }
    else if (a === "pick") {
      const st = testState(el.dataset.kind, el.dataset.kind === "final" ? null : n);
      const pool = testPool(el.dataset.kind, u), q = pool.find(x => x.id === +el.dataset.id);
      st.cur.ans[q.id] = q.o ? +el.dataset.v : el.dataset.v;
      save();
      $$(`[data-id="${q.id}"]`).forEach(b => b.setAttribute("aria-pressed", String(b === el)));
      const cnt = Object.keys(st.cur.ans).length, tot = st.cur.order.length;
      $("#cnt").textContent = `أجبت عن ${cnt} من ${tot}`;
      $("#submit").disabled = cnt < tot;
    }
    else if (a === "submit") submitTest(el.dataset.kind, el.dataset.kind === "final" ? null : u);
    else if (a === "ex") {
      const prev = S.ex[el.dataset.n];
      S.ex[el.dataset.n] = el.dataset.v;
      if (el.dataset.v === "solved" && prev !== "solved") gain(10, "حللت تمريناً"); else save();
      render();
    }
    else if (a === "plan") { S.plan[el.dataset.d] = el.checked; save(); }
    else if (a === "edit-student") { $("#app .me-head").outerHTML = studentForm(); }
    else if (a === "copy") { navigator.clipboard.writeText($("#ccode").textContent).then(() => toast("نُسخ الرمز")); }
    else if (a === "export") {
      const blob = new Blob([JSON.stringify(S)], { type: "application/json" });
      const link = document.createElement("a"); link.href = URL.createObjectURL(blob);
      link.download = "python-mastery-progress-" + today() + ".json"; link.click(); URL.revokeObjectURL(link.href);
    }
    else if (a === "reset") { if (confirm("سيُمسح كل تقدّمك على هذا الجهاز نهائياً. هل أنت متأكد؟")) { S = blank(); save(); render(); } }
    else if (a === "clear-weak") { S.weak = {}; save(); render(); }
    else if (a === "verify") { $("#vout").innerHTML = verifyCode($("#vcode").value); }
    else if (a === "teacher-off") { S.teacher = false; save(); render(); }
    else if (a === "print") window.print();
  }

  function onSubmit(e) {
    const f = e.target;
    if (f.matches("[data-student]")) {
      e.preventDefault();
      const name = f.name.value.trim(), id = f.id.value.trim();
      if (!name || !id) return;
      S.student = { name, id }; save(); toast("حُفظت البيانات"); render();
    } else if (f.matches("[data-search]")) {
      e.preventDefault();
      location.hash = "#/search?q=" + encodeURIComponent(f.q.value.trim());
    } else if (f.matches("[data-teacher]")) {
      e.preventDefault();
      if (hash(f.pw.value + SALT) === CFG.teacherHash) { S.teacher = true; save(); toast("فُعّل وضع المدرس"); render(); }
      else toast("كلمة المرور غير صحيحة");
    }
  }

  function onKey(e) {
    if (!cardSession || !location.hash.includes("/cards") || e.target.matches("input, textarea")) return;
    if ((e.key === " " || e.key === "Enter") && !e.target.closest("button:not(.flip-inner)")) { e.preventDefault(); $(".flip-inner") && $(".flip-inner").click(); }
    else if (cardSession.flipped && e.key === "1") gradeCard(false);
    else if (cardSession.flipped && e.key === "2") gradeCard(true);
  }

  function onChange(e) {
    if (e.target.id === "imp") {
      const file = e.target.files[0]; if (!file) return;
      file.text().then(t => {
        try { const s = JSON.parse(t); if (s.v !== 2) throw 0; S = Object.assign(blank(), s); save(); toast("استُورد التقدم"); render(); }
        catch (_) { toast("ملف غير صالح"); }
      });
    }
    if (e.target.dataset.ex) { S.exCode = S.exCode || {}; S.exCode[e.target.dataset.ex] = e.target.value; save(); }
  }

  // مفتاح Tab داخل المحرر يكتب أربع مسافات (Shift+Tab يخرج من المحرر للحفاظ على التنقل بلوحة المفاتيح)
  function onEditorKey(e) {
    if (e.key === "Tab" && !e.shiftKey && e.target.matches(".editor textarea") && !e.target.dataset.tabOut) {
      e.preventDefault();
      const t = e.target, s = t.selectionStart;
      t.setRangeText("    ", s, t.selectionEnd, "end");
    }
    if (e.key === "Escape" && e.target.matches(".editor textarea")) e.target.dataset.tabOut = "1";
  }

  /* ---------- الرأس والتذييل: الإعدادات ---------- */
  function prefs() { try { return JSON.parse(localStorage.getItem("pm_prefs")) || {}; } catch (e) { return {}; } }
  function setPrefs(p) { try { localStorage.setItem("pm_prefs", JSON.stringify(p)); } catch (e) { /* */ } }
  function paintPrefs() {
    const d = document.documentElement, dark = d.getAttribute("data-theme") === "dark", hc = d.getAttribute("data-contrast") === "high";
    const bt = $("#btn-theme"), bc = $("#btn-contrast"), bf = $("#btn-font");
    bt.innerHTML = dark ? ICON.sun : ICON.moon; bt.setAttribute("aria-pressed", String(dark)); bt.setAttribute("aria-label", dark ? "الوضع الفاتح" : "الوضع الليلي");
    bc.innerHTML = ICON.contrast; bc.setAttribute("aria-pressed", String(hc));
    const f = d.getAttribute("data-font"), names = { s: "صغير", m: "متوسط", l: "كبير" };
    bf.setAttribute("aria-label", `حجم الخط: ${names[f]}. اضغط للتغيير`);
    bf.textContent = f === "s" ? "ع-" : f === "l" ? "ع+" : "ع";
    $('meta[name="theme-color"]').setAttribute("content", hc ? "#000000" : "#0F2438");
  }
  function initPrefs() {
    const d = document.documentElement;
    $("#btn-theme").addEventListener("click", () => {
      const p = prefs(); p.theme = d.getAttribute("data-theme") === "dark" ? "light" : "dark"; d.setAttribute("data-theme", p.theme); setPrefs(p); paintPrefs();
    });
    $("#btn-contrast").addEventListener("click", () => {
      const p = prefs(); p.contrast = d.getAttribute("data-contrast") === "high" ? "" : "high";
      if (p.contrast) d.setAttribute("data-contrast", "high"); else d.removeAttribute("data-contrast"); setPrefs(p); paintPrefs();
    });
    $("#btn-font").addEventListener("click", () => {
      const order = ["s", "m", "l"], p = prefs(); p.font = order[(order.indexOf(d.getAttribute("data-font")) + 1) % 3];
      d.setAttribute("data-font", p.font); setPrefs(p); paintPrefs(); announce("حجم الخط تغيّر");
    });
    paintPrefs();
  }
  function initFooter() {
    $("#year").textContent = new Date().getFullYear();
    $("#ft-uni").textContent = CFG.university;
    const A = CFG.author, links = [];
    if (A.github) links.push(`<a href="${esc(A.github)}" target="_blank" rel="noopener">${ICON.gh}GitHub</a>`);
    if (A.linkedin) links.push(`<a href="${esc(A.linkedin)}" target="_blank" rel="noopener">${ICON.in}LinkedIn</a>`);
    if (A.scholar) links.push(`<a href="${esc(A.scholar)}" target="_blank" rel="noopener">${ICON.scholar}Google Scholar</a>`);
    if (A.email) links.push(`<a href="mailto:${esc(A.email)}">${ICON.mail}Email</a>`);
    $("#author-links").innerHTML = links.join("");
  }

  async function start() {
    initPrefs(); initFooter();
    try { D = await getJSON("core.json"); }
    catch (e) { $("#app").innerHTML = `<div class="panel lockbox"><h1>تعذّر تحميل الموقع</h1><p>تحقق من اتصالك بالإنترنت ثم أعد تحميل الصفحة.</p></div>`; return; }
    document.addEventListener("click", onClick);
    document.addEventListener("submit", onSubmit);
    document.addEventListener("keydown", onKey);
    document.addEventListener("keydown", onEditorKey);
    document.addEventListener("change", onChange);
    document.addEventListener("input", e => { if (e.target.dataset && e.target.dataset.ex) onChange(e); });
    window.addEventListener("hashchange", onRoute);
    onRoute();
    if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost")) navigator.serviceWorker.register("sw.js").catch(() => {});
  }
  start();
})();
