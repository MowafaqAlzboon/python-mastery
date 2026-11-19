# -*- coding: utf-8 -*-
"""
verify_all.py — التحقق الآلي من كل الوحدات المكتوبة بالأسلوب التربوي
1) كل عنصر يحتوي الحقول الإلزامية الـ 12 (وإجابات التمارين)
2) كل مفتاح يطابق صفاً في المحتوى الأصلي (python_mastery_workbook.py)، ولا يُفقد صف
3) تشغيل كل مقطع كود فعلياً:
   - المثال الصحيح يعمل ويعطي الناتج المكتوب حرفياً
   - المثال الخاطئ يطلق الخطأ المذكور بالضبط (أو يعطي الناتج الخاطئ المذكور للخطأ المنطقي)
   - تمرين الإصلاح خاطئ قبل الإصلاح، وصحيح بعده
التشغيل: python verify_all.py
"""
import importlib
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import python_mastery_workbook as wbk  # noqa: E402

FIELDS = ["real", "what", "name", "why", "goal", "syntax", "good", "good_out", "bad", "bad_err", "bad_why",
          "explain_q", "explain", "explain_ans", "write", "write_ans", "fix", "fix_err", "fix_ans", "fix_why", "bonus"]
NO_EXCEPTION = {"خطأ منطقي", "مخالفة أسلوب", None}

# (الوحدة، الوحدة البرمجية، اسم قائمة الدروس، الجدول الأصلي)
UNITS = [
    ("01", "lesson_keywords", "KEYWORDS_LESSON", wbk.KEYWORDS),
    ("02", "lesson_unit02", "LESSONS", wbk.NAMING_RULES),
    ("03", "lesson_unit03", "LESSONS", wbk.DATA_TYPES),
    ("04", "lesson_unit04", "LESSONS", wbk.OPERATORS),
    ("05", "lesson_unit05", "LESSONS", wbk.BUILTINS),
    ("06", "lesson_unit06", "LESSONS", wbk.CONTROL),
    ("07", "lesson_unit07", "LESSONS", wbk.STRINGS),
    ("08", "lesson_unit08", "LESSONS", wbk.COLLECTIONS, True),
    ("09", "lesson_unit09", "LESSONS", wbk.FUNCTIONS),
    ("10", "lesson_unit10", "LESSONS", wbk.FILES),
    ("11", "lesson_unit11", "LESSONS", wbk.ERRORS),
    ("12", "lesson_unit12", "LESSONS", wbk.OOP),
    ("13", "lesson_unit13", "LESSONS", wbk.MODULES),
]

TMP = tempfile.mkdtemp()
os.chmod(TMP, 0o777)


def _as_student():
    """تشغيل المقطع بمستخدم عادي (لا root) حتى تظهر أخطاء الصلاحيات كما على حاسوب الطالب."""
    if os.getuid() == 0:
        os.setgid(65534)
        os.setuid(65534)


def run(code, stdin=""):
    """تشغيل مقطع في عملية ومجلد مستقلين؛ يرجع (اسم الخطأ أو None، الناتج)."""
    work = tempfile.mkdtemp(dir=TMP)
    os.chmod(work, 0o777)
    path = os.path.join(work, "snippet.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    os.chmod(path, 0o644)
    env = dict(os.environ, PYTHONBREAKPOINT="0", PYTHONIOENCODING="utf-8", MPLBACKEND="Agg",
               MPLCONFIGDIR=work, HOME=work)
    try:
        p = subprocess.run([sys.executable, "-W", "ignore", path], capture_output=True, text=True,
                           timeout=30, cwd=work, input=stdin, env=env, preexec_fn=_as_student)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", ""
    if p.returncode == 0:
        return None, p.stdout.strip()
    last = [line for line in p.stderr.strip().splitlines() if line.strip()][-1]
    m = re.match(r"([\w.]+)", last)          # مثل io.UnsupportedOperation ← UnsupportedOperation
    return (m.group(1).split(".")[-1] if m else last), p.stdout.strip()


def check_unit(number, module_name, list_name, source_rows, pair_keys=False):
    mod = importlib.import_module(module_name)
    lessons = list(getattr(mod, list_name))
    reused = list(getattr(mod, "REUSED", {}).values())
    problems, executed = [], 0

    # (2) تغطية المحتوى الأصلي
    source_keys = [f"{r[0]} [{r[1]}]" if pair_keys else r[0] for r in source_rows]
    lesson_keys = [k["key"] for k in lessons + reused]
    missing = [k for k in source_keys if k not in lesson_keys]
    extra = [k for k in lesson_keys if k not in source_keys]
    dupes = {k for k in lesson_keys if lesson_keys.count(k) > 1}
    if missing: problems.append(f"صفوف أصلية بلا درس: {missing}")
    if extra: problems.append(f"دروس بلا صف أصلي: {extra}")
    if dupes: problems.append(f"مفاتيح مكررة: {dupes}")

    for k in [mod.UNIT_INTRO] + lessons:
        key = k["key"]
        miss = [f for f in FIELDS if not k.get(f)]
        if miss:
            problems.append(f"{key}: حقول ناقصة {miss}")

        def check(label, code, expect_err=None, expect_out=None):
            nonlocal executed
            if expect_err == "حلقة لا نهائية" or label in k.get("skip", ()):
                return
            executed += 1
            stdin = k.get(f"{label}_stdin", k.get("stdin", ""))
            if k.get(f"{label}_cmp") is False or (label == "good" and k.get("good_cmp") is False):
                expect_out = None
            err, out = run(code, stdin)
            if expect_err in NO_EXCEPTION:
                if err:
                    problems.append(f"{key}/{label}: خطأ غير متوقع {err}")
                elif expect_out is not None and out != expect_out:
                    problems.append(f"{key}/{label}: الناتج {out!r} ≠ {expect_out!r}")
            elif err != expect_err:
                problems.append(f"{key}/{label}: ظهر {err!r} والمتوقع {expect_err}")

        check("good", k["good"], None, k["good_out"])
        check("bad", k["bad"], k["bad_err"], k.get("bad_out"))
        check("explain", k["explain"], k.get("explain_err"), k.get("explain_out"))
        check("write_ans", k["write_ans"])
        check("fix", k["fix"], k["fix_err"], k.get("fix_out"))
        check("fix_ans", k["fix_ans"], k.get("fix_ans_err"))
        if k.get("bonus_code"):
            check("bonus", k["bonus_code"])
    return len(lessons), len(reused), executed, problems


if __name__ == "__main__":
    total_bad = 0
    for unit in UNITS:
        n, r, ex, probs = check_unit(*unit)
        total_bad += len(probs)
        print(f"الوحدة {unit[0]}: {n} درساً جديداً + {r} معاد استخدامه | مقاطع مُشغّلة: {ex} | مشكلات: {len(probs)}")
        for p in probs:
            print("   -", p)
    print("النتيجة:", "✅ كل شيء سليم" if total_bad == 0 else f"❌ {total_bad} مشكلة")
