# -*- coding: utf-8 -*-
"""
lesson_keywords.py — نموذج الأسلوب التربوي الجديد للوحدة 01: الكلمات المحجوزة
==========================================================================
كل عنصر يتبع البنية الإلزامية ذات الـ 12 نقطة:
  1 🌍 real      مثال من أرض الواقع
  2 📖 what      ما هو؟
  3 ❓ name      لماذا سُمي بهذا الاسم؟
  4 🎯 why       ما أهميته؟
  5 🛠️ goal      ما الغاية منه؟
  6 💻 syntax    كيف يُكتب؟
  7 ✅ good      مثال صحيح          (+ good_out: الناتج المتوقع)
  8 ❌ bad       مثال خاطئ          (+ bad_err: الخطأ المتوقع، bad_why: الشرح)
  9 🔍 explain   تمرين تفسير        (+ explain_q: السؤال، explain_ans: الإجابة)
 10 ✏️ write     تمرين كتابة        (+ write_ans: حل نموذجي)
 11 🔧 fix       تمرين إيجاد خطأ    (+ fix_err، fix_ans: الكود المصحح، fix_why)
 12 💡 bonus     معلومة إضافية

حقول إضافية:
  level   متى يدرس الطالب الكلمة بعمق (لتخفيف العبء على المبتدئ)
  group   مجموعة الكلمة (لترتيب تربوي بدل الترتيب الأبجدي)

bad_err / fix_err:
  اسم الخطأ في بايثون (SyntaxError، NameError، ...) أو:
  "خطأ منطقي"      الكود يعمل لكن نتيجته خاطئة (أخطر أنواع الأخطاء على المبتدئ)
  "حلقة لا نهائية" لا يُشغَّل في التحقق الآلي
"""
import textwrap


def C(s):
    """تنظيف المسافة البادئة لكتل الكود."""
    return textwrap.dedent(s).strip("\n")


# ============================================================
# مقدمة الوحدة: مفهوم «الكلمات المحجوزة» نفسه
# ============================================================
UNIT_INTRO = dict(
    key="الكلمات المحجوزة (Reserved Keywords)",
    real="تخيّل أنك دخلت مطعماً، وعلى إحدى الطاولات ورقة مكتوب عليها «محجوز». لا يمكنك الجلوس عليها مهما كانت فارغة، لأنها لشخص آخر. في بايثون توجد كلمات «محجوزة» للغة نفسها، لا يمكنك أن تستخدمها أسماءً لمتغيراتك أو دوالك.",
    what="هي 35 كلمة لها معنى ثابت في بايثون، مثل if و for و def. تستخدمها لكتابة الأوامر، ولا يجوز أن تسمّي بها شيئاً.",
    name="سُمّيت «محجوزة» (Reserved) لأن بايثون حجزتها لنفسها لبناء الجمل البرمجية، تماماً كالطاولة المحجوزة: موجودة أمامك، لكنها ليست لك.",
    why="إذا سمّيت متغيراً باسم كلمة محجوزة سيظهر خطأ SyntaxError ولن يعمل البرنامج إطلاقاً. ومعرفة هذه الكلمات هي معرفة «أدوات» اللغة نفسها: كل جملة برمجية تكتبها لاحقاً مبنية عليها.",
    goal="تُخبر بايثون ماذا تريد أن تفعل: if تعني «اتخذ قراراً»، و for تعني «كرّر»، و def تعني «عرّف دالة». لو سمحت بايثون باستخدامها أسماءً لما استطاعت التمييز بين أمرك واسم متغيرك.",
    syntax=C("""
        # لا تُستخدم الكلمة المحجوزة اسماً… اختر اسماً بديلاً واضحاً
        condition = True      # بدلاً من: if = True
        class_name = "P1"     # بدلاً من: class = "P1"
    """),
    good=C("""
        age = 25
        name = "Ahmed"
        print(name, age)
    """),
    good_out="Ahmed 25",
    bad="if = 25",
    bad_err="SyntaxError",
    bad_why="if كلمة محجوزة تبدأ بها الجمل الشرطية، فلا يمكن أن تكون اسم متغير.",
    explain_q="ماذا يحدث عند تشغيل السطر التالي؟ ولماذا؟",
    explain="for = 10",
    explain_err="SyntaxError",
    explain_ans="يظهر SyntaxError ولا يعمل البرنامج، لأن for كلمة محجوزة لبدء الحلقات.",
    write="اكتب اسم متغير بديلاً عن كلمة class لتخزين اسم شعبة دراسية، وخزّن فيه \"Python 1\" ثم اطبعه.",
    write_ans=C("""
        class_name = "Python 1"
        print(class_name)
    """),
    fix='class = "Python"',
    fix_err="SyntaxError",
    fix_ans='course = "Python"',
    fix_why="class محجوزة لتعريف الأصناف؛ استبدلها باسم وصفي مثل course.",
    bonus="لمعرفة كل الكلمات المحجوزة في إصدار بايثون الذي لديك اكتب الكود التالي. وتذكّر: كل الكلمات المحجوزة بأحرف صغيرة ما عدا ثلاثاً تبدأ بحرف كبير: True و False و None.",
    bonus_code=C("""
        import keyword
        print(len(keyword.kwlist))
        print(keyword.kwlist)
    """),
)

# ============================================================
# المجموعات (ترتيب تربوي: من الأبسط إلى الأعمق)
# ============================================================
GROUPS = [
    ("values", "القيم الثابتة", "كلمات تمثّل قيماً جاهزة: نعم، لا، لا شيء."),
    ("logic", "عوامل المنطق والمقارنة", "كلمات تربط الشروط وتفحص العلاقات."),
    ("decisions", "اتخاذ القرار", "كلمات تجعل البرنامج يختار طريقه."),
    ("loops", "التكرار", "كلمات تكرّر العمل وتتحكم في التكرار."),
    ("functions", "الدوال والنطاق", "كلمات لبناء أوامرك الخاصة وتحديد مكان المتغيرات."),
    ("objects", "الأصناف والحذف", "كلمات لصناعة القوالب وحذف البيانات."),
    ("errors", "التعامل مع الأخطاء", "كلمات تحمي البرنامج من التوقف المفاجئ."),
    ("imports", "الاستيراد والموارد", "كلمات لجلب أدوات جاهزة وفتح الملفات بأمان."),
    ("async", "البرمجة غير المتزامنة", "كلمات متقدمة لإنجاز أكثر من مهمة دون انتظار."),
]

NOW = "تدرسها الآن"


def later(unit):
    """مستوى الكلمة: الوحدة التي تُدرَس فيها بعمق."""
    return f"تعرّف عليها الآن، وتدرسها بعمق في {unit}"


KEYWORDS_LESSON = [
    # ==================== القيم الثابتة ====================
    dict(
        key="True", group="values", level=NOW,
        real="مفتاح الإضاءة في غرفتك له حالتان فقط: مضاء أو مطفأ. True هي حالة «مضاء»: الجواب «نعم».",
        what="قيمة منطقية تعني «صحيح» أو «نعم».",
        name="True كلمة إنجليزية معناها «صحيح». وتبدأ بحرف كبير لأنها قيمة ثابتة صنعتها بايثون، لا متغير عادي.",
        why="كل قرار في البرنامج (هل المريض بالغ؟ هل التسلسل صالح؟) نتيجته True أو False. بدونها لا توجد شروط ولا قرارات.",
        goal="تمثيل الجواب «نعم» وتخزينه في متغير أو استخدامه في شرط.",
        syntax="is_adult = True",
        good=C("""
            age = 20
            is_adult = age >= 18
            print(is_adult)
        """), good_out="True",
        bad="is_valid = true", bad_err="NameError",
        bad_why="بايثون حساسة لحالة الأحرف: true بحرف صغير ليست True، فتعتبرها اسم متغير غير معرّف.",
        explain_q="ماذا يطبع هذا الكود؟ ولماذا؟", explain="print(5 > 3)",
        explain_ans="يطبع True لأن المقارنة 5 > 3 صحيحة، ونتيجة أي مقارنة قيمة منطقية.",
        write="أنشئ متغيراً اسمه has_fever قيمته True ثم اطبعه.",
        write_ans="has_fever = True\nprint(has_fever)",
        fix="is_registered = TRUE", fix_err="NameError",
        fix_ans="is_registered = True",
        fix_why="الصواب True: حرف أول كبير والبقية صغيرة.",
        bonus="True تساوي 1 في الحساب، لذلك يطبع الكود التالي 2. هذه الخاصية مفيدة لعدّ الحالات الصحيحة.",
        bonus_code="print(True + True)",
    ),
    dict(
        key="False", group="values", level=NOW,
        real="إشارة المرور الحمراء تقول للمشاة: «لا، لا تعبر الآن». False هي هذه الـ«لا».",
        what="قيمة منطقية تعني «خطأ» أو «لا».",
        name="False كلمة إنجليزية معناها «خاطئ»، وهي عكس True.",
        why="تحتاجها للتعبير عن حالة غير متحققة: المريض ليس مدخناً، الملف لم يُحفظ بعد.",
        goal="تمثيل الجواب «لا»، وغالباً تكون القيمة الابتدائية لمتغير يتغير لاحقاً.",
        syntax="is_smoker = False",
        good=C("""
            temperature = 36.8
            has_fever = temperature > 37.5
            print(has_fever)
        """), good_out="False",
        bad="False = 0", bad_err="SyntaxError",
        bad_why="لا يمكن تغيير قيمة False لأنها كلمة محجوزة ثابتة.",
        explain_q="ماذا يطبع هذا الكود؟", explain="print(bool(0))",
        explain_ans="يطبع False، لأن بايثون تعتبر الصفر قيمة «فارغة» تعادل False.",
        write="أنشئ متغيراً is_finished قيمته False، ثم غيّره إلى True واطبعه.",
        write_ans="is_finished = False\nis_finished = True\nprint(is_finished)",
        fix="done = false", fix_err="NameError", fix_ans="done = False",
        fix_why="false بحرف صغير ليست معرّفة؛ الصواب False.",
        bonus="القيم التي تعاملها بايثون كأنها False: الصفر 0، والنص الفارغ \"\"، والقائمة الفارغة []، والقاموس الفارغ {}، و None.",
        bonus_code='print(bool(""), bool([]), bool("ATG"))',
    ),
    dict(
        key="None", group="values", level=NOW,
        real="في ملف المريض خانة «نتيجة التحليل». قبل صدور النتيجة تكون الخانة موجودة لكنها فارغة. None هي هذه الخانة الفارغة.",
        what="قيمة خاصة تعني «لا شيء» أو «لا توجد قيمة بعد».",
        name="None كلمة إنجليزية معناها «لا شيء».",
        why="تميّز بين «لا توجد قيمة» وبين الصفر؛ فنتيجة تحليل تساوي 0 تختلف عن نتيجة لم تصدر أصلاً.",
        goal="قيمة ابتدائية لمتغير سيُملأ لاحقاً، وهي أيضاً ما ترجعه الدالة التي لا تحتوي return.",
        syntax="lab_result = None",
        good=C("""
            lab_result = None
            if lab_result is None:
                print("النتيجة لم تصدر بعد")
        """), good_out="النتيجة لم تصدر بعد",
        bad='None = "empty"', bad_err="SyntaxError",
        bad_why="None كلمة محجوزة ثابتة لا يمكن تغيير قيمتها.",
        explain_q="ماذا يطبع هذا الكود؟ (انتبه: هناك سطران)", explain='x = print("hi")\nprint(x)',
        explain_ans="يطبع hi ثم None، لأن الدالة print تطبع ولا ترجع قيمة، فيُخزَّن في x القيمة None.",
        write='أنشئ متغيراً diagnosis قيمته None، ثم اطبع "لا يوجد تشخيص" إذا كانت قيمته None.',
        write_ans='diagnosis = None\nif diagnosis is None:\n    print("لا يوجد تشخيص")',
        fix="result = none", fix_err="NameError", fix_ans="result = None",
        fix_why="none بحرف صغير ليست معرّفة؛ الصواب None.",
        bonus="للمقارنة مع None استخدم is وليس == (هذا ما توصي به PEP 8، دليل أسلوب كتابة بايثون).",
    ),
    # ==================== المنطق والمقارنة ====================
    dict(
        key="and", group="logic", level=NOW,
        real="لكي تسافر تحتاج جواز سفر «و» تذكرة طيران. إذا نقص أحدهما فلن تسافر.",
        what="تربط شرطين، والنتيجة True فقط إذا تحقق الشرطان معاً.",
        name="and كلمة إنجليزية معناها «و».",
        why="القرارات الحقيقية مركّبة غالباً: يكون BMI طبيعياً إذا كان أكبر من أو يساوي 18.5 «و» أقل من 25.",
        goal="دمج عدة شروط في شرط واحد يجب أن تتحقق كلها.",
        syntax="الشرط_الأول and الشرط_الثاني",
        good=C("""
            bmi = 22
            print(bmi >= 18.5 and bmi < 25)
        """), good_out="True",
        bad="age = 30\nprint(age > 18 and < 60)", bad_err="SyntaxError",
        bad_why="كل طرف من and يجب أن يكون شرطاً كاملاً؛ الطرف الثاني ينقصه المتغير: age < 60.",
        explain_q="ماذا يطبع هذا الكود؟", explain="print(True and False)",
        explain_ans="يطبع False، لأن and تحتاج أن يكون الطرفان True.",
        write="لديك age = 30. اطبع True إذا كان العمر بين 18 و 60 (شاملاً الحدّين) باستخدام and.",
        write_ans="age = 30\nprint(age >= 18 and age <= 60)",
        fix="x = 5\nprint(x > 1 and < 10)", fix_err="SyntaxError",
        fix_ans="x = 5\nprint(x > 1 and x < 10)",
        fix_why="أعِد كتابة المتغير في الطرف الثاني: x < 10.",
        bonus="تسمح بايثون بكتابة المقارنة المتسلسلة بدل and، وهي أقرب للرياضيات: 18 <= age <= 60.",
        bonus_code="age = 30\nprint(18 <= age <= 60)",
    ),
    dict(
        key="or", group="logic", level=NOW,
        real="يُسمح بدخول قاعة المحاضرات لمن كان طالباً «أو» مدرساً. يكفي أن تكون أحدهما.",
        what="تربط شرطين، والنتيجة True إذا تحقق شرط واحد على الأقل.",
        name="or كلمة إنجليزية معناها «أو».",
        why="لقبول أكثر من احتمال: القاعدة G «أو» C تُحسب ضمن نسبة GC.",
        goal="دمج شروط يكفي تحقق أحدها.",
        syntax="الشرط_الأول or الشرط_الثاني",
        good=C("""
            base = "G"
            print(base == "G" or base == "C")
        """), good_out="True",
        bad=C("""
            base = "A"
            if base == "G" or "C":
                print("قاعدة GC")
        """), bad_err="خطأ منطقي",
        bad_why="الكود يعمل لكنه يطبع «قاعدة GC» مع أن القاعدة A! السبب أن \"C\" وحدها نص غير فارغ فتُعتبر True دائماً. الصواب: base == \"G\" or base == \"C\".",
        bad_out="قاعدة GC",
        explain_q="ماذا يطبع هذا الكود؟", explain="print(False or False)",
        explain_ans="يطبع False، لأن or تحتاج طرفاً واحداً True على الأقل، وكلاهما False.",
        write='لديك blood = "O-". اطبع True إذا كانت الفصيلة "O-" أو "AB+".',
        write_ans='blood = "O-"\nprint(blood == "O-" or blood == "AB+")',
        fix="x = 15\nprint(x > 10 or)", fix_err="SyntaxError",
        fix_ans="x = 15\nprint(x > 10 or x < 0)",
        fix_why="or تحتاج شرطاً بعدها؛ لا يمكن أن تنتهي الجملة عندها.",
        bonus="or تتوقف عند أول طرف صحيح ولا تفحص البقية (التقييم المختصر Short-circuit)، وهذا يسرّع البرنامج.",
    ),
    dict(
        key="not", group="logic", level=NOW,
        real="لافتة «ليس مغلقاً» على باب المحل تعني أنه مفتوح. not تقلب الحالة إلى عكسها.",
        what="تعكس القيمة المنطقية: True تصبح False، و False تصبح True.",
        name="not كلمة إنجليزية معناها «ليس» أو «لا».",
        why="تجعل الشروط المنفية سهلة القراءة: «إذا لم يكن التسلسل فارغاً».",
        goal="نفي شرط أو قيمة.",
        syntax="not شرط",
        good=C("""
            seq = ""
            if not seq:
                print("التسلسل فارغ")
        """), good_out="التسلسل فارغ",
        bad="print(!True)", bad_err="SyntaxError",
        bad_why="بعض اللغات تستخدم ! للنفي، أما بايثون فتستخدم الكلمة not.",
        explain_q="ماذا يطبع هذا الكود؟", explain="print(not 0)",
        explain_ans="يطبع True، لأن 0 تُعامل كـ False، ونفيها True.",
        write='لديك is_closed = False. اطبع "مفتوح" إذا لم يكن المحل مغلقاً.',
        write_ans='is_closed = False\nif not is_closed:\n    print("مفتوح")',
        fix='is_valid = False\nif !is_valid:\n    print("غير صالح")', fix_err="SyntaxError",
        fix_ans='is_valid = False\nif not is_valid:\n    print("غير صالح")',
        fix_why="استبدل ! بالكلمة not.",
        bonus="هناك عاملان مركّبان يستخدمان not: «not in» (ليس موجوداً في) و «is not» (ليس هو نفسه).",
        bonus_code='print("U" not in "ATGC")',
    ),
    dict(
        key="in", group="logic", level=NOW,
        real="تفتح لوحة النتائج وتبحث: هل اسمي موجود «في» قائمة الناجحين؟",
        what="تفحص هل عنصر موجود داخل مجموعة أو نص، والنتيجة True أو False.",
        name="in كلمة إنجليزية معناها «في» أو «داخل».",
        why="البحث من أكثر العمليات شيوعاً: هل يحتوي التسلسل على كودون البداية ATG؟",
        goal="فحص العضوية، وتُستخدم أيضاً في حلقة for للمرور على العناصر.",
        syntax="عنصر in مجموعة",
        good=C("""
            seq = "CCATGAA"
            print("ATG" in seq)
        """), good_out="True",
        bad='print("ATG" in 12345)', bad_err="TypeError",
        bad_why="لا يمكن البحث داخل رقم؛ in تعمل على النصوص والقوائم والقواميس والمجموعات.",
        explain_q="ماذا يطبع هذا الكود؟", explain='print("U" in "ATGC")',
        explain_ans="يطبع False، لأن الحرف U غير موجود في النص ATGC (فـ U موجود في RNA لا في DNA).",
        write='لديك patients = ["Sara", "Ali"]. اطبع True إذا كان "Ali" موجوداً في القائمة.',
        write_ans='patients = ["Sara", "Ali"]\nprint("Ali" in patients)',
        fix='if "A" in ["A", "T"]\n    print("موجود")', fix_err="SyntaxError",
        fix_ans='if "A" in ["A", "T"]:\n    print("موجود")',
        fix_why="جملة if يجب أن تنتهي بنقطتين رأسيتين (:).",
        bonus="البحث بـ in داخل set أو dict أسرع بكثير من البحث داخل list عندما تكون البيانات كبيرة.",
    ),
    dict(
        key="is", group="logic", level=NOW,
        real="توأمان متطابقان في الشكل (==)، لكن كل واحد منهما ليس «هو» الآخر (is).",
        what="تفحص هل المتغيران يشيران إلى الشيء نفسه في الذاكرة، لا هل قيمتاهما متساويتان فقط.",
        name="is كلمة إنجليزية معناها «هو».",
        why="هي الطريقة الصحيحة للمقارنة مع None، وتساعدك على فهم أن متغيرين قد يشيران إلى القائمة نفسها.",
        goal="فحص الهوية (نفس الكائن)، وأشهر استخدام لها: x is None.",
        syntax="أ is ب",
        good=C("""
            a = [1, 2]
            b = a
            c = [1, 2]
            print(a is b, a is c)
        """), good_out="True False",
        bad="is = 5", bad_err="SyntaxError",
        bad_why="is كلمة محجوزة لا تصلح اسماً لمتغير.",
        explain_q="ماذا يطبع هذا الكود؟", explain="x = None\nprint(x is None)",
        explain_ans="يطبع True لأن x يشير إلى None نفسها.",
        write='لديك result = None. اطبع "لا توجد قيمة" إذا كان result هو None.',
        write_ans='result = None\nif result is None:\n    print("لا توجد قيمة")',
        fix="result = 5\nif result not is None:\n    print(result)", fix_err="SyntaxError",
        fix_ans="result = 5\nif result is not None:\n    print(result)",
        fix_why="الترتيب الصحيح هو is not وليس not is.",
        bonus="القاعدة العملية: استخدم == لمقارنة القيم، واستخدم is للمقارنة مع None فقط تقريباً.",
    ),
    # ==================== اتخاذ القرار ====================
    dict(
        key="if", group="decisions", level=later("الوحدة 06 (هياكل التحكم)"),
        real="«إذا» كان الجو ممطراً، خذ مظلة. أنت تفحص الشرط أولاً، ثم تتصرف.",
        what="تنفّذ مجموعة أوامر فقط عندما يكون الشرط صحيحاً.",
        name="if كلمة إنجليزية معناها «إذا».",
        why="بدونها يسير البرنامج في خط واحد ولا يستطيع اتخاذ أي قرار.",
        goal="جعل البرنامج يختار ماذا يفعل حسب البيانات: حرارة المريض مرتفعة؟ أعطِ تنبيهاً.",
        syntax="if شرط:\n    أوامر (مزاحة 4 مسافات)",
        good=C("""
            temp = 38.5
            if temp > 37.5:
                print("لدى المريض حمى")
        """), good_out="لدى المريض حمى",
        bad='age = 20\nif age = 18:\n    print("عمره 18")', bad_err="SyntaxError",
        bad_why="العلامة = للتخزين، أما للمقارنة فنستخدم ==.",
        explain_q="ماذا يطبع هذا الكود؟", explain='x = 3\nif x > 5:\n    print("كبير")\nprint("انتهى")',
        explain_ans="يطبع «انتهى» فقط، لأن الشرط 3 > 5 خاطئ فلا يُنفذ السطر المزاح، أما السطر الأخير فليس داخل if.",
        write='لديك age = 21. اطبع "بالغ" إذا كان العمر 18 أو أكثر.',
        write_ans='age = 21\nif age >= 18:\n    print("بالغ")',
        fix='age = 25\nif age > 18\nprint("بالغ")', fix_err="SyntaxError",
        fix_ans='age = 25\nif age > 18:\n    print("بالغ")',
        fix_why="خطآن: تنقص النقطتان الرأسيتان بعد الشرط، والسطر التالي يجب أن يُزاح 4 مسافات.",
        bonus="أي قيمة يمكن أن تكون شرطاً: القائمة الفارغة تُعامل False، والقائمة التي فيها عناصر تُعامل True.",
    ),
    dict(
        key="elif", group="decisions", level=later("الوحدة 06 (هياكل التحكم)"),
        real="إشارة المرور: إذا كانت حمراء فقف، «وإلا إذا» كانت صفراء فاستعد، وإلا فانطلق.",
        what="شرط إضافي يُفحص فقط إذا لم تتحقق الشروط التي قبله.",
        name="elif اختصار للعبارة الإنجليزية else if، ومعناها «وإلا إذا».",
        why="لتصنيف شيء إلى أكثر من فئتين: نحافة، طبيعي، زيادة وزن، سمنة.",
        goal="بناء سلسلة اختيارات مرتبة يُنفذ منها خيار واحد فقط.",
        syntax="if الشرط_الأول:\n    ...\nelif الشرط_الثاني:\n    ...",
        good=C("""
            bmi = 27
            if bmi < 18.5:
                print("نحافة")
            elif bmi < 25:
                print("طبيعي")
            elif bmi < 30:
                print("زيادة وزن")
        """), good_out="زيادة وزن",
        bad='x = 7\nelif x > 5:\n    print("كبير")', bad_err="SyntaxError",
        bad_why="لا يمكن أن تبدأ بـ elif؛ يجب أن تسبقها if.",
        explain_q="ماذا يطبع هذا الكود؟",
        explain=C("""
            score = 85
            if score >= 90:
                print("A")
            elif score >= 80:
                print("B")
            elif score >= 70:
                print("C")
        """),
        explain_ans="يطبع B فقط. الشرط الأول خاطئ، والثاني صحيح فيُنفذ ثم تتوقف السلسلة، فلا يُفحص الثالث رغم أنه صحيح أيضاً.",
        write="لديك temp = 36.9. اطبع «منخفضة» إذا كانت أقل من 36، و«طبيعية» إذا كانت حتى 37.5، و«حمى» في غير ذلك.",
        write_ans='temp = 36.9\nif temp < 36:\n    print("منخفضة")\nelif temp <= 37.5:\n    print("طبيعية")\nelse:\n    print("حمى")',
        fix='x = 5\nif x > 10:\n    print("كبير")\nelse if x > 3:\n    print("متوسط")', fix_err="SyntaxError",
        fix_ans='x = 5\nif x > 10:\n    print("كبير")\nelif x > 3:\n    print("متوسط")',
        fix_why="بايثون لا تعرف else if منفصلتين؛ الصواب elif.",
        bonus="بما أن بايثون تتوقف عند أول شرط صحيح، رتّب الشروط بحيث يأتي الأضيق أولاً.",
    ),
    dict(
        key="else", group="decisions", level=later("الوحدة 06 (هياكل التحكم)"),
        real="إذا كان في السيارة وقود فانطلق، «وإلا» فاذهب إلى محطة الوقود أولاً.",
        what="مجموعة أوامر تُنفذ عندما لا يتحقق أي شرط قبلها.",
        name="else كلمة إنجليزية معناها «وإلا».",
        why="تضمن أن البرنامج يعرف ماذا يفعل في كل الحالات، فلا تبقى حالة بلا تصرف.",
        goal="المسار الافتراضي البديل.",
        syntax="if شرط:\n    ...\nelse:\n    ...",
        good=C("""
            age = 15
            if age >= 18:
                print("بالغ")
            else:
                print("قاصر")
        """), good_out="قاصر",
        bad='age = 15\nif age >= 18:\n    print("بالغ")\nelse age < 18:\n    print("قاصر")', bad_err="SyntaxError",
        bad_why="else لا تأخذ شرطاً أبداً؛ هي «كل ما تبقّى».",
        explain_q="ماذا يطبع هذا الكود؟", explain='x = 10\nif x % 2 == 0:\n    print("زوجي")\nelse:\n    print("فردي")',
        explain_ans="يطبع «زوجي» لأن باقي قسمة 10 على 2 يساوي 0.",
        write='لديك mark = 45. اطبع "ناجح" إذا كانت العلامة 50 أو أكثر، وإلا "راسب".',
        write_ans='mark = 45\nif mark >= 50:\n    print("ناجح")\nelse:\n    print("راسب")',
        fix='mark = 70\nif mark >= 50:\n    print("ناجح")\nelse\n    print("راسب")', fix_err="SyntaxError",
        fix_ans='mark = 70\nif mark >= 50:\n    print("ناجح")\nelse:\n    print("راسب")',
        fix_why="else تحتاج نقطتين رأسيتين (:) بعدها.",
        bonus="else لا تُستخدم مع if فقط: تعمل أيضاً مع for و while و try، وستراها في وحدات لاحقة.",
    ),
    # ==================== التكرار ====================
    dict(
        key="for", group="loops", level=later("الوحدة 06 (هياكل التحكم)"),
        real="عندما تقرأ كتاباً تقلّب الصفحات واحدة واحدة: «لكل» صفحة تفعل الشيء نفسه، وهو القراءة.",
        what="حلقة تكرر مجموعة أوامر مرة لكل عنصر في مجموعة.",
        name="for كلمة إنجليزية معناها «لكل».",
        why="تغنيك عن كتابة السطر نفسه مئات المرات؛ تسلسل DNA قد يحتوي ملايين القواعد.",
        goal="المرور على عناصر قائمة أو نص أو مدى أرقام ومعالجة كل عنصر.",
        syntax="for عنصر in مجموعة:\n    أوامر",
        good=C("""
            for base in "ATG":
                print(base)
        """), good_out="A\nT\nG",
        bad="for i in 5:\n    print(i)", bad_err="TypeError",
        bad_why="لا يمكن المرور على رقم واحد. إن أردت التكرار 5 مرات فاستخدم range(5).",
        explain_q="ماذا يطبع هذا الكود؟", explain="total = 0\nfor n in [1, 2, 3]:\n    total = total + n\nprint(total)",
        explain_ans="يطبع 6: الحلقة تجمع 1 ثم 2 ثم 3، والطباعة خارج الحلقة فتحدث مرة واحدة.",
        write='اطبع كل اسم في القائمة ["Ali", "Sara", "Omar"] في سطر منفصل.',
        write_ans='for name in ["Ali", "Sara", "Omar"]:\n    print(name)',
        fix="for i in range(3)\n    print(i)", fix_err="SyntaxError",
        fix_ans="for i in range(3):\n    print(i)",
        fix_why="سطر for يجب أن ينتهي بنقطتين رأسيتين.",
        bonus="range(5) تعطي الأرقام 0 و 1 و 2 و 3 و 4. الرقم 5 نفسه غير مشمول، لأن العدّ يبدأ من الصفر.",
        bonus_code="print(list(range(5)))",
    ),
    dict(
        key="while", group="loops", level=later("الوحدة 06 (هياكل التحكم)"),
        real="«طالما» الكوب غير ممتلئ، استمر في صبّ الماء. أنت لا تعرف مسبقاً كم ثانية ستحتاج.",
        what="حلقة تتكرر ما دام الشرط صحيحاً، وتتوقف عندما يصبح خاطئاً.",
        name="while كلمة إنجليزية معناها «طالما» أو «أثناء».",
        why="تُستخدم عندما لا تعرف عدد التكرارات مسبقاً، مثل الاستمرار في طلب كلمة مرور حتى تكون صحيحة.",
        goal="التكرار المشروط حتى تحقق هدف معين.",
        syntax="while شرط:\n    أوامر",
        good=C("""
            dose = 100
            while dose > 25:
                dose = dose / 2
            print(dose)
        """), good_out="25.0",
        bad='i = 0\nwhile i < 3:\n    print(i)', bad_err="حلقة لا نهائية",
        bad_why="لا يتغير i أبداً، فيبقى الشرط صحيحاً إلى الأبد ويطبع البرنامج 0 بلا توقف. الحل: أضف i += 1 داخل الحلقة.",
        explain_q="ماذا يطبع هذا الكود؟", explain="n = 3\nwhile n > 0:\n    print(n)\n    n = n - 1",
        explain_ans="يطبع 3 ثم 2 ثم 1، كل رقم في سطر. عندما يصبح n صفراً يصير الشرط خاطئاً فتتوقف الحلقة.",
        write="اطبع الأعداد من 1 إلى 5 باستخدام while.",
        write_ans="i = 1\nwhile i <= 5:\n    print(i)\n    i += 1",
        fix="count = 1\nwhile count <= 3:\nprint(count)\n    count += 1", fix_err="IndentationError",
        fix_ans="count = 1\nwhile count <= 3:\n    print(count)\n    count += 1",
        fix_why="كل أوامر الحلقة يجب أن تكون مزاحة بالمقدار نفسه (4 مسافات).",
        bonus="إذا علقت في حلقة لا نهائية اضغط Ctrl + C في الطرفية لإيقاف البرنامج.",
    ),
    dict(
        key="break", group="loops", level=later("الوحدة 06 (هياكل التحكم)"),
        real="تبحث عن مفاتيحك في الأدراج واحداً تلو الآخر. وجدتها في الدرج الثاني؟ «تتوقف» فوراً ولا تفتح البقية.",
        what="توقف الحلقة فوراً وتخرج منها.",
        name="break كلمة إنجليزية معناها «اكسر»؛ أي اكسر الحلقة.",
        why="توفّر الوقت عندما تجد ما تبحث عنه، مثل التوقف عند أول كودون توقف في التسلسل.",
        goal="إنهاء الحلقة مبكراً عند تحقق هدف.",
        syntax="for ...:\n    if شرط:\n        break",
        good=C("""
            for codon in ["ATG", "CCA", "TAA", "GGC"]:
                if codon == "TAA":
                    print("كودون توقف")
                    break
                print(codon)
        """), good_out="ATG\nCCA\nكودون توقف",
        bad="x = 5\nif x > 3:\n    break", bad_err="SyntaxError",
        bad_why="break تعمل داخل الحلقات فقط (for أو while)، وليس داخل if وحدها.",
        explain_q="ماذا يطبع هذا الكود؟", explain="for i in range(10):\n    if i == 3:\n        break\n    print(i)",
        explain_ans="يطبع 0 و 1 و 2 فقط؛ عندما يصل i إلى 3 تتوقف الحلقة قبل الطباعة.",
        write="في القائمة ages = [34, 72, 61] اطبع أول عمر أكبر من 60 ثم أوقف الحلقة.",
        write_ans="ages = [34, 72, 61]\nfor a in ages:\n    if a > 60:\n        print(a)\n        break",
        fix="for n in [1, 2, 3]:\n    if n == 2:\n    break", fix_err="IndentationError",
        fix_ans="for n in [1, 2, 3]:\n    if n == 2:\n        break",
        fix_why="break داخل if فيجب أن تُزاح أكثر من if بأربع مسافات.",
        bonus="break تُخرجك من أقرب حلقة فقط. في الحلقات المتداخلة تبقى الحلقة الخارجية تعمل.",
    ),
    dict(
        key="continue", group="loops", level=later("الوحدة 06 (هياكل التحكم)"),
        real="أثناء تصحيح أوراق الامتحان وجدت ورقة فارغة، فتتخطّاها وتتابع تصحيح الباقي.",
        what="تتخطى بقية الدورة الحالية وتنتقل مباشرة إلى الدورة التالية.",
        name="continue كلمة إنجليزية معناها «تابِع» أو «استمر».",
        why="لتجاهل البيانات غير الصالحة دون إيقاف المعالجة كلها، مثل تخطي القاعدة المجهولة N.",
        goal="تخطي عناصر معينة داخل الحلقة.",
        syntax="for ...:\n    if شرط:\n        continue",
        good=C("""
            for base in "ATNG":
                if base == "N":
                    continue
                print(base)
        """), good_out="A\nT\nG",
        bad="def check():\n    continue", bad_err="SyntaxError",
        bad_why="continue تعمل داخل الحلقات فقط.",
        explain_q="ماذا يطبع هذا الكود؟", explain="for i in range(5):\n    if i % 2 == 0:\n        continue\n    print(i)",
        explain_ans="يطبع 1 و 3: الأعداد الزوجية 0 و 2 و 4 تُتخطّى.",
        write="اطبع الأعداد الموجبة فقط من القائمة [3, -1, 4, -5] باستخدام continue.",
        write_ans="for n in [3, -1, 4, -5]:\n    if n < 0:\n        continue\n    print(n)",
        fix='for b in "AN":\n    if b == "N":\n        continue\n        print(b)', fix_err="خطأ منطقي",
        fix_out="",
        fix_ans='for b in "AN":\n    if b == "N":\n        continue\n    print(b)',
        fix_why="الكود لا يطبع شيئاً! print موضوعة داخل if بعد continue فلا تُنفذ أبداً. أزحها لتكون داخل الحلقة خارج if.",
        bonus="الفرق باختصار: break توقف الحلقة كلها، و continue تتخطى دورة واحدة فقط.",
    ),
    dict(
        key="pass", group="loops", level=later("الوحدة 06 (هياكل التحكم)"),
        real="تضع ورقة «محجوز» على مقعد في القاعة حتى يأتي صديقك. الورقة لا تفعل شيئاً، لكنها تحفظ المكان.",
        what="أمر لا يفعل شيئاً، يوضع حيث تتطلب بايثون وجود كود.",
        name="pass كلمة إنجليزية معناها «مرِّر» أو «تجاوز».",
        why="بايثون لا تقبل كتلة فارغة بعد النقطتين؛ pass تمنع الخطأ وأنت ما زلت تبني البرنامج.",
        goal="حجز مكان لكود ستكتبه لاحقاً.",
        syntax="def اسم():\n    pass",
        good=C("""
            def analyze_dna():
                pass  # سنكتبها لاحقاً

            print("البرنامج يعمل")
        """), good_out="البرنامج يعمل",
        bad='def analyze():\n\nprint("x")', bad_err="IndentationError",
        bad_why="الدالة بلا أي سطر داخلها، وبايثون تنتظر كتلة مزاحة.",
        explain_q="ماذا يطبع هذا الكود؟", explain='for i in range(3):\n    pass\nprint("تم")',
        explain_ans="يطبع «تم» مرة واحدة فقط؛ الحلقة تدور 3 مرات دون أن تفعل شيئاً.",
        write="اكتب دالة فارغة اسمها calculate_bmi ستكملها لاحقاً.",
        write_ans="def calculate_bmi():\n    pass",
        fix='age = 20\nif age > 18:\nelse:\n    print("قاصر")', fix_err="IndentationError",
        fix_ans='age = 20\nif age > 18:\n    pass\nelse:\n    print("قاصر")',
        fix_why="كتلة if فارغة؛ ضع pass داخلها (أو اكتب الأمر المطلوب).",
        bonus="يمكن استخدام ثلاث نقاط ... بالغرض نفسه، وستراها كثيراً في التوثيق الرسمي.",
    ),
    # ==================== الدوال والنطاق ====================
    dict(
        key="def", group="functions", level=later("الوحدة 09 (الدوال)"),
        real="وصفة الطبخ تكتبها مرة واحدة في دفترك، ثم تستخدمها كلما أردت إعداد الطبق دون أن تعيد كتابتها.",
        what="تعرّف دالة: مجموعة أوامر لها اسم تستدعيها متى شئت.",
        name="def اختصار للكلمة الإنجليزية define، ومعناها «عرِّف».",
        why="الدوال تمنع تكرار الكود وتقسّم البرنامج الكبير إلى أجزاء صغيرة مفهومة.",
        goal="إنشاء أوامر خاصة بك مثل calculate_bmi أو gc_content.",
        syntax="def اسم_الدالة(المعاملات):\n    أوامر",
        good=C("""
            def greet(name):
                print("مرحباً", name)

            greet("Sara")
        """), good_out="مرحباً Sara",
        bad='def greet:\n    print("hi")', bad_err="SyntaxError",
        bad_why="الأقواس () إلزامية بعد اسم الدالة حتى لو لم يكن لها معاملات.",
        explain_q="ماذا يطبع هذا الكود؟", explain="def double(x):\n    return x * 2\n\nprint(double(4))",
        explain_ans="يطبع 8؛ الدالة تضرب المدخل في 2 وترجع الناتج.",
        write="اكتب دالة square(n) ترجع مربع العدد، ثم اطبع square(5).",
        write_ans="def square(n):\n    return n * n\n\nprint(square(5))",
        fix="def add(a, b)\n    return a + b", fix_err="SyntaxError",
        fix_ans="def add(a, b):\n    return a + b",
        fix_why="سطر def يجب أن ينتهي بنقطتين رأسيتين.",
        bonus="تعريف الدالة لا يشغّلها! الدالة تعمل فقط عندما تستدعيها باسمها متبوعاً بالأقواس.",
    ),
    dict(
        key="return", group="functions", level=later("الوحدة 09 (الدوال)"),
        real="آلة القهوة: تعطيها المال والبن، «فتُرجع» لك كوب القهوة لتأخذه وتشربه.",
        what="ترجع نتيجة من الدالة إلى المكان الذي استدعاها، وتنهي الدالة فوراً.",
        name="return كلمة إنجليزية معناها «أرجِع».",
        why="بدونها لا يمكنك استخدام نتيجة الدالة في حسابات أخرى؛ الطباعة وحدها تعرض النتيجة ولا تسلّمها.",
        goal="تسليم ناتج الدالة لاستخدامه لاحقاً.",
        syntax="def f():\n    return قيمة",
        good=C("""
            def bmi(weight, height):
                return weight / height ** 2

            print(round(bmi(70, 1.75), 1))
        """), good_out="22.9",
        bad="return 5", bad_err="SyntaxError",
        bad_why="return تعمل داخل الدوال فقط.",
        explain_q="ماذا يطبع هذا الكود؟", explain='def f():\n    return 1\n    print("hi")\n\nprint(f())',
        explain_ans="يطبع 1 فقط؛ السطر بعد return لا يُنفذ أبداً لأن return تنهي الدالة.",
        write="اكتب دالة is_adult(age) ترجع True إذا كان العمر 18 أو أكثر، ثم اطبع is_adult(20).",
        write_ans="def is_adult(age):\n    return age >= 18\n\nprint(is_adult(20))",
        fix="def total(a, b):\n    a + b\n\nprint(total(2, 3))", fix_err="خطأ منطقي",
        fix_out="None",
        fix_ans="def total(a, b):\n    return a + b\n\nprint(total(2, 3))",
        fix_why="الكود يطبع None بدل 5 لأن الدالة تحسب المجموع ولا ترجعه. أضف return.",
        bonus="يمكن أن ترجع الدالة أكثر من قيمة مفصولة بفاصلة: return low, high.",
    ),
    dict(
        key="lambda", group="functions", level=later("الوحدة 09 (الدوال)"),
        real="بدلاً من فتح دفتر كامل، تكتب ملاحظة سريعة على ورقة لاصقة وتستخدمها مرة واحدة.",
        what="دالة قصيرة بلا اسم تُكتب في سطر واحد.",
        name="الاسم مأخوذ من الحرف اليوناني λ (لامدا) المستخدم في فرع من الرياضيات اسمه «حساب لامدا».",
        why="مفيدة جداً مع sorted و map و filter عندما تحتاج دالة صغيرة لمرة واحدة.",
        goal="كتابة دالة بسيطة في المكان الذي تحتاجها فيه مباشرة.",
        syntax="lambda المعاملات: تعبير",
        good=C("""
            square = lambda x: x ** 2
            print(square(4))
        """), good_out="16",
        bad="double = lambda x: return x * 2", bad_err="SyntaxError",
        bad_why="lambda ترجع التعبير تلقائياً، ولا تُكتب داخلها كلمة return.",
        explain_q="ماذا يطبع هذا الكود؟", explain="ages = [52, 18, 33]\nprint(sorted(ages, key=lambda a: -a))",
        explain_ans="يطبع [52, 33, 18]: الترتيب حسب سالب العمر يعني ترتيباً تنازلياً.",
        write="اكتب lambda اسمها half ترجع نصف العدد، ثم اطبع half(10).",
        write_ans="half = lambda x: x / 2\nprint(half(10))",
        fix="add = lambda a, b -> a + b", fix_err="SyntaxError",
        fix_ans="add = lambda a, b: a + b",
        fix_why="بعد معاملات lambda تأتي نقطتان رأسيتان (:) وليس سهماً.",
        bonus="إذا احتاجت الدالة أكثر من تعبير واحد فاستخدم def؛ lambda للأشياء القصيرة فقط.",
    ),
    dict(
        key="yield", group="functions", level=later("الوحدة 09 (الدوال) – مستوى البرمجة 2"),
        real="آلة التذاكر في البنك تعطيك تذكرة واحدة كلما ضغطت الزر، ولا تطبع كل التذاكر دفعة واحدة.",
        what="تجعل الدالة «مولّداً» يُنتج القيم واحدة تلو الأخرى عند الطلب.",
        name="yield كلمة إنجليزية معناها «يُنتِج» أو «يُعطي».",
        why="توفّر الذاكرة عند التعامل مع بيانات ضخمة، مثل ملف FASTA بحجم عدة غيغابايتات.",
        goal="إنتاج سلسلة قيم تدريجياً بدل تخزينها كلها في قائمة.",
        syntax="def f():\n    yield قيمة",
        good=C("""
            def countdown(n):
                while n > 0:
                    yield n
                    n -= 1

            print(list(countdown(3)))
        """), good_out="[3, 2, 1]",
        bad="yield 5", bad_err="SyntaxError",
        bad_why="yield تعمل داخل الدوال فقط.",
        explain_q="ماذا يطبع هذا الكود؟", explain='def bases():\n    yield "A"\n    yield "T"\n\nfor b in bases():\n    print(b)',
        explain_ans="يطبع A ثم T؛ كل دورة تطلب من المولد القيمة التالية.",
        write="اكتب مولداً evens(n) ينتج الأعداد الزوجية من 0 حتى n، ثم اطبعها كقائمة لـ n = 6.",
        write_ans="def evens(n):\n    for i in range(0, n + 1, 2):\n        yield i\n\nprint(list(evens(6)))",
        fix="def gen():\n    yield = 1", fix_err="SyntaxError",
        fix_ans="def gen():\n    yield 1",
        fix_why="yield ليست متغيراً يُخزَّن فيه؛ تكتب القيمة بعدها مباشرة.",
        bonus="المولّد «يتذكر» مكانه: عند طلب القيمة التالية يكمل من السطر الذي توقف عنده.",
    ),
    dict(
        key="global", group="functions", level=later("الوحدة 09 (الدوال)"),
        real="سبورة الصف يراها الجميع. إذا أردت تعديل ما عليها من مقعدك فعليك أن تعلن: «سأكتب على السبورة لا في دفتري».",
        what="تسمح للدالة بتعديل متغير عام معرّف خارجها.",
        name="global كلمة إنجليزية معناها «عام» أو «عالمي».",
        why="بدونها تعتبر الدالة المتغير محلياً خاصاً بها، فلا يتغير المتغير الأصلي، أو يظهر خطأ.",
        goal="تعديل متغير مشترك بين أجزاء البرنامج من داخل دالة.",
        syntax="def f():\n    global اسم_المتغير",
        good=C("""
            count = 0

            def add_patient():
                global count
                count += 1

            add_patient()
            print(count)
        """), good_out="1",
        bad="count = 0\n\ndef add():\n    count += 1\n\nadd()", bad_err="UnboundLocalError",
        bad_why="الدالة تحاول تعديل count دون التصريح بأنه عام، فتعتبره متغيراً محلياً لم تُعطَ له قيمة بعد.",
        explain_q="ماذا يطبع هذا الكود؟", explain="x = 5\n\ndef f():\n    x = 10\n\nf()\nprint(x)",
        explain_ans="يطبع 5؛ الدالة أنشأت x محلياً خاصاً بها ولم تغيّر x العام.",
        write="لديك total = 0. اكتب دالة add_five تضيف 5 إلى total العام، ثم استدعها واطبع total.",
        write_ans="total = 0\n\ndef add_five():\n    global total\n    total += 5\n\nadd_five()\nprint(total)",
        fix="visits = 0\n\ndef new_visit():\n    visits += 1\n\nnew_visit()", fix_err="UnboundLocalError",
        fix_ans="visits = 0\n\ndef new_visit():\n    global visits\n    visits += 1\n\nnew_visit()",
        fix_why="صرّح بأن visits متغير عام داخل الدالة.",
        bonus="المبرمجون المحترفون يقللون استخدام global؛ الأوضح غالباً أن ترجع الدالة القيمة الجديدة.",
    ),
    dict(
        key="nonlocal", group="functions", level=later("الوحدة 09 (الدوال) – مستوى البرمجة 2"),
        real="أنت في غرفة داخل شقة، وتريد تعديل شيء في صالة الشقة (المستوى الأعلى مباشرة)، لا في مدخل العمارة كلها.",
        what="تسمح لدالة داخلية بتعديل متغير يخص الدالة الخارجية التي تحتويها.",
        name="nonlocal معناها «غير محلي»: المتغير ليس محلياً في الدالة الداخلية، وليس عاماً للبرنامج كله.",
        why="ضرورية عند بناء دوال متداخلة تحتفظ بحالة، مثل العدّادات.",
        goal="تعديل متغيرات الدالة المحيطة.",
        syntax="def outer():\n    x = 0\n    def inner():\n        nonlocal x",
        good=C("""
            def counter():
                n = 0
                def inc():
                    nonlocal n
                    n += 1
                    return n
                return inc

            c = counter()
            c()
            print(c())
        """), good_out="2",
        bad="x = 1\nnonlocal x", bad_err="SyntaxError",
        bad_why="nonlocal لا تُستخدم خارج الدوال المتداخلة.",
        explain_q="ماذا يطبع هذا الكود؟",
        explain=C("""
            def outer():
                msg = "قبل"
                def inner():
                    nonlocal msg
                    msg = "بعد"
                inner()
                print(msg)

            outer()
        """),
        explain_ans="يطبع «بعد»، لأن الدالة الداخلية عدّلت msg الخاص بالدالة الخارجية.",
        write="اكتب دالة outer فيها total = 0، وداخلها دالة inner تضيف 10 إلى total باستخدام nonlocal، ثم اطبع total.",
        write_ans="def outer():\n    total = 0\n    def inner():\n        nonlocal total\n        total += 10\n    inner()\n    print(total)\n\nouter()",
        fix="def outer():\n    n = 0\n    def inner():\n        n += 1\n    inner()\n\nouter()", fix_err="UnboundLocalError",
        fix_ans="def outer():\n    n = 0\n    def inner():\n        nonlocal n\n        n += 1\n    inner()\n\nouter()",
        fix_why="أضف nonlocal n داخل inner.",
        bonus="global للمستوى الأعلى (البرنامج كله)، و nonlocal للمستوى الذي فوقك مباشرة.",
    ),
    # ==================== الأصناف والحذف ====================
    dict(
        key="class", group="objects", level=later("الوحدة 12 (البرمجة الكائنية)"),
        real="مخطط البناء عند المهندس: من مخطط واحد تُبنى منازل كثيرة، لكل منزل لونه وعنوانه الخاص.",
        what="تعرّف «صنفاً»: قالباً تصنع منه كائنات لها بيانات وتصرفات.",
        name="class كلمة إنجليزية معناها «صنف» أو «فئة»، لأنها تصف فئة من الأشياء المتشابهة (فئة المرضى، فئة الأطباء).",
        why="أساس البرمجة الكائنية التي تُبنى بها البرامج الكبيرة مثل أنظمة السجلات الصحية.",
        goal="تنظيم البيانات والدوال المرتبطة بها في وحدة واحدة.",
        syntax="class اسم_الصنف:\n    ...",
        good=C("""
            class Patient:
                def __init__(self, name):
                    self.name = name

            p = Patient("Sara")
            print(p.name)
        """), good_out="Sara",
        bad='class = "Python 1"', bad_err="SyntaxError",
        bad_why="class محجوزة لتعريف الأصناف؛ استخدم class_name أو course.",
        explain_q="ماذا يطبع هذا الكود؟", explain='class Clinic:\n    city = "Amman"\n\nprint(Clinic.city)',
        explain_ans="يطبع Amman؛ city خاصية معرّفة داخل الصنف.",
        write='عرّف صنفاً Course فيه خاصية name قيمتها "Python"، ثم اطبعها.',
        write_ans='class Course:\n    name = "Python"\n\nprint(Course.name)',
        fix="class Patient\n    pass", fix_err="SyntaxError",
        fix_ans="class Patient:\n    pass",
        fix_why="سطر class يحتاج نقطتين رأسيتين.",
        bonus="أسماء الأصناف تُكتب بأسلوب PascalCase: أول حرف من كل كلمة كبير، مثل PatientRecord.",
    ),
    dict(
        key="del", group="objects", level=later("الوحدة 08 (القوائم والقواميس)"),
        real="تشطب اسم شخص من قائمة المدعوين لأنه اعتذر عن الحضور.",
        what="تحذف متغيراً، أو عنصراً من قائمة، أو مفتاحاً من قاموس.",
        name="del اختصار للكلمة الإنجليزية delete، ومعناها «احذف».",
        why="لإزالة بيانات لم تعد مطلوبة أو يجب ألا تُحفظ، مثل رقم هاتف مريض.",
        goal="حذف عنصر محدد.",
        syntax="del متغير\ndel قائمة[فهرس]\ndel قاموس[مفتاح]",
        good=C("""
            patient = {"name": "Ali", "phone": "079"}
            del patient["phone"]
            print(patient)
        """), good_out="{'name': 'Ali'}",
        bad="x = 5\ndel x\nprint(x)", bad_err="NameError",
        bad_why="بعد del لم يعد المتغير x موجوداً، فلا يمكن طباعته.",
        explain_q="ماذا يطبع هذا الكود؟", explain="nums = [10, 20, 30]\ndel nums[0]\nprint(nums)",
        explain_ans="يطبع [20, 30]؛ حُذف العنصر الأول (الفهرس 0).",
        write="لديك readings = [120, 130, 125]. احذف العنصر الأخير باستخدام del ثم اطبع القائمة.",
        write_ans="readings = [120, 130, 125]\ndel readings[-1]\nprint(readings)",
        fix='d = {"a": 1}\ndel d["b"]', fix_err="KeyError",
        fix_ans='d = {"a": 1}\nd.pop("b", None)',
        fix_why="المفتاح b غير موجود. إمّا أن تحذف مفتاحاً موجوداً، أو تستخدم pop مع قيمة افتراضية لتجنب الخطأ.",
        bonus="del تحذف «الاسم» فقط؛ أما الكائن نفسه فتحذفه بايثون تلقائياً من الذاكرة عندما لا يشير إليه أي اسم.",
    ),
    # ==================== التعامل مع الأخطاء ====================
    dict(
        key="try", group="errors", level=later("الوحدة 11 (معالجة الأخطاء)"),
        real="في السيرك، البهلوان «يحاول» حركته الخطرة وتحته شبكة أمان؛ إن سقط التقطته الشبكة واستمر العرض.",
        what="كتلة تجرّب فيها كوداً قد يفشل، دون أن يتوقف البرنامج كله.",
        name="try كلمة إنجليزية معناها «حاول».",
        why="بدونها يكفي خطأ واحد (مثل إدخال نص بدل رقم) لإيقاف البرنامج كاملاً.",
        goal="حماية جزء خطِر من الكود.",
        syntax="try:\n    كود قد يفشل\nexcept نوع_الخطأ:\n    البديل",
        good=C("""
            try:
                age = int("25")
                print(age)
            except ValueError:
                print("ليس رقماً")
        """), good_out="25",
        bad='try:\n    x = 1 / 0\nprint("x")', bad_err="SyntaxError",
        bad_why="try لا تأتي وحدها؛ يجب أن تتبعها except أو finally.",
        explain_q="ماذا يطبع هذا الكود؟", explain='try:\n    print(10 / 0)\nexcept ZeroDivisionError:\n    print("قسمة على صفر")',
        explain_ans="يطبع «قسمة على صفر»؛ القسمة فشلت فانتقل التنفيذ إلى except.",
        write='حاول تحويل النص "abc" إلى رقم باستخدام int، واطبع "إدخال غير صالح" عند الفشل.',
        write_ans='try:\n    n = int("abc")\nexcept ValueError:\n    print("إدخال غير صالح")',
        fix='try:\nnum = int("5")\nexcept ValueError:\n    pass', fix_err="IndentationError",
        fix_ans='try:\n    num = int("5")\nexcept ValueError:\n    pass',
        fix_why="الكود داخل try يجب أن يُزاح 4 مسافات.",
        bonus="اجعل كتلة try صغيرة قدر الإمكان: ضع فيها فقط السطر الذي قد يفشل.",
    ),
    dict(
        key="except", group="errors", level=later("الوحدة 11 (معالجة الأخطاء)"),
        real="شبكة الأمان نفسها في السيرك: هي التي «تلتقط» البهلوان عندما يسقط.",
        what="تلتقط نوعاً محدداً من الأخطاء وتنفذ بدلاً منه كوداً بديلاً.",
        name="except من «exception» أي «استثناء»: الخطأ حالة استثنائية خرجت عن المسار الطبيعي.",
        why="تعرض للمستخدم رسالة مفهومة بالعربية بدل رسالة خطأ مخيفة بالإنجليزية.",
        goal="معالجة الخطأ بطريقة مناسبة.",
        syntax="except نوع_الخطأ:\n    ...",
        good=C("""
            patient = {"id": "P1"}
            try:
                print(patient["age"])
            except KeyError:
                print("العمر غير مسجل")
        """), good_out="العمر غير مسجل",
        bad='except ValueError:\n    print("خطأ")', bad_err="SyntaxError",
        bad_why="except لا تأتي إلا بعد try.",
        explain_q="ماذا يطبع هذا الكود؟", explain='try:\n    int("x")\nexcept ValueError:\n    print("خطأ في التحويل")\nprint("استمر البرنامج")',
        explain_ans="يطبع «خطأ في التحويل» ثم «استمر البرنامج»؛ الخطأ عولج فلم يتوقف البرنامج.",
        write='لديك readings = [120, 130]. حاول طباعة readings[5]، والتقط IndexError واطبع "لا توجد قراءة".',
        write_ans='readings = [120, 130]\ntry:\n    print(readings[5])\nexcept IndexError:\n    print("لا توجد قراءة")',
        fix='try:\n    x = int("a")\nexcept ValueError\n    print("خطأ")', fix_err="SyntaxError",
        fix_ans='try:\n    x = int("a")\nexcept ValueError:\n    print("خطأ")',
        fix_why="سطر except يحتاج نقطتين رأسيتين.",
        bonus="تجنّب كتابة except: وحدها دون نوع الخطأ؛ ستُخفي أخطاء حقيقية في برنامجك دون أن تعرف.",
    ),
    dict(
        key="finally", group="errors", level=later("الوحدة 11 (معالجة الأخطاء)"),
        real="بعد العملية الجراحية، سواء نجحت أم لا، يجب «في النهاية» تعقيم الأدوات دائماً.",
        what="كتلة تُنفذ دائماً، سواء حدث خطأ أم لم يحدث.",
        name="finally كلمة إنجليزية معناها «أخيراً» أو «في النهاية».",
        why="تضمن تنفيذ أعمال التنظيف المهمة، مثل إغلاق ملف أو اتصال بقاعدة بيانات.",
        goal="تنفيذ كود ختامي في كل الأحوال.",
        syntax="try:\n    ...\nfinally:\n    ...",
        good=C("""
            try:
                print("قراءة البيانات")
            finally:
                print("إغلاق الملف")
        """), good_out="قراءة البيانات\nإغلاق الملف",
        bad='finally:\n    print("تم")', bad_err="SyntaxError",
        bad_why="finally جزء من بنية try، ولا تأتي وحدها.",
        explain_q="ماذا يطبع هذا الكود؟",
        explain='try:\n    x = 1 / 0\nexcept ZeroDivisionError:\n    print("خطأ")\nfinally:\n    print("انتهى")',
        explain_ans="يطبع «خطأ» ثم «انتهى»: حدث الخطأ فعولج، ثم نُفذت finally كالعادة.",
        write='اقسم 10 على 2 داخل try واطبع الناتج، واطبع "تم" في finally.',
        write_ans='try:\n    print(10 / 2)\nfinally:\n    print("تم")',
        fix="try:\n    print(1)\nfinaly:\n    print(2)", fix_err="SyntaxError",
        fix_ans="try:\n    print(1)\nfinally:\n    print(2)",
        fix_why="خطأ إملائي: الصواب finally (بحرفي l).",
        bonus="finally تُنفذ حتى لو كان داخل try أمر return؛ لذلك هي المكان الأضمن لأعمال التنظيف.",
    ),
    dict(
        key="raise", group="errors", level=later("الوحدة 11 (معالجة الأخطاء)"),
        real="الحكم «يرفع» البطاقة الحمراء عند المخالفة فيتوقف اللعب فوراً.",
        what="تُطلق خطأً بنفسك عندما تكون البيانات غير منطقية.",
        name="raise كلمة إنجليزية معناها «ارفع».",
        why="تمنع البرنامج من متابعة العمل ببيانات خاطئة، مثل عمر سالب أو حرارة 80 درجة.",
        goal="حراسة الدوال من المدخلات الخاطئة.",
        syntax='raise ValueError("رسالة توضح الخطأ")',
        good=C("""
            def set_age(age):
                if age < 0:
                    raise ValueError("العمر لا يكون سالباً")
                return age

            print(set_age(30))
        """), good_out="30",
        bad='raise "خطأ"', bad_err="TypeError",
        bad_why="لا يمكن رفع نص؛ يجب رفع كائن خطأ مثل ValueError(\"...\").",
        explain_q="ماذا يطبع هذا الكود؟", explain='try:\n    raise ValueError("قيمة سالبة")\nexcept ValueError as e:\n    print(e)',
        explain_ans="يطبع «قيمة سالبة»؛ رُفع الخطأ ثم التُقط وطُبعت رسالته.",
        write='اكتب دالة check_temp(t) ترفع ValueError إذا كانت t أكبر من 45، وإلا ترجع t.',
        write_ans='def check_temp(t):\n    if t > 45:\n        raise ValueError("حرارة غير منطقية")\n    return t\n\nprint(check_temp(37))',
        fix='def check(age):\n    if age < 0:\n        raise ValueError("عمر غير صالح"\n    return age', fix_err="SyntaxError",
        fix_ans='def check(age):\n    if age < 0:\n        raise ValueError("عمر غير صالح")\n    return age\n\nprint(check(5))',
        fix_why="ينقص القوس الأخير بعد رسالة الخطأ.",
        bonus="يمكنك تعريف أخطاء خاصة بمجالك، مثل: class InvalidSequenceError(Exception): pass",
    ),
    dict(
        key="assert", group="errors", level=later("الوحدة 11 (معالجة الأخطاء)"),
        real="قبل الإقلاع يراجع الطيار قائمة فحص: «تأكّد» أن الوقود كافٍ. إن لم يكن كذلك فلا إقلاع.",
        what="تتحقق من شرط يجب أن يكون صحيحاً، وتوقف البرنامج بخطأ إن لم يكن كذلك.",
        name="assert كلمة إنجليزية معناها «أكِّد» أو «اجزم».",
        why="تكشف الأخطاء مبكراً أثناء كتابة البرنامج واختباره، قبل أن تسبب نتائج خاطئة.",
        goal="فحص الافتراضات داخل الكود.",
        syntax='assert شرط, "رسالة عند الفشل"',
        good=C("""
            seq = "ATGC"
            assert len(seq) > 0, "تسلسل فارغ"
            print("التسلسل صالح")
        """), good_out="التسلسل صالح",
        bad='seq = ""\nassert len(seq) > 0, "تسلسل فارغ"', bad_err="AssertionError",
        bad_why="الشرط خاطئ لأن التسلسل فارغ، فتوقف البرنامج مع الرسالة «تسلسل فارغ».",
        explain_q="ماذا يطبع هذا الكود؟", explain='assert 2 + 2 == 4\nprint("صحيح")',
        explain_ans="يطبع «صحيح»؛ الشرط متحقق فلا يحدث شيء ويستمر البرنامج.",
        write='لديك weight = 70. تأكد باستخدام assert أن الوزن أكبر من صفر مع رسالة "وزن غير صالح".',
        write_ans='weight = 70\nassert weight > 0, "وزن غير صالح"',
        fix='seq = ""\nassert(len(seq) > 0, "فارغ")\nprint("مرّ الفحص!")', fix_err="خطأ منطقي",
        fix_out="مرّ الفحص!",
        fix_ans='seq = ""\nassert len(seq) > 0, "فارغ"',
        fix_ans_err="AssertionError",
        fix_why="الأقواس جعلت الشرط والرسالة tuple غير فارغة، فيمرّ الفحص دائماً حتى مع تسلسل فارغ! بعد حذف الأقواس يعمل الفحص فعلاً ويوقف البرنامج بـ AssertionError كما يجب.",
        bonus="لا تستخدم assert للتحقق من مدخلات المستخدم، لأنها تتعطل عند تشغيل بايثون بالخيار ‎-O. للمدخلات استخدم if و raise.",
    ),
    # ==================== الاستيراد والموارد ====================
    dict(
        key="import", group="imports", level=later("الوحدة 13 (الوحدات والمكتبات)"),
        real="بدلاً من أن تصنع مفكاً ومطرقة بنفسك، تحضر صندوق أدوات جاهزاً من المحل.",
        what="تجلب وحدة أو مكتبة جاهزة إلى برنامجك لتستخدم أدواتها.",
        name="import كلمة إنجليزية معناها «استيراد».",
        why="آلاف المكتبات الجاهزة (رياضيات، تحليل بيانات، تسلسلات جينية) توفّر عليك سنوات من العمل.",
        goal="استخدام كود كتبه آخرون واختبروه.",
        syntax="import اسم_الوحدة",
        good=C("""
            import math
            print(math.sqrt(16))
        """), good_out="4.0",
        bad="import Math", bad_err="ModuleNotFoundError",
        bad_why="اسم الوحدة math بأحرف صغيرة؛ بايثون حساسة لحالة الأحرف.",
        explain_q="ماذا يطبع هذا الكود؟", explain="import math\nprint(math.pi > 3)",
        explain_ans="يطبع True؛ قيمة π تقارب 3.14159.",
        write="استورد الوحدة statistics واطبع متوسط القراءات [120, 130, 125] باستخدام statistics.mean.",
        write_ans="import statistics\nprint(statistics.mean([120, 130, 125]))",
        fix="import math\nprint(sqrt(9))", fix_err="NameError",
        fix_ans="import math\nprint(math.sqrt(9))",
        fix_why="بعد import math يجب كتابة اسم الوحدة قبل الدالة: math.sqrt.",
        bonus="جرّب كتابة import this في بايثون: ستطبع «زِن بايثون»، وهي مبادئ اللغة في 19 سطراً.",
    ),
    dict(
        key="from", group="imports", level=later("الوحدة 13 (الوحدات والمكتبات)"),
        real="من صندوق الأدوات كله، تأخذ المفك «فقط» لأنه كل ما تحتاجه.",
        what="تستورد جزءاً محدداً من وحدة بدل الوحدة كاملة.",
        name="from كلمة إنجليزية معناها «من».",
        why="تجعل الكود أقصر: تكتب sqrt بدل math.sqrt.",
        goal="استيراد ما تحتاجه فقط.",
        syntax="from الوحدة import الاسم",
        good=C("""
            from math import sqrt
            print(sqrt(25))
        """), good_out="5.0",
        bad="from math import squareroot", bad_err="ImportError",
        bad_why="لا توجد دالة بهذا الاسم في math؛ اسمها الصحيح sqrt.",
        explain_q="ماذا يطبع هذا الكود؟", explain="from math import pi\nprint(round(pi, 2))",
        explain_ans="يطبع 3.14؛ قيمة π مقربة لخانتين عشريتين.",
        write="استورد الدالة mean فقط من statistics واطبع متوسط [2, 4, 6].",
        write_ans="from statistics import mean\nprint(mean([2, 4, 6]))",
        fix="import sqrt from math", fix_err="SyntaxError",
        fix_ans="from math import sqrt",
        fix_why="الترتيب الصحيح: from الوحدة import الاسم.",
        bonus="تجنّب from math import * لأنها تجلب كل الأسماء فتختلط بأسماء متغيراتك دون أن تشعر.",
    ),
    dict(
        key="as", group="imports", level=later("الوحدة 13 (الوحدات والمكتبات)"),
        real="بدلاً من مناداة صديقك باسمه الكامل كل مرة، تناديه بلقبه القصير «أبو أحمد».",
        what="تعطي اسماً مستعاراً قصيراً لوحدة أو شيء آخر.",
        name="as كلمة إنجليزية معناها «باسم» أو «بصفة».",
        why="بعض أسماء المكتبات طويلة، وهناك اختصارات عالمية يفهمها كل المبرمجين: np و pd.",
        goal="تقصير الأسماء وتوحيدها.",
        syntax="import الوحدة as اختصار",
        good=C("""
            import statistics as st
            print(st.mean([2, 4, 6]))
        """), good_out="4",
        bad="import statistics as st\nprint(statistics.mean([1, 2]))", bad_err="NameError",
        bad_why="بعد إعطاء الاسم المستعار st لم يعد الاسم statistics معرّفاً؛ استخدم st.",
        explain_q="ماذا يطبع هذا الكود؟", explain="import math as m\nprint(m.floor(2.7))",
        explain_ans="يطبع 2؛ الدالة floor تقرّب للأسفل، و m هو اسم مستعار لـ math.",
        write="استورد الوحدة datetime باسم مستعار dt.",
        write_ans="import datetime as dt\nprint(dt.date(2026, 1, 1))",
        fix="import math as\nprint(math.pi)", fix_err="SyntaxError",
        fix_ans="import math as m\nprint(m.pi)",
        fix_why="بعد as يجب كتابة الاسم المستعار، ثم استخدامه.",
        bonus="as تظهر في ثلاثة أماكن: import x as y، و except ValueError as e، و with open(...) as f.",
    ),
    dict(
        key="with", group="imports", level=later("الوحدة 10 (الملفات)"),
        real="تستعير كتاباً من مكتبة الجامعة، وعند انتهاء المدة يُسجَّل إرجاعه تلقائياً دون أن تتذكر ذلك.",
        what="تفتح مورداً مثل الملف، وتغلقه تلقائياً عند الانتهاء حتى لو حدث خطأ.",
        name="with كلمة إنجليزية معناها «مع»: افعل هذه الأوامر «مع» هذا الملف المفتوح.",
        why="نسيان إغلاق الملف قد يُفقدك البيانات أو يمنع البرامج الأخرى من فتحه.",
        goal="التعامل الآمن مع الملفات والموارد.",
        syntax="with open(اسم_الملف) as f:\n    أوامر",
        good=C("""
            with open("notes.txt", "w") as f:
                f.write("ATGC")

            with open("notes.txt") as f:
                print(f.read())
        """), good_out="ATGC",
        bad='with open("missing.txt") as f:\n    print(f.read())', bad_err="FileNotFoundError",
        bad_why="الملف غير موجود. الوضع الافتراضي \"r\" للقراءة فقط ويتطلب وجود الملف.",
        explain_q="ماذا يطبع هذا الكود؟", explain='with open("a.txt", "w") as f:\n    f.write("hi")\nprint(f.closed)',
        explain_ans="يطبع True؛ عند الخروج من كتلة with أُغلق الملف تلقائياً.",
        write='اكتب النص "مرحبا" في ملف اسمه hello.txt باستخدام with.',
        write_ans='with open("hello.txt", "w", encoding="utf-8") as f:\n    f.write("مرحبا")',
        fix='with open("data.txt", "w") as f\n    f.write("1")', fix_err="SyntaxError",
        fix_ans='with open("data.txt", "w") as f:\n    f.write("1")',
        fix_why="سطر with يحتاج نقطتين رأسيتين.",
        bonus='عند كتابة نصوص عربية أضف encoding="utf-8" دائماً حتى تظهر الحروف صحيحة على كل الأجهزة.',
    ),
    # ==================== غير المتزامن ====================
    dict(
        key="async", group="async", level="متقدمة – خارج نطاق المقررين، يكفي أن تعرف أنها محجوزة",
        real="الطاهي الماهر يضع الأرز على النار، وبدلاً من الوقوف منتظراً يقطّع السلطة. هذا عمل «غير متزامن».",
        what="تعرّف دالة يمكنها أن تنتظر شيئاً بطيئاً دون أن توقف بقية البرنامج.",
        name="async اختصار للكلمة الإنجليزية asynchronous، ومعناها «غير متزامن».",
        why="مهمة عند جلب بيانات من الإنترنت، مثل تنزيل تسلسلات من قاعدة NCBI، دون تجميد البرنامج.",
        goal="تنفيذ مهام انتظار متعددة بكفاءة.",
        syntax="async def اسم_الدالة():\n    ...",
        good=C("""
            import asyncio

            async def hello():
                return "مرحبا"

            print(asyncio.run(hello()))
        """), good_out="مرحبا",
        bad="async = True", bad_err="SyntaxError",
        bad_why="async محجوزة منذ إصدار بايثون 3.7.",
        explain_q="ماذا يطبع هذا الكود؟", explain="import asyncio\n\nasync def compute():\n    return 2 * 3\n\nprint(asyncio.run(compute()))",
        explain_ans="يطبع 6؛ asyncio.run تشغّل الدالة غير المتزامنة وترجع نتيجتها.",
        write='اكتب دالة غير متزامنة done ترجع "تم"، وشغّلها باستخدام asyncio.run واطبع النتيجة.',
        write_ans='import asyncio\n\nasync def done():\n    return "تم"\n\nprint(asyncio.run(done()))',
        fix="def async fetch():\n    pass", fix_err="SyntaxError",
        fix_ans="async def fetch():\n    pass",
        fix_why="async تأتي قبل def وليس بعدها.",
        bonus="البرمجة غير المتزامنة موضوع متقدم؛ ستحتاجها عند بناء خوادم الويب أو أدوات تجلب بيانات كثيرة من الإنترنت.",
    ),
    dict(
        key="await", group="async", level="متقدمة – خارج نطاق المقررين، يكفي أن تعرف أنها محجوزة",
        real="تنتظر قهوتك من الآلة، لكن المقهى لا يتوقف: يستمر في خدمة الزبائن الآخرين حتى تجهز قهوتك.",
        what="تنتظر نتيجة دالة غير متزامنة، وتسمح للبرنامج بإنجاز أعمال أخرى خلال الانتظار.",
        name="await كلمة إنجليزية معناها «انتظِر».",
        why="بدونها لا تحصل على نتيجة الدالة غير المتزامنة.",
        goal="أخذ نتيجة مهمة بطيئة عند جهوزها.",
        syntax="نتيجة = await دالة_غير_متزامنة()",
        good=C("""
            import asyncio

            async def get_value():
                await asyncio.sleep(0)
                return 42

            async def main():
                v = await get_value()
                print(v)

            asyncio.run(main())
        """), good_out="42",
        bad="def main():\n    await something()", bad_err="SyntaxError",
        bad_why="await تعمل فقط داخل دالة معرّفة بـ async def.",
        explain_q="ماذا يطبع هذا الكود؟",
        explain='import asyncio\n\nasync def main():\n    print("قبل")\n    await asyncio.sleep(0)\n    print("بعد")\n\nasyncio.run(main())',
        explain_ans="يطبع «قبل» ثم «بعد»؛ الانتظار لا يغيّر ترتيب الأوامر داخل الدالة نفسها.",
        write='اكتب async def main تنتظر asyncio.sleep(0) ثم تطبع "انتهى"، وشغّلها.',
        write_ans='import asyncio\n\nasync def main():\n    await asyncio.sleep(0)\n    print("انتهى")\n\nasyncio.run(main())',
        fix="async def main():\n    x = await", fix_err="SyntaxError",
        fix_ans="import asyncio\n\nasync def main():\n    x = await asyncio.sleep(0)",
        fix_why="await تحتاج شيئاً تنتظره بعدها.",
        bonus="asyncio.sleep(1) تنتظر ثانية دون أن تجمّد البرنامج، بعكس time.sleep(1) التي تجمّده.",
    ),
]
