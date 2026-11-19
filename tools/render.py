# -*- coding: utf-8 -*-
"""
render.py — تحويل درس (قاموس بالنقاط الـ 12) إلى HTML جاهز للموقع.

لماذا نولّد HTML مسبقاً بدل بنائه في المتصفح؟
- معالجة اتجاه النص (عربي داخل كود، كود داخل جملة عربية) دقيقة ومُختبرة هنا مرة واحدة.
- المتصفح يعرض فقط، فيصبح الموقع أسرع وأبسط.

أزرار «شغّل» تحمل الكود داخل <pre> نفسه، ويقرؤه app.js عبر textContent ثم يشغّله بـ Pyodide.
"""
import html
import re

E = html.escape

# النقاط الـ 12 بالترتيب الإلزامي: (الرمز، العنوان)
POINTS = {
    "real": ("🌍", "مثال من أرض الواقع"), "what": ("📖", "ما هو؟"),
    "name": ("❓", "لماذا سُمّي بهذا الاسم؟"), "why": ("🎯", "ما أهميته؟"),
    "goal": ("🛠️", "ما الغاية منه؟"), "syntax": ("💻", "كيف يُكتب؟"),
    "good": ("✅", "مثال صحيح"), "bad": ("❌", "مثال خاطئ"),
    "explain": ("🔍", "تمرين تفسير"), "write": ("✏️", "تمرين كتابة"),
    "fix": ("🔧", "تمرين إيجاد الخطأ"), "bonus": ("💡", "معلومة إضافية"),
}
LOGIC_ERRORS = ("خطأ منطقي", "حلقة لا نهائية", "مخالفة أسلوب")

ARABIC = re.compile(r"[؀-ۿ][؀-ۿ0-9_]*(?:\s+[؀-ۿ][؀-ۿ0-9_]*)*")
FORMULA = re.compile(r"[<>=+\-*/%\[\]&|^~:]")
LATIN_RUN = re.compile(r"(?![.,:;])[!-~](?:[ !-~]*[!-~])?")
CODE_CHARS = re.compile(r"[A-Za-z0-9<>=!+*/%&|^~_\-\[\]{}\"'#@$]")


def prose(text):
    """نص عربي مع عزل كل مقطع إنجليزي/برمجي باتجاه LTR (وإلا انقلب <= إلى => مثلاً)."""
    out, last = [], 0
    for m in LATIN_RUN.finditer(text):
        run = m.group(0)
        core = run.rstrip(".,:;")
        tail = run[len(core):]
        head = ""
        # قوس غير مغلق داخل المقطع يخص الجملة العربية لا الكود
        while core.startswith("(") and core.count("(") > core.count(")"):
            head, core = head + "(", core[1:]
        while core.endswith(")") and core.count(")") > core.count("("):
            tail, core = ")" + tail, core[:-1]
        out.append(E(text[last:m.start()]) + E(head))
        out.append(f'<bdi dir="ltr">{E(core)}</bdi>' if CODE_CHARS.search(core) else E(core))
        out.append(E(tail))
        last = m.end()
    out.append(E(text[last:]))
    return "".join(out)


def key_html(key):
    """عنوان العنصر: العربي من اليمين بخط النص، والبرمجي من اليسار بخط الكود. يرجع (html, dir, class)."""
    label = re.match(r"^[؀-ۿ]+: ", key)          # مثل «مفهوم: pip install»
    if ARABIC.search(key) and (label or not FORMULA.search(key)):
        return prose(key), "rtl", "k-ar"
    return ARABIC.sub(lambda m: f"<bdi>{m.group(0)}</bdi>", E(key)), "ltr", "k-code"


def pre(c):
    """كود من اليسار لليمين، مع عزل الكلمات العربية داخله (bdi) كي لا ينقلب ترتيبها."""
    return '<pre dir="ltr"><code>' + ARABIC.sub(lambda m: f"<bdi>{m.group(0)}</bdi>", E(c)) + "</code></pre>"


def _runnable(c, stdin="", label="شغّل"):
    """كتلة كود مع زر تشغيل؛ مخرجات التشغيل تُضاف تحتها في المتصفح."""
    s = f' data-stdin="{E(stdin)}"' if stdin else ""
    return (f'<div class="code">{pre(c)}<button class="run" type="button" data-run{s}>'
            f'<span aria-hidden="true">▶</span> {label}</button></div>')


def editor(initial, aria, stdin=""):
    """محرر صغير يكتب فيه الطالب ويشغّل كوده."""
    s = f' data-stdin="{E(stdin)}"' if stdin else ""
    rows = max(4, min(14, initial.count("\n") + 2))
    return (f'<div class="editor"><textarea dir="ltr" spellcheck="false" rows="{rows}" aria-label="{E(aria)}">{E(initial)}</textarea>'
            f'<button class="run" type="button" data-run-editor{s}><span aria-hidden="true">▶</span> شغّل كودك</button></div>')


def output(o):
    if not o:
        return '<div class="out"><span>الناتج:</span> <em>لا شيء يُطبع</em></div>'
    return f'<div class="out"><span>الناتج:</span><pre dir="ltr">{E(o)}</pre></div>'


def err_badge(e):
    cls = "logic" if e in LOGIC_ERRORS else "exc"
    return f'<span class="err {cls}" dir="auto">{E(e)}</span>'


def point(key, body, n):
    icon, title = POINTS[key]
    return (f'<section class="pt pt-{key}"><h3 class="pt-h"><span class="pn">{n}</span>'
            f'<span aria-hidden="true">{icon}</span> {title}</h3><div class="pb">{body}</div></section>')


def stdin_of(k, label):
    return k.get(f"{label}_stdin", k.get("stdin", ""))


NOT_IN_BROWSER = '<p class="small muted">هذا المثال يعمل على حاسوبك فقط (المتصفح لا يدعم هذه الوحدة).</p>'


def lesson_body(k):
    """النقاط الـ 12 لدرس واحد."""
    skip = set(k.get("browser_skip", ()))

    def runnable(c, stdin="", label="شغّل", which=None):     # يحجب زر التشغيل عن أمثلة لا تعمل في المتصفح
        return (pre(c) + NOT_IN_BROWSER) if which in skip else _runnable(c, stdin, label)
    p = [
        point("real", f"<p>{prose(k['real'])}</p>", 1),
        point("what", f"<p>{prose(k['what'])}</p>", 2),
        point("name", f"<p>{prose(k['name'])}</p>", 3),
        point("why", f"<p>{prose(k['why'])}</p>", 4),
        point("goal", f"<p>{prose(k['goal'])}</p>", 5),
        point("syntax", pre(k["syntax"]), 6),
    ]
    good = runnable(k["good"], stdin_of(k, "good"), which="good") + output(k["good_out"])
    if k.get("stdin"):
        good += f'<p class="small muted">عند تشغيله أُدخلت القيمة: <bdi dir="ltr">{E(k["stdin"].strip())}</bdi></p>'
    p.append(point("good", good, 7))

    bad_code = runnable(k["bad"], stdin_of(k, "bad"), "شغّل وشاهد الخطأ") if k["bad_err"] != "حلقة لا نهائية" else pre(k["bad"])
    bad = bad_code + f'<p class="bad-why">{err_badge(k["bad_err"])} {prose(k["bad_why"])}</p>'
    if k.get("bad_out"):
        bad += output(k["bad_out"])
    p.append(point("bad", bad, 8))

    p.append(point("explain",
                   f'<p class="task">{prose(k["explain_q"])}</p>' + pre(k["explain"]) +
                   '<p class="small muted">فكّر في الإجابة أولاً، ثم افتحها وتحقّق بالتشغيل.</p>'
                   f'<details><summary>اعرض الإجابة</summary><p>{prose(k["explain_ans"])}</p>'
                   + runnable(k["explain"], stdin_of(k, "explain"), "تحقّق بالتشغيل") + "</details>", 9))

    p.append(point("write",
                   f'<p class="task">{prose(k["write"])}</p>'
                   + editor("", "اكتب حلك هنا", stdin_of(k, "write_ans")) +
                   f'<details><summary>اعرض حلاً نموذجياً</summary>{runnable(k["write_ans"], stdin_of(k, "write_ans"))}</details>', 10))

    fix_ans = runnable(k["fix_ans"], stdin_of(k, "fix_ans"), which="fix_ans")
    if k.get("fix_ans_err"):
        fix_ans += f'<p class="small muted">بعد التصحيح يُطلق الكود {E(k["fix_ans_err"])} كما ينبغي.</p>'
    fix_initial = k["fix"] if k["fix_err"] != "حلقة لا نهائية" else k["fix"]
    p.append(point("fix",
                   '<p class="task">في الكود التالي خطأ. صحّحه داخل المحرر ثم شغّله.</p>'
                   + editor(fix_initial, "صحّح الكود هنا", stdin_of(k, "fix")) +
                   f'<details><summary>اعرض التصحيح</summary><p>{err_badge(k["fix_err"])} {prose(k["fix_why"])}</p>{fix_ans}</details>', 11))

    bonus = f"<p>{prose(k['bonus'])}</p>" + (runnable(k["bonus_code"]) if k.get("bonus_code") else "")
    p.append(point("bonus", bonus, 12))
    return '<div class="pts">' + "".join(p) + "</div>"
