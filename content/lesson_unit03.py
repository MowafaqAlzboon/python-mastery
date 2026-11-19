# -*- coding: utf-8 -*-
"""
lesson_unit03.py — الوحدة 03: أنواع البيانات (Data Types)
البنية نفسها ذات الـ 12 نقطة. المفتاح key = اسم النوع كما في الموقع.
"""
from lesson_keywords import C

UNIT = dict(number="03", title="أنواع البيانات", en="Data Types")

GROUPS = [
    ("single", "قيم مفردة", "كل متغير يحمل قيمة واحدة: عدد، نص، نعم/لا، لا شيء."),
    ("collections", "مجموعات", "متغير واحد يحمل عدة قيم."),
    ("advanced", "أنواع متقدمة", "أنواع ستحتاجها في حالات خاصة."),
]

UNIT_INTRO = dict(
    key="أنواع البيانات (Data Types)",
    real="في المطبخ لا تضع الحليب في كيس ورقي، ولا الطحين في زجاجة. لكل شيء وعاء يناسبه. وفي بايثون لكل قيمة «نوع» يناسبها: الأعداد لها نوع، والنصوص لها نوع، والقوائم لها نوع.",
    what="نوع البيانات يحدد شكل القيمة وما يمكن فعله بها: الأعداد تُجمع وتُضرب، والنصوص تُقسم وتُحوّل لحروف كبيرة.",
    name="سُمّيت «أنواعاً» (Types) لأنها تصنّف القيم إلى فئات، كما تصنّف المختبرات العينات إلى دم وبول وأنسجة.",
    why="العملية نفسها تتصرف بطريقة مختلفة حسب النوع: 2 + 2 تعطي 4، أما \"2\" + \"2\" فتعطي \"22\". عدم معرفة النوع من أكثر أسباب الأخطاء.",
    goal="اختيار الوعاء المناسب لكل معلومة: العمر عدد صحيح، الحرارة عدد عشري، الاسم نص.",
    syntax="type(القيمة)  # لمعرفة نوع أي قيمة",
    good=C("""
        print(type(25))
        print(type(36.6))
        print(type("Ali"))
    """), good_out="<class 'int'>\n<class 'float'>\n<class 'str'>",
    bad='age = "25"\nprint(age + 1)', bad_err="TypeError",
    bad_why="العمر مخزّن كنص بين علامتي تنصيص، ولا يمكن جمع نص مع عدد.",
    explain_q="ماذا يطبع كل سطر؟", explain='print(2 + 2)\nprint("2" + "2")',
    explain_ans="السطر الأول يطبع 4 (جمع عددين)، والثاني يطبع 22 (دمج نصين). العملية نفسها والنتيجة مختلفة بسبب النوع.",
    write="اطبع نوع القيمة True ونوع القيمة None.",
    write_ans="print(type(True))\nprint(type(None))",
    fix='weight = "70"\nprint(weight * 2)', fix_err="خطأ منطقي",
    fix_out="7070",
    fix_ans="weight = 70\nprint(weight * 2)",
    fix_why="يطبع 7070 بدل 140، لأن الوزن نص فكُرّر مرتين. احذف علامتي التنصيص ليصبح عدداً.",
    bonus="بايثون لغة «ديناميكية الأنواع»: لا تكتب النوع عند إنشاء المتغير، بل تكتشفه بايثون من القيمة نفسها.",
)

LESSONS = [
    # ==================== قيم مفردة ====================
    dict(
        key="int", group="single", level="تدرسها الآن",
        real="عدد الكراسي في القاعة، عدد أفراد أسرتك، عدد حبات الدواء: أعداد كاملة لا كسور فيها. لا يوجد «نصف كرسي».",
        what="العدد الصحيح: عدد بلا فاصلة عشرية، موجب أو سالب أو صفر.",
        name="int اختصار integer أي «عدد صحيح» (Integer كلمة لاتينية تعني «كامل»).",
        why="أغلب العدّ في البرامج أعداد صحيحة: عدد المرضى، طول التسلسل، رقم الدورة في الحلقة.",
        goal="تمثيل الكميات التي تُعدّ ولا تُقاس.",
        syntax="age = 45\nseq_length = 1500",
        good=C("""
            patients = 12
            beds = 10
            print(patients - beds)
        """), good_out="2",
        bad='beds = int("10.5")', bad_err="ValueError",
        bad_why="النص \"10.5\" فيه فاصلة عشرية، فلا تستطيع int تحويله مباشرة. حوّله أولاً بـ float ثم بـ int.",
        explain_q="ماذا يطبع هذا الكود؟", explain="print(int(3.9))",
        explain_ans="يطبع 3. الدالة int تحذف الجزء العشري ولا تقرّب.",
        write="خزّن عدد قواعد تسلسل طوله 1500 في متغير، ثم اطبع نوعه.",
        write_ans="seq_length = 1500\nprint(type(seq_length))",
        fix='age = "30"\nprint(age + 5)', fix_err="TypeError",
        fix_ans='age = int("30")\nprint(age + 5)',
        fix_why="حوّل النص إلى عدد صحيح باستخدام int قبل الجمع.",
        bonus="الأعداد الصحيحة في بايثون ليس لها حد أقصى: جرّب print(2 ** 100) وستحصل على رقم من 31 خانة.",
        bonus_code="print(2 ** 100)",
    ),
    dict(
        key="float", group="single", level="تدرسها الآن",
        real="وزنك على الميزان 72.5 كغ، وحرارتك 37.2 درجة: قياسات فيها كسور.",
        what="العدد العشري: عدد فيه فاصلة عشرية.",
        name="float اختصار floating-point أي «الفاصلة العائمة»، لأن الفاصلة العشرية «تطفو» إلى أي موضع: 3.14 أو 314.0 أو 0.00314.",
        why="كل القياسات الطبية والعلمية تقريباً أعداد عشرية: الحرارة، الضغط، تركيز الجلوكوز، نسبة GC.",
        goal="تمثيل القياسات والنسب.",
        syntax="temperature = 37.2\nbmi = 24.5",
        good=C("""
            weight = 70
            height = 1.75
            print(round(weight / height ** 2, 2))
        """), good_out="22.86",
        bad="temp = 37,2\nprint(temp + 1)", bad_err="TypeError",
        bad_why="الفاصلة العشرية في بايثون نقطة (.) لا فاصلة (,). الفاصلة صنعت مجموعة (tuple) من رقمين.",
        explain_q="ماذا يطبع هذا الكود؟ (النتيجة قد تفاجئك)", explain="print(0.1 + 0.2)",
        explain_ans="يطبع 0.30000000000000004 وليس 0.3، لأن الحاسوب يخزن الكسور بالنظام الثنائي بدقة محدودة. لذلك نستخدم round عند العرض.",
        write="خزّن حرارة مريض 38.6 واطبع الفرق بينها وبين 37.0 مقرباً لخانة واحدة.",
        write_ans="temp = 38.6\nprint(round(temp - 37.0, 1))",
        fix='glucose = float("5,6")', fix_err="ValueError",
        fix_ans='glucose = float("5.6")\nprint(glucose)',
        fix_why="استبدل الفاصلة بنقطة؛ هذا شائع عند قراءة بيانات من برامج عربية أو أوروبية.",
        bonus="القسمة العادية / تعطي دائماً float حتى لو كانت النتيجة كاملة: 10 / 2 تعطي 5.0.",
        bonus_code="print(10 / 2)",
    ),
    dict(
        key="str", group="single", level="تدرسها الآن",
        real="اسمك، عنوانك، رسالة على هاتفك، وتسلسل DNA مثل ATGCGT: كلها حروف متتالية.",
        what="النص: سلسلة من الحروف والرموز بين علامتي تنصيص.",
        name="str اختصار string أي «خيط» أو «سلسلة»، لأن الحروف منظومة واحدة بعد الأخرى كحبات المسبحة على خيط.",
        why="كل ما يُكتب ويُقرأ في البرنامج نص: أسماء المرضى، التشخيصات، التسلسلات الجينية، محتوى الملفات.",
        goal="تخزين البيانات النصية ومعالجتها.",
        syntax='name = "Sara"\nseq = \'ATGC\'',
        good=C("""
            seq = "ATGCGT"
            print(len(seq))
            print(seq.lower())
        """), good_out="6\natgcgt",
        bad="name = Sara", bad_err="NameError",
        bad_why="بدون علامات التنصيص ظنّت بايثون أن Sara اسم متغير غير معرّف.",
        explain_q="ماذا يطبع هذا الكود؟", explain='print("Ha" * 3)',
        explain_ans="يطبع HaHaHa؛ ضرب النص في عدد يكرره.",
        write="خزّن التسلسل \"ATGC\" واطبع أول حرف فيه.",
        write_ans='seq = "ATGC"\nprint(seq[0])',
        fix="message = \"لم تصدر النتيجة')", fix_err="SyntaxError",
        fix_ans='message = "لم تصدر النتيجة"\nprint(message)',
        fix_why="افتح النص وأغلقه بالعلامة نفسها: \" مع \" أو ' مع '.",
        bonus="النصوص «غير قابلة للتعديل»: seq.upper() لا تغيّر seq، بل تعطيك نصاً جديداً يجب أن تخزّنه.",
    ),
    dict(
        key="bool", group="single", level="تدرسها الآن",
        real="مفتاح الإضاءة: إما يعمل أو لا. سؤال في الاستمارة: نعم أو لا. لا يوجد خيار ثالث.",
        what="القيمة المنطقية: إما True (صحيح) أو False (خطأ).",
        name="bool اختصار Boolean، نسبة إلى عالم الرياضيات الإنجليزي جورج بول الذي وضع «جبر المنطق» في القرن التاسع عشر.",
        why="كل الشروط والقرارات في البرنامج تعتمد على قيم منطقية.",
        goal="تمثيل نتائج الأسئلة التي جوابها نعم/لا.",
        syntax="is_diabetic = False\nprint(5 > 3)  # True",
        good=C("""
            hba1c = 7.1
            is_diabetic = hba1c >= 6.5
            print(is_diabetic)
        """), good_out="True",
        bad='is_diabetic = "False"\nif is_diabetic:\n    print("سكري")', bad_err="خطأ منطقي",
        bad_why="يطبع «سكري»! النص \"False\" ليس القيمة False؛ أي نص غير فارغ يُعامل True.",
        bad_out="سكري",
        explain_q="ماذا يطبع هذا الكود؟", explain="print(bool(0), bool(7), bool(\"\"))",
        explain_ans="يطبع False True False: الصفر والنص الفارغ «فارغان» فيعاملان False، وأي عدد آخر True.",
        write="لديك systolic = 145. خزّن في متغير منطقي هل الضغط مرتفع (أكبر من 140) واطبعه.",
        write_ans="systolic = 145\nis_high = systolic > 140\nprint(is_high)",
        fix='has_fever = "True"\nprint(has_fever and False)', fix_err="خطأ منطقي",
        fix_out="False",
        fix_ans="has_fever = True\nprint(has_fever and False)",
        fix_why="الناتج هنا صحيح بالصدفة، لكن المتغير نص لا قيمة منطقية. احذف علامتي التنصيص.",
        bonus="bool فرع من int: True تساوي 1 و False تساوي 0، لذلك sum([True, True, False]) يعطي 2.",
        bonus_code="print(sum([True, True, False]))",
    ),
    dict(
        key="NoneType", group="single", level="تدرسها الآن",
        real="خانة «نتيجة الخزعة» في ملف المريض قبل صدورها: الخانة موجودة لكنها فارغة.",
        what="النوع الذي له قيمة واحدة فقط هي None، وتعني «لا توجد قيمة».",
        name="NoneType أي «نوع اللاشيء»: None تعني «لا شيء»، و Type تعني «نوع».",
        why="تميّز بين «القيمة صفر» و«لا توجد قيمة أصلاً»، وهذا فرق حاسم في البيانات الطبية.",
        goal="تمثيل البيانات الناقصة أو التي لم تُحسب بعد.",
        syntax="lab_result = None",
        good=C("""
            lab_result = None
            print(lab_result is None)
            print(type(lab_result))
        """), good_out="True\n<class 'NoneType'>",
        bad="result = None\nprint(result + 1)", bad_err="TypeError",
        bad_why="لا يمكن إجراء عملية حسابية على «لا شيء». افحص أولاً هل القيمة None.",
        explain_q="ماذا يطبع هذا الكود؟", explain='def get_result():\n    pass\n\nprint(get_result())',
        explain_ans="يطبع None، لأن الدالة لا ترجع شيئاً صراحة.",
        write='لديك biopsy = None. اطبع "بانتظار النتيجة" إذا لم تصدر بعد.',
        write_ans='biopsy = None\nif biopsy is None:\n    print("بانتظار النتيجة")',
        fix="glucose = None\nprint(glucose * 2)", fix_err="TypeError",
        fix_ans='glucose = None\nif glucose is not None:\n    print(glucose * 2)\nelse:\n    print("لا توجد قراءة")',
        fix_why="افحص القيمة قبل استخدامها في الحساب.",
        bonus="في pandas تظهر القيم الناقصة غالباً بالرمز NaN أو None، وستتعامل معها بالدالتين fillna و dropna.",
    ),
    # ==================== مجموعات ====================
    dict(
        key="list", group="collections", level="تعرّف عليها الآن، وتدرسها بعمق في الوحدة 08 (القوائم والقواميس)",
        real="قائمة المشتريات على ورقة: مرتبة، تضيف إليها أو تشطب منها، وقد يتكرر فيها الشيء نفسه.",
        what="القائمة: مجموعة مرتبة من القيم بين قوسين مربعين [ ]، ويمكن تعديلها.",
        name="list تعني «قائمة» بالإنجليزية.",
        why="أكثر هيكل بيانات استخداماً: قراءات الضغط، أسماء المرضى، الكودونات في تسلسل.",
        goal="تخزين عدة قيم مرتبة في متغير واحد، مع إمكانية الإضافة والحذف.",
        syntax="readings = [120, 135, 118]",
        good=C("""
            readings = [120, 135, 118]
            readings.append(140)
            print(readings)
            print(len(readings))
        """), good_out="[120, 135, 118, 140]\n4",
        bad="readings = [120, 135]\nprint(readings[2])", bad_err="IndexError",
        bad_why="الترقيم يبدأ من 0: العنصر الأول readings[0] والثاني readings[1]، ولا يوجد ثالث.",
        explain_q="ماذا يطبع هذا الكود؟", explain='codons = ["ATG", "CCA", "TAA"]\nprint(codons[0], codons[-1])',
        explain_ans="يطبع ATG TAA: الفهرس 0 للأول، والفهرس -1 للأخير.",
        write="أنشئ قائمة بأعمار ثلاثة مرضى، ثم أضف عمراً رابعاً واطبع القائمة.",
        write_ans="ages = [34, 52, 18]\nages.append(70)\nprint(ages)",
        fix="ages = [34, 52, 18\nprint(ages)", fix_err="SyntaxError",
        fix_ans="ages = [34, 52, 18]\nprint(ages)",
        fix_why="القوس المربع لم يُغلق.",
        bonus="القائمة يمكن أن تحتوي أنواعاً مختلفة معاً: [\"Ali\", 52, True]، لكن الأفضل أن تحتوي نوعاً واحداً لتسهيل المعالجة.",
    ),
    dict(
        key="tuple", group="collections", level="تعرّف عليها الآن، وتدرسها بعمق في الوحدة 08 (القوائم والقواميس)",
        real="تاريخ ميلادك (اليوم، الشهر، السنة): مجموعة قيم مرتبة لن تتغير أبداً.",
        what="مجموعة مرتبة من القيم بين قوسين عاديين ( )، لا يمكن تعديلها بعد إنشائها.",
        name="tuple مأخوذة من نهايات كلمات مثل quintuple (خماسية) و sextuple (سداسية)، أي «مجموعة من عدد معين من العناصر».",
        why="تحمي البيانات التي يجب ألا تتغير، مثل إحداثيات جين على الكروموسوم، وهي أسرع من القائمة قليلاً.",
        goal="تجميع قيم ثابتة مرتبطة ببعضها.",
        syntax='gene_location = ("chr7", 117480025)',
        good=C("""
            gene_location = ("chr7", 117480025)
            chromosome, position = gene_location
            print(chromosome)
        """), good_out="chr7",
        bad='dob = (15, 3, 2004)\ndob[0] = 16', bad_err="TypeError",
        bad_why="الـ tuple غير قابلة للتعديل؛ إن احتجت التعديل فاستخدم list.",
        explain_q="ماذا يطبع هذا الكود؟", explain="point = (3, 4)\nx, y = point\nprint(x + y)",
        explain_ans="يطبع 7. السطر الثاني «فكّك» الـ tuple إلى متغيرين.",
        write="أنشئ tuple تخزن ضغط الدم (120, 80) واطبع القيمة الأولى.",
        write_ans="bp = (120, 80)\nprint(bp[0])",
        fix="single = (5)\nprint(type(single))", fix_err="خطأ منطقي",
        fix_out="<class 'int'>",
        fix_ans="single = (5,)\nprint(type(single))",
        fix_why="الأقواس وحدها لا تصنع tuple؛ الفاصلة هي التي تصنعها. لعنصر واحد اكتب (5,).",
        bonus="عندما ترجع الدالة أكثر من قيمة (return a, b) فهي في الحقيقة ترجع tuple.",
    ),
    dict(
        key="dict", group="collections", level="تعرّف عليها الآن، وتدرسها بعمق في الوحدة 08 (القوائم والقواميس)",
        real="دليل الهاتف: تبحث بالاسم (المفتاح) فتجد الرقم (القيمة). وملف المريض كذلك: «الاسم: سارة، العمر: 30».",
        what="القاموس: مجموعة أزواج «مفتاح: قيمة» بين قوسين معقوفين { }.",
        name="dict اختصار dictionary أي «قاموس»: كما تبحث في القاموس عن الكلمة فتجد معناها، تبحث هنا بالمفتاح فتجد القيمة.",
        why="الطريقة الطبيعية لتمثيل السجلات: سجل مريض، نتائج تحليل، عدد مرات ظهور كل قاعدة في تسلسل.",
        goal="الوصول السريع إلى القيم بأسماء واضحة بدل أرقام مواقع.",
        syntax='patient = {"id": "P001", "age": 52}',
        good=C("""
            patient = {"id": "P001", "age": 52}
            patient["bmi"] = 27.3
            print(patient["age"], len(patient))
        """), good_out="52 3",
        bad='patient = {"id": "P001"}\nprint(patient["age"])', bad_err="KeyError",
        bad_why="المفتاح age غير موجود. استخدم patient.get(\"age\") لتحصل على None بدل الخطأ.",
        explain_q="ماذا يطبع هذا الكود؟", explain='counts = {"A": 3, "T": 2}\ncounts["A"] = counts["A"] + 1\nprint(counts)',
        explain_ans="يطبع {'A': 4, 'T': 2}؛ زادت قيمة المفتاح A بواحد.",
        write='أنشئ قاموساً لمريض فيه الاسم "Ali" وفصيلة الدم "O+"، واطبع فصيلة الدم.',
        write_ans='patient = {"name": "Ali", "blood": "O+"}\nprint(patient["blood"])',
        fix='patient = {"name": "Ali", "age" 30}', fix_err="SyntaxError",
        fix_ans='patient = {"name": "Ali", "age": 30}\nprint(patient)',
        fix_why="بين المفتاح وقيمته نقطتان رأسيتان (:).",
        bonus="المفاتيح لا تتكرر: إذا كتبت المفتاح نفسه مرتين تبقى القيمة الأخيرة فقط.",
    ),
    dict(
        key="set", group="collections", level="تعرّف عليها الآن، وتدرسها بعمق في الوحدة 08 (القوائم والقواميس)",
        real="ألبوم طوابع: لا يضع الهاوي الطابع نفسه مرتين، ولا يهمه ترتيبها بل وجودها.",
        what="المجموعة: قيم فريدة بلا تكرار وبلا ترتيب، بين قوسين معقوفين { }.",
        name="set تعني «مجموعة» كما في «نظرية المجموعات» في الرياضيات.",
        why="تحذف التكرار تلقائياً، وتجيب بسرعة كبيرة عن سؤال «هل هذا العنصر موجود؟».",
        goal="معرفة القيم المختلفة، وإجراء عمليات الاتحاد والتقاطع.",
        syntax='bases = {"A", "T", "G", "C"}',
        good=C("""
            seq = "AATTGGCCA"
            unique_bases = set(seq)
            print(len(unique_bases))
        """), good_out="4",
        bad="s = {3, 1, 2}\nprint(s[0])", bad_err="TypeError",
        bad_why="المجموعة بلا ترتيب، فلا يوجد «عنصر أول» يمكن الوصول إليه برقم.",
        explain_q="ماذا يطبع هذا الكود؟", explain="print(set([1, 2, 2, 3, 3, 3]))",
        explain_ans="يطبع {1, 2, 3}؛ حُذف التكرار.",
        write='تحقق هل كل حروف التسلسل "GATTACA" من القواعد A و T و G و C باستخدام set.',
        write_ans='seq = "GATTACA"\nprint(set(seq) <= set("ATGC"))',
        fix="empty = {}\nempty.add(5)", fix_err="AttributeError",
        fix_ans="empty = set()\nempty.add(5)\nprint(empty)",
        fix_why="{} وحدها تصنع قاموساً فارغاً لا مجموعة. للمجموعة الفارغة اكتب set().",
        bonus="البحث بـ in داخل set أسرع بآلاف المرات من البحث داخل list عندما يكون عدد العناصر كبيراً.",
    ),
    dict(
        key="range", group="collections", level="تعرّف عليها الآن، وتدرسها بعمق في الوحدة 06 (هياكل التحكم)",
        real="أرقام المقاعد في الحافلة من 1 إلى 30: لا تحتاج أن تكتبها كلها، يكفي أن تقول «من 1 إلى 30».",
        what="سلسلة أعداد متتالية تُحدد بالبداية والنهاية والخطوة، وتُستخدم غالباً في الحلقات.",
        name="range تعني «مدى» أو «نطاق».",
        why="تولّد أعداداً كثيرة دون أن تحجز ذاكرة لها كلها، وهي أساس الحلقات المعدودة.",
        goal="التكرار عدداً محدداً من المرات، أو المرور على مواقع التسلسل.",
        syntax="range(البداية, النهاية, الخطوة)  # النهاية غير مشمولة",
        good=C("""
            print(list(range(1, 6)))
            print(list(range(0, 9, 3)))
        """), good_out="[1, 2, 3, 4, 5]\n[0, 3, 6]",
        bad="print(list(range(1.5, 4)))", bad_err="TypeError",
        bad_why="range تقبل أعداداً صحيحة فقط.",
        explain_q="ماذا يطبع هذا الكود؟", explain="print(len(range(10)))",
        explain_ans="يطبع 10: الأعداد من 0 إلى 9.",
        write="اطبع قائمة أرقام الأيام من 1 إلى 7 باستخدام range.",
        write_ans="print(list(range(1, 8)))",
        fix="for day in range(1, 7):\n    print(day)  # المطلوب طباعة 1 إلى 7", fix_err="خطأ منطقي",
        fix_out="1\n2\n3\n4\n5\n6",
        fix_ans="for day in range(1, 8):\n    print(day)",
        fix_why="النهاية غير مشمولة؛ لطباعة 7 يجب أن تكون النهاية 8.",
        bonus="range يمكن أن تعدّ تنازلياً بخطوة سالبة: range(10, 0, -2) تعطي 10، 8، 6، 4، 2.",
        bonus_code="print(list(range(10, 0, -2)))",
    ),
    # ==================== أنواع متقدمة ====================
    dict(
        key="complex", group="advanced", level="متقدمة – للاطلاع فقط في البرمجة 1",
        real="موقعك على الخريطة يحتاج رقمين معاً: شرق-غرب وشمال-جنوب. العدد المركّب كذلك: رقم من جزأين في قيمة واحدة.",
        what="عدد له جزء حقيقي وجزء تخيلي يُكتب بالحرف j، مثل 3 + 4j.",
        name="complex تعني «مركّب» لأنه مركّب من جزأين.",
        why="يُستخدم في معالجة الإشارات الحيوية (مثل تخطيط القلب ECG) وتحويلات فورييه.",
        goal="الحسابات العلمية والهندسية المتقدمة.",
        syntax="z = 3 + 4j",
        good=C("""
            z = 3 + 4j
            print(abs(z))
            print(z.real, z.imag)
        """), good_out="5.0\n3.0 4.0",
        bad="z = 3 + 4i", bad_err="SyntaxError",
        bad_why="بايثون تستخدم j للجزء التخيلي (كما في الهندسة الكهربائية) لا i.",
        explain_q="ماذا يطبع هذا الكود؟", explain="print((1 + 2j) + (3 + 1j))",
        explain_ans="يطبع (4+3j): تُجمع الأجزاء الحقيقية معاً (1+3) والتخيلية معاً (2+1).",
        write="أنشئ العدد المركب 6 + 8j واطبع قيمته المطلقة.",
        write_ans="z = 6 + 8j\nprint(abs(z))",
        fix="z = complex(2, j)", fix_err="NameError",
        fix_ans="z = complex(2, 1)\nprint(z)",
        fix_why="الوسيط الثاني للدالة complex هو رقم الجزء التخيلي، لا الحرف j.",
        bonus="القيمة المطلقة لـ 3 + 4j هي 5، وهي طول الوتر في المثلث القائم 3-4-5 الشهير.",
    ),
    dict(
        key="frozenset", group="advanced", level="متقدمة – للاطلاع فقط في البرمجة 1",
        real="قائمة فصائل الدم المعتمدة في بنك الدم: ثابتة لا يُضاف إليها ولا يُحذف منها.",
        what="مجموعة (set) مجمّدة: قيم فريدة لا يمكن تعديلها بعد إنشائها.",
        name="frozen تعني «مجمّد»، فهي set «مجمّدة».",
        why="تحمي المجموعات الثابتة من التعديل الخاطئ، ويمكن استخدامها مفتاحاً في قاموس.",
        goal="تمثيل مجموعات مرجعية ثابتة.",
        syntax='VALID_BASES = frozenset("ATGC")',
        good=C("""
            VALID_BASES = frozenset("ATGC")
            print("G" in VALID_BASES)
        """), good_out="True",
        bad='VALID = frozenset("ATGC")\nVALID.add("U")', bad_err="AttributeError",
        bad_why="frozenset لا تملك add لأنها لا تقبل التعديل.",
        explain_q="ماذا يطبع هذا الكود؟", explain="print(frozenset([1, 1, 2]))",
        explain_ans="يطبع frozenset({1, 2})؛ حُذف التكرار كما في set.",
        write='أنشئ frozenset لفصائل الدم "A" و "B" و "AB" و "O" واطبع عددها.',
        write_ans='BLOOD_GROUPS = frozenset(["A", "B", "AB", "O"])\nprint(len(BLOOD_GROUPS))',
        fix='STOP = frozenset(["TAA", "TAG"])\nSTOP.add("TGA")', fix_err="AttributeError",
        fix_ans='STOP = frozenset(["TAA", "TAG", "TGA"])\nprint(len(STOP))',
        fix_why="ضع كل العناصر عند الإنشاء، لأن التعديل بعده غير ممكن.",
        bonus="كودونات التوقف الثلاثة TAA و TAG و TGA مثال مثالي لـ frozenset في المعلوماتية الحيوية.",
    ),
    dict(
        key="bytes", group="advanced", level="متقدمة – للاطلاع فقط في البرمجة 1",
        real="الصورة على هاتفك لا يخزنها الهاتف كصورة، بل كسلسلة طويلة من الأرقام (بايتات) يحولها إلى صورة عند العرض.",
        what="سلسلة بايتات: بيانات ثنائية خام، تُكتب بالحرف b قبل علامة التنصيص.",
        name="byte وحدة تخزين تساوي 8 بتات؛ و bytes جمعها: «بايتات».",
        why="الملفات المضغوطة والصور وبيانات الأجهزة الطبية تُقرأ كبايتات، ثم تُحوّل إلى نص أو أرقام.",
        goal="التعامل مع البيانات الثنائية وتحويل النصوص للإرسال عبر الشبكة.",
        syntax='raw = b"ATG"\ntext = raw.decode()',
        good=C("""
            raw = "ATG".encode()
            print(raw)
            print(raw.decode())
        """), good_out="b'ATG'\nATG",
        bad='data = b"ATG"\nprint(data + "C")', bad_err="TypeError",
        bad_why="لا يمكن دمج bytes مع str؛ حوّل أحدهما ليطابق الآخر.",
        explain_q="ماذا يطبع هذا الكود؟", explain='print(len("مرحبا".encode("utf-8")))',
        explain_ans="يطبع 10: كلمة «مرحبا» خمسة حروف، لكن كل حرف عربي يأخذ بايتين في ترميز UTF-8.",
        write='حوّل النص "DNA" إلى bytes ثم أعده نصاً واطبعه.',
        write_ans='raw = "DNA".encode()\nprint(raw.decode())',
        fix='raw = b"سلام"', fix_err="SyntaxError",
        fix_ans='raw = "سلام".encode("utf-8")\nprint(raw)',
        fix_why="الكتابة b\"...\" تقبل حروف ASCII الإنجليزية فقط؛ للعربية استخدم encode.",
        bonus="ملفات FASTQ المضغوطة (.gz) في تحليلات التسلسل الجيني تُقرأ أولاً كبايتات ثم تُفك.",
    ),
]
