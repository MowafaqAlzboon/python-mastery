# -*- coding: utf-8 -*-
"""
build_data.py — يولّد بيانات الموقع من ملفات المحتوى (content/).

التشغيل من جذر المستودع:
    python tools/build_data.py

الناتج (assets/data/):
    core.json   : قائمة الوحدات ومجموعاتها، التمارين، الخطة، المصادر، الاختبار الشامل
    uNN.json    : لكل وحدة: المقدمة والدروس (HTML جاهز) والبطاقات وأسئلة التدريب والإتقان
    search.json : فهرس بحث خفيف بكل عناوين الدروس

ملاحظة الأمان التعليمي: الإجابات الصحيحة لا تُكتب صراحة؛ يُكتب «رمز تحقق» فقط
(نفس معادلة ملف Excel: (id*37 + رقم_الإجابة*101) % 997).
"""
import hashlib
import importlib
import json
import os
import random
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "content"))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import python_mastery_workbook as wbk  # noqa: E402
from render import E, key_html, lesson_body, pre, prose  # noqa: E402

OUT = os.path.join(ROOT, "assets", "data")
RNG = random.Random(2026)

# (الرقم، الوحدة البرمجية، اسم قائمة الدروس، العنوان، العنوان الإنجليزي)
UNITS = [
    ("01", "lesson_keywords", "KEYWORDS_LESSON", "الكلمات المحجوزة", "Keywords"),
    ("02", "lesson_unit02", "LESSONS", "قواعد التسمية", "Naming Rules & PEP 8"),
    ("03", "lesson_unit03", "LESSONS", "أنواع البيانات", "Data Types"),
    ("04", "lesson_unit04", "LESSONS", "العوامل", "Operators"),
    ("05", "lesson_unit05", "LESSONS", "الدوال المدمجة", "Built-in Functions"),
    ("06", "lesson_unit06", "LESSONS", "هياكل التحكم", "Control Flow"),
    ("07", "lesson_unit07", "LESSONS", "السلاسل النصية", "String Methods"),
    ("08", "lesson_unit08", "LESSONS", "القوائم والقواميس والمجموعات", "Lists, Dicts & Sets"),
    ("09", "lesson_unit09", "LESSONS", "الدوال", "Functions"),
    ("10", "lesson_unit10", "LESSONS", "الملفات", "File Handling"),
    ("11", "lesson_unit11", "LESSONS", "معالجة الأخطاء", "Exceptions"),
    ("12", "lesson_unit12", "LESSONS", "البرمجة الكائنية", "Object-Oriented Programming"),
    ("13", "lesson_unit13", "LESSONS", "الوحدات والمكتبات", "Modules & Libraries"),
]
LETTERS_TF = ["صح", "خطأ"]
TEST_ORIGINAL, TEST_GENERATED = 15, 5          # تركيب اختبار الإتقان في كل محاولة
COMMON_ERRORS = ["SyntaxError", "NameError", "TypeError", "ValueError", "IndexError", "KeyError",
                 "AttributeError", "ZeroDivisionError", "IndentationError", "FileNotFoundError",
                 "ModuleNotFoundError", "UnboundLocalError", "ImportError"]


# مدخلات تجريبية لتمارين input() (يستطيع الطالب تغييرها في الموقع)
EX_INPUT = {2: "70\n1.75\n", 3: "38.5\n", 4: "atgcgcta\n", 9: "20\n", 10: "27.3\n", 15: "60\n",
            17: "ATGXC\n", 29: "abc\n200\n45\n"}
SAMPLE_FASTA = ">BRCA1 human breast cancer gene\nATGGATTTATCTGCTCTTCGCGTTGAAGAAG\nTACAAAATGTCATTAATGCTATGCAGAAAATC\n>TP53 tumor protein p53\nATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCC\n>INS insulin\nATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCG\n"
# ملفات تجريبية تُنشأ في مجلد التشغيل قبل تنفيذ كود التمرين
EX_FILES = {
    26: {"patients.csv": "id,name,age,ward\nP1,Sara,40,A\nP2,Ali,55,B\nP3,Huda,61,A\nP4,Omar,33,C\n"},
    28: {"genes.fasta": SAMPLE_FASTA},
    49: {"genes.fasta": SAMPLE_FASTA},
}


def answer_code(qid, answer_no):
    return (qid * 37 + answer_no * 101) % 997


def plain(text):
    """نص بلا وسوم لقراءة البطاقة صوتياً."""
    return re.sub(r"\s+", " ", text).strip()


def ordered_lessons(mod, list_name):
    """الدروس الجديدة + المعاد استخدامها، مرتبة حسب مجموعات الوحدة."""
    items = list(getattr(mod, list_name)) + list(getattr(mod, "REUSED", {}).values())
    groups = mod.GROUPS
    gkeys = [g[0] for g in groups]
    stray = [k["key"] for k in items if k["group"] not in gkeys]
    assert not stray, f"دروس بلا مجموعة: {stray}"
    out = []
    for g in gkeys:
        out += [k for k in items if k["group"] == g]
    return out, groups


def find_lesson(keys, ref_key):
    """ربط مرجع السؤال (مثل «append()») بفهرس الدرس (مثل «append() [list]»)."""
    if ref_key in keys:
        return keys.index(ref_key)
    for i, k in enumerate(keys):
        if k.startswith(ref_key + " [") or k.split(" ")[-1] == ref_key or ref_key in k:
            return i
    return None


def original_question(q, unit_keys, misses):
    text, cp = q["text"], None
    prefix = "ما ناتج تنفيذ: "
    if text.startswith(prefix):
        text, cp = "ما ناتج تنفيذ الكود التالي؟", q["text"][len(prefix):]
    unit = q["ref"].split(" • ")[0][:2]
    ref_key = q["ref"].split(" • ", 1)[1]
    li = find_lesson(unit_keys[unit], ref_key)
    if li is None:
        misses.append(q["ref"])
    if q["options"]:
        no = q["options"].index(q["correct"]) + 1
    else:
        no = LETTERS_TF.index(q["correct"]) + 5
    return {"id": q["id"], "u": unit, "k": q["kind"], "d": q["difficulty"], "t": prose(text),
            "cp": pre(cp) if cp else None, "o": q["options"], "code": answer_code(q["id"], no),
            "l": li, "src": "bank"}


def generated_questions(unit, lessons, start_id):
    """
    أسئلة إضافية مأخوذة من دروس الوحدة نفسها (مُتحقق من صحتها بالتشغيل في verify_all.py):
    1) «أي خطأ يظهر؟» من المثال الخاطئ عندما يكون الخطأ استثناءً حقيقياً.
    2) «ما الناتج؟» من المثال الصحيح عندما يكون الناتج سطراً قصيراً.
    """
    out, qid = [], start_id
    outputs = [k["good_out"] for k in lessons if k["good_out"] and "\n" not in k["good_out"] and len(k["good_out"]) <= 30]
    for li, k in enumerate(lessons):
        err = k["bad_err"]
        if err not in ("خطأ منطقي", "حلقة لا نهائية", "مخالفة أسلوب") and k["bad"].count("\n") < 9:
            pool = [e for e in COMMON_ERRORS if e != err]
            opts = RNG.sample(pool, 3) + [err]
            RNG.shuffle(opts)
            qid += 1
            out.append({"id": qid, "u": unit, "k": "أي خطأ يظهر؟", "d": "متوسط",
                        "t": "ما اسم الخطأ الذي يظهر عند تشغيل هذا الكود؟", "cp": pre(k["bad"]),
                        "o": opts, "code": answer_code(qid, opts.index(err) + 1), "l": li, "src": "gen"})
        go = k["good_out"]
        if (go and "\n" not in go and len(go) <= 30 and not k.get("stdin") and k["good"].count("\n") < 9
                and k.get("good_cmp") is not False):
            pool = list({o for o in outputs if o != go})
            if len(pool) >= 3:
                opts = RNG.sample(pool, 3) + [go]
                RNG.shuffle(opts)
                qid += 1
                out.append({"id": qid, "u": unit, "k": "ما الناتج؟", "d": "متوسط",
                            "t": "ما ناتج تنفيذ الكود التالي؟", "cp": pre(k["good"]),
                            "o": opts, "code": answer_code(qid, opts.index(go) + 1), "l": li, "src": "gen"})
    return out, qid


def card(k):
    """بطاقة تذكّر مشتقة من الدرس: الوجه = العنصر، الظهر = تعريفه وطريقة كتابته."""
    inner, kdir, kcls = key_html(k["key"])
    return {"f": f'<span dir="{kdir}" class="{kcls}">{inner}</span>',
            "b": f"<p>{prose(k['what'])}</p>{pre(k['syntax'])}",
            "sf": k["key"], "sb": plain(k["what"])}


def stamp_service_worker():
    """تحديث رقم نسخة sw.js من بصمة كل ملفات الموقع، حتى يحصل الطلبة على النسخة الجديدة تلقائياً."""
    h = hashlib.sha1()
    for folder in ("assets", "."):
        base = os.path.join(ROOT, folder)
        for dirpath, _, files in sorted(os.walk(base)):
            if folder == "." and dirpath != base:
                continue
            for name in sorted(files):
                if name.endswith((".html", ".css", ".js", ".json", ".webmanifest")) and name != "sw.js":
                    h.update(open(os.path.join(dirpath, name), "rb").read())
    sw = os.path.join(ROOT, "sw.js")
    text = open(sw, encoding="utf-8").read()
    text = re.sub(r'const VERSION = "pm-[0-9a-f]+";', f'const VERSION = "pm-{h.hexdigest()[:10]}";', text)
    open(sw, "w", encoding="utf-8").write(text)


def main():
    os.makedirs(OUT, exist_ok=True)
    mods = {n: importlib.import_module(m) for n, m, *_ in UNITS}
    unit_lessons, unit_groups = {}, {}
    for n, m, ln, *_ in UNITS:
        unit_lessons[n], unit_groups[n] = ordered_lessons(mods[n], ln)
    unit_keys = {n: [k["key"] for k in ls] for n, ls in unit_lessons.items()}

    misses = []
    bank = {}
    for q in wbk.UNIT_TESTS:
        oq = original_question(q, unit_keys, misses)
        bank.setdefault(oq["u"], []).append(oq)
    final = [original_question(q, unit_keys, misses) for q in wbk.FINAL_EXAM]

    core_units, search, gen_id = [], [], 5000
    total_cards = total_q = 0
    for i, (n, m, ln, title, en) in enumerate(UNITS):
        mod, lessons, groups = mods[n], unit_lessons[n], unit_groups[n]
        gen, gen_id = generated_questions(n, lessons, gen_id)
        lesson_list = []
        for li, k in enumerate(lessons):
            inner, kdir, kcls = key_html(k["key"])
            lesson_list.append({
                "key": k["key"], "kh": inner, "kd": kdir, "kc": kcls, "g": k["group"], "lvl": k["level"],
                "reused": k.get("reused_from"), "html": lesson_body(k)})
            search.append([n, li, k["key"], plain(k["what"])[:90]])
        unit = {
            "n": n, "title": title, "en": en,
            "intro": {"key": mod.UNIT_INTRO["key"], "html": lesson_body(mod.UNIT_INTRO)},
            "groups": [{"id": g[0], "title": g[1], "desc": g[2]} for g in groups],
            "lessons": lesson_list,
            "cards": [card(k) for k in lessons],
            "bank": bank.get(n, []),
            "gen": gen,
            "test": {"original": min(TEST_ORIGINAL, len(bank.get(n, []))),
                     "generated": min(TEST_GENERATED, len(gen))},
        }
        total_cards += len(unit["cards"])
        total_q += len(unit["bank"]) + len(gen)
        with open(os.path.join(OUT, f"u{n}.json"), "w", encoding="utf-8") as f:
            json.dump(unit, f, ensure_ascii=False, separators=(",", ":"))
        core_units.append({
            "n": n, "title": title, "en": en, "course": "P1" if i < 10 else "P2",
            "count": len(lessons), "groups": [{"id": g[0], "title": g[1]} for g in groups],
            "lessons": [[k["key"], k["group"]] for k in lessons]})

    exercises = []
    for idx, ((t, d, s, sol, lvl), u) in enumerate(zip(wbk.EXERCISES_RAW, wbk.EXERCISE_UNITS), start=1):
        exercises.append({"n": idx, "t": t, "u": u[:2], "d": d, "hint": s, "lvl": lvl, "sol": sol,
                          "stdin": EX_INPUT.get(idx, ""), "files": EX_FILES.get(idx),
                          "c": "P2" if (wbk.UNIT_COURSE[u] == "البرمجة 2" or idx in wbk.EXERCISE_P2) else "P1",
                          "tr": wbk.track_of([t, d, sol])})
    plan = [{"day": i, "topic": p[1],
             "u": (p[2][:2] if p[2] in wbk.UNITS else ("final" if p[2] == wbk.S15 else None)), "act": p[4]}
            for i, p in enumerate(wbk.PLAN, start=1)]
    resources = [{"name": r[0], "url": r[1], "desc": r[2], "level": r[3]} for r in wbk.RESOURCES]
    core = {"threshold": wbk.MASTERY_THRESHOLD, "units": core_units, "final": final,
            "exercises": exercises, "plan": plan, "resources": resources,
            "stats": {"lessons": sum(u["count"] for u in core_units), "cards": total_cards,
                      "questions": total_q + len(final), "exercises": len(exercises)}}
    with open(os.path.join(OUT, "core.json"), "w", encoding="utf-8") as f:
        json.dump(core, f, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(OUT, "search.json"), "w", encoding="utf-8") as f:
        json.dump(search, f, ensure_ascii=False, separators=(",", ":"))

    # بصمة المحتوى: تُستخدم في عامل الخدمة لتحديث النسخة المخزنة عند تغيّر البيانات
    digest = hashlib.sha1()
    for name in sorted(os.listdir(OUT)):
        if name.endswith(".json"):
            digest.update(open(os.path.join(OUT, name), "rb").read())
    with open(os.path.join(OUT, "version.txt"), "w") as f:
        f.write(digest.hexdigest()[:10])

    stamp_service_worker()
    print(f"دروس {core['stats']['lessons']} | بطاقات {total_cards} | أسئلة {core['stats']['questions']} "
          f"| تمارين {len(exercises)} | نسخة {digest.hexdigest()[:10]}")
    # الأسئلة المفاهيمية العامة تُربط بمقدمة الوحدة (l = null) وهذا مقصود
    real_misses = [r for r in misses if "مفاهيمي" not in r and "ليست محجوزة" not in r]
    if real_misses:
        print("⚠ أسئلة لم تُربط بدرس:", real_misses)


if __name__ == "__main__":
    main()
