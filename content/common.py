# -*- coding: utf-8 -*-
"""
common.py — أدوات مشتركة لكتابة الدروس بالبنية ذات الـ 12 نقطة.

L(...) دالة مختصرة تُرجع قاموس الدرس بالحقول نفسها المستخدمة في lesson_keywords.py،
حتى تبقى ملفات الوحدات الكبيرة قصيرة ومقروءة. الترتيب يطابق النقاط الـ 12:
  real(1) what(2) name(3) why(4) goal(5) syntax(6) good(7)+good_out
  bad(8)+bad_err+bad_why  explain(9)+explain_ans  write(10)+write_ans
  fix(11)+fix_err+fix_ans+fix_why  bonus(12)
حقول اختيارية عبر **extra:
  explain_q   نص سؤال التفسير (الافتراضي «ماذا يطبع هذا الكود؟»)
  bad_out / fix_out   الناتج المتوقع للأخطاء المنطقية
  stdin       مدخلات تُمرَّر لبرنامج يستخدم input() أثناء التحقق
  good_cmp=False  لا تقارن ناتج المثال الصحيح حرفياً (ناتج يتغير من جهاز لآخر)
  bonus_code  كود مرافق للمعلومة الإضافية
"""
import textwrap

NOW = "تدرسها الآن"


def later(unit):
    return f"تعرّف عليها الآن، وتدرسها بعمق في {unit}"


def C(s):
    return textwrap.dedent(s).strip("\n")


def L(key, group, level, real, what, name, why, goal, syntax, good, good_out,
      bad, bad_err, bad_why, explain, explain_ans, write, write_ans,
      fix, fix_err, fix_ans, fix_why, bonus, **extra):
    d = dict(key=key, group=group, level=level, real=real, what=what, name=name, why=why,
             goal=goal, syntax=syntax, good=C(good), good_out=good_out, bad=C(bad),
             bad_err=bad_err, bad_why=bad_why, explain_q="ماذا يطبع هذا الكود؟",
             explain=C(explain), explain_ans=explain_ans, write=write, write_ans=C(write_ans),
             fix=C(fix), fix_err=fix_err, fix_ans=C(fix_ans), fix_why=fix_why, bonus=bonus)
    d.update(extra)
    return d


def reuse(lessons, key, group, unit_from, new_key=None):
    """إعادة استخدام درس كامل من وحدة أخرى (المحتوى نفسه، مجموعة جديدة، ومفتاح ربط جديد عند الحاجة)."""
    src = {k["key"]: k for k in lessons}[key]
    return dict(src, group=group, reused_from=unit_from, key=new_key or key)
