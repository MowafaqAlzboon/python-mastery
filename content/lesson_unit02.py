# -*- coding: utf-8 -*-
"""
lesson_unit02.py — الوحدة 02: قواعد التسمية (المتغيرات وأسماؤها)
البنية نفسها ذات الـ 12 نقطة (انظر lesson_keywords.py).
المفتاح key = نص القاعدة الأصلية في الموقع حتى يرتبط الدرس بصفّه ولا يُحذف شيء.
نوع خطأ إضافي في هذه الوحدة:
  "مخالفة أسلوب"  الكود يعمل، لكنه يخالف اتفاقية PEP 8 فيصعب قراءته وصيانته.
"""
from lesson_keywords import C

UNIT = dict(number="02", title="قواعد التسمية", en="Naming Rules & PEP 8")

GROUPS = [
    ("must", "قواعد إلزامية", "إذا خالفتها لن يعمل البرنامج."),
    ("style", "اتفاقيات الأسلوب (PEP 8)", "إذا خالفتها يعمل البرنامج، لكن يصعب على غيرك قراءته."),
    ("special", "أسماء خاصة", "معانٍ خاصة للشرطة السفلية _ في بداية الاسم ونهايته."),
]

UNIT_INTRO = dict(
    key="المتغيرات وأسماؤها (Variables & Names)",
    real="في غرفتك صناديق تخزين، تضع في كل صندوق شيئاً وتكتب عليه اسماً لتعرف ما فيه دون أن تفتحه: «كتب»، «شواحن»، «أوراق الجامعة». المتغير في بايثون صندوق تضع فيه قيمة، واسمه هو الملصق المكتوب عليه.",
    what="المتغير اسم يشير إلى قيمة محفوظة في ذاكرة الحاسوب، مثل رقم أو نص، لتستخدمها لاحقاً.",
    name="سُمّي «متغيراً» (Variable) لأن القيمة داخله يمكن أن تتغير أثناء تشغيل البرنامج: العمر اليوم 20 وبعد سنة 21.",
    why="بدون المتغيرات لا تستطيع حفظ أي بيانات أو معالجتها أو إعادة استخدامها. والاسم الجيد يجعل الكود مفهوماً، والاسم الخاطئ يوقف البرنامج أو يربك من يقرؤه.",
    goal="تخزين البيانات مؤقتاً بأسماء واضحة لاستخدامها في الحسابات والقرارات.",
    syntax="اسم_المتغير = القيمة",
    good=C("""
        score = 100
        score = score + 10
        print(score)
    """), good_out="110",
    bad='2name = "Ahmed"', bad_err="SyntaxError",
    bad_why="لا يمكن أن يبدأ اسم المتغير برقم.",
    explain_q="ماذا يطبع هذا الكود؟", explain="x = 5\nx = x * 2\nprint(x)",
    explain_ans="يطبع 10. السطر الثاني يأخذ القيمة القديمة 5، يضربها في 2، ثم يخزن الناتج في الصندوق نفسه.",
    write="أنشئ متغيراً يخزن اسمك، وآخر يخزن عمرك، ثم اطبعهما.",
    write_ans='name = "Sara"\nage = 20\nprint(name, age)',
    fix="my-var = 10", fix_err="SyntaxError",
    fix_ans="my_var = 10",
    fix_why="الشرطة - تعني الطرح في بايثون؛ استخدم الشرطة السفلية _ بدلاً منها.",
    bonus="العلامة = في بايثون لا تعني «يساوي» كما في الرياضيات، بل تعني «خزّن القيمة التي على اليمين في الاسم الذي على اليسار». لذلك x = x + 1 جملة صحيحة تماماً.",
)

LESSONS = [
    # ==================== قواعد إلزامية ====================
    dict(
        key="يبدأ الاسم بحرف أو شرطة سفلية _", group="must", level="تدرسها الآن",
        real="رقم لوحة السيارة في الأردن له شكل محدد، ولا تقبل دائرة الترخيص لوحة مكتوبة بطريقة أخرى. وبايثون كذلك لها شكل محدد لبداية كل اسم.",
        what="أول حرف في اسم المتغير يجب أن يكون حرفاً (a–z أو A–Z) أو شرطة سفلية _، ولا يجوز أن يكون رقماً.",
        name="تُسمّى «قاعدة الحرف الأول» لأنها تتحكم فقط في أول خانة من الاسم؛ بعد ذلك يمكن استخدام الأرقام.",
        why="إذا بدأ الاسم برقم ظنّت بايثون أنه عدد، فتفشل في قراءة السطر ويظهر SyntaxError.",
        goal="تمكين بايثون من التمييز فوراً بين الأسماء والأعداد.",
        syntax="patient1 = ...   ✓\n_temp = ...      ✓\n1patient = ...   ✗",
        good=C("""
            patient1 = "Ali"
            _count = 3
            print(patient1, _count)
        """), good_out="Ali 3",
        bad='1patient = "Ali"', bad_err="SyntaxError",
        bad_why="الاسم بدأ بالرقم 1.",
        explain_q="أي الأسماء التالية صالح؟", explain="dose2 = 5\n_x = 1\nprint(dose2 + _x)",
        explain_ans="كلاهما صالح ويطبع 6: dose2 بدأ بحرف، و _x بدأ بشرطة سفلية. الرقم مسموح في وسط الاسم ونهايته.",
        write="أنشئ متغيراً يخزن جرعة الدواء الثانية (250) باسم صالح، ثم اطبعه.",
        write_ans="dose_2 = 250\nprint(dose_2)",
        fix="2nd_dose = 250", fix_err="SyntaxError",
        fix_ans="second_dose = 250",
        fix_why="انقل الرقم من البداية أو اكتبه بالحروف.",
        bonus="الشرطة السفلية في بداية الاسم لها معنى خاص («للاستخدام الداخلي»)، وستراه في قسم الأسماء الخاصة من هذه الوحدة.",
    ),
    dict(
        key="يتكون الاسم من حروف وأرقام و _ فقط", group="must", level="تدرسها الآن",
        real="البريد الإلكتروني الجامعي لا يقبل المسافات ولا الرموز الغريبة مثل # أو !؛ يقبل حروفاً وأرقاماً ورموزاً محددة فقط.",
        what="اسم المتغير يتكون فقط من الحروف والأرقام والشرطة السفلية _.",
        name="تسمى «الأحرف المسموحة» لأن بايثون تحدد مجموعة صغيرة من الرموز يُسمح بها في الأسماء.",
        why="الرموز مثل - و . و @ لها وظائف في بايثون (طرح، الوصول لخاصية، مزخرف)؛ إذا وضعتها في الاسم فهمت بايثون شيئاً آخر.",
        goal="منع الخلط بين أسماء المتغيرات والعمليات.",
        syntax="gc_content   ✓\ngc-content   ✗\ngc.content   ✗",
        good=C("""
            gc_content = 52.1
            print(gc_content)
        """), good_out="52.1",
        bad="gc-content = 52.1", bad_err="SyntaxError",
        bad_why="بايثون قرأت السطر كأنه gc ناقص content، ولا يمكن التخزين في عملية طرح.",
        explain_q="لماذا يعطي هذا الكود خطأ رغم أن المتغيرين معرّفان؟", explain="gc = 5\ncontent = 2\nprint(gc-content)",
        explain_ans="لا يعطي خطأ! يطبع 3، لأن gc-content هنا عملية طرح بين متغيرين. هذا يوضح لماذا لا يُسمح بالشرطة داخل الاسم.",
        write="أنشئ متغيراً يخزن رقم ملف المريض \"P001\" باسم مكون من كلمتين.",
        write_ans='file_number = "P001"\nprint(file_number)',
        fix="heart.rate = 72", fix_err="NameError",
        fix_ans="heart_rate = 72",
        fix_why="النقطة تعني «خاصية من كائن»، فظنّت بايثون أن heart كائن غير معرّف. استخدم _.",
        bonus="بايثون 3 تقبل الحروف العربية في الأسماء أيضاً، لكن الاتفاق بين المبرمجين أن تُستخدم الحروف الإنجليزية (انظر آخر قاعدة في الوحدة).",
    ),
    dict(
        key="لا مسافات داخل الاسم", group="must", level="تدرسها الآن",
        real="عند تسمية ملف على حاسوبك ترى أحياناً أسماء مثل report_final.docx بدل «report final»، لأن بعض الأنظمة ترتبك من المسافات.",
        what="لا يجوز أن يحتوي اسم المتغير على مسافة.",
        name="تسمى «قاعدة عدم المسافات» لأن المسافة في بايثون تفصل بين العناصر المختلفة في السطر.",
        why="بايثون تقرأ المسافة كحدّ بين كلمتين، فتظن أن patient name شيئان منفصلان، فيظهر SyntaxError.",
        goal="جعل كل اسم «كلمة واحدة» متصلة.",
        syntax="patient_name   ✓\npatient name   ✗",
        good=C("""
            patient_name = "Sara"
            print(patient_name)
        """), good_out="Sara",
        bad='patient name = "Sara"', bad_err="SyntaxError",
        bad_why="المسافة قسمت الاسم إلى كلمتين.",
        explain_q="ماذا يطبع هذا الكود؟", explain='first_name = "Omar"\nlast_name = "Ali"\nprint(first_name, last_name)',
        explain_ans="يطبع Omar Ali. المسافة بين الكلمتين في الناتج تضعها print تلقائياً بين القيم، وليست جزءاً من الاسمين.",
        write="أنشئ متغيراً يخزن فصيلة الدم \"O+\" باسم من كلمتين دون مسافة.",
        write_ans='blood_type = "O+"\nprint(blood_type)',
        fix="heart rate = 80", fix_err="SyntaxError",
        fix_ans="heart_rate = 80",
        fix_why="استبدل المسافة بشرطة سفلية.",
        bonus="هناك أسلوبان لدمج الكلمات: snake_case (patient_name) المستخدم في بايثون، و camelCase (patientName) المستخدم في لغات مثل JavaScript.",
    ),
    dict(
        key="بايثون حساسة لحالة الأحرف", group="must", level="تدرسها الآن",
        real="كلمة المرور Amman2026 تختلف عن amman2026؛ النظام يعتبرهما كلمتين مختلفتين تماماً.",
        what="الحرف الكبير والصغير مختلفان في بايثون: age و Age و AGE ثلاثة أسماء مختلفة.",
        name="تسمى «الحساسية لحالة الأحرف» (Case Sensitivity) لأن بايثون تنتبه لحالة الحرف: كبير (Upper case) أو صغير (Lower case).",
        why="من أكثر أخطاء المبتدئين شيوعاً: تعرّف المتغير بحرف صغير ثم تكتبه بحرف كبير فيظهر NameError.",
        goal="الدقة: كل اسم يُكتب دائماً بالطريقة نفسها حرفاً حرفاً.",
        syntax="age = 30\nprint(age)   ✓\nprint(Age)   ✗",
        good=C("""
            age = 30
            print(age)
        """), good_out="30",
        bad="age = 30\nprint(Age)", bad_err="NameError",
        bad_why="المتغير المعرّف هو age بحرف صغير، أما Age فلم يُعرَّف أبداً.",
        explain_q="ماذا يطبع هذا الكود؟", explain='name = "Ali"\nName = "Sara"\nprint(name)',
        explain_ans="يطبع Ali، لأن name و Name متغيران مختلفان، ولكل منهما قيمته.",
        write="عرّف متغيراً اسمه bmi قيمته 22.5، ثم اطبعه بكتابة الاسم بالحالة نفسها تماماً.",
        write_ans="bmi = 22.5\nprint(bmi)",
        fix='Diagnosis = "Asthma"\nprint(diagnosis)', fix_err="NameError",
        fix_ans='diagnosis = "Asthma"\nprint(diagnosis)',
        fix_why="وحّد حالة الأحرف؛ والأفضل حروف صغيرة للمتغيرات.",
        bonus="الحساسية لحالة الأحرف تشمل الكلمات المحجوزة والدوال أيضاً: True صحيحة و true خاطئة، و print صحيحة و Print خاطئة.",
    ),
    dict(
        key="لا تستخدم الكلمات المحجوزة", group="must", level="تدرسها الآن",
        real="الطاولة المحجوزة في المطعم ليست لك مهما كانت فارغة (راجع الوحدة 01).",
        what="لا يجوز تسمية متغير بإحدى الكلمات المحجوزة الـ35 مثل if أو class أو for.",
        name="لأنها «محجوزة» للغة نفسها لبناء الأوامر.",
        why="استخدامها اسماً يسبب SyntaxError فوراً.",
        goal="ترك الكلمات المحجوزة لوظيفتها، واختيار أسماء وصفية بديلة.",
        syntax="class_name = ...   ✓\nclass = ...        ✗",
        good=C("""
            class_name = "Python 1"
            print(class_name)
        """), good_out="Python 1",
        bad='class = "Python 1"', bad_err="SyntaxError",
        bad_why="class كلمة محجوزة لتعريف الأصناف.",
        explain_q="هل هذا الاسم صالح؟ ماذا يطبع؟", explain="if_valid = True\nprint(if_valid)",
        explain_ans="صالح ويطبع True؛ if_valid ليست كلمة محجوزة، بل اسم يحتوي كلمة محجوزة، وهذا مسموح.",
        write="أنشئ متغيراً يخزن كلمة \"pass\" (نتيجة الطالب) باسم صالح.",
        write_ans='result = "pass"\nprint(result)',
        fix="lambda = 0.5", fix_err="SyntaxError",
        fix_ans="wavelength = 0.5",
        fix_why="lambda محجوزة؛ في الفيزياء والأحياء يُستخدم الاسم wavelength أو lam بدلاً منها.",
        bonus="إذا احتجت اسماً يشبه كلمة محجوزة، أضف شرطة سفلية في نهايته: class_ أو lambda_. هذه اتفاقية معروفة في PEP 8.",
    ),
    # ==================== اتفاقيات الأسلوب ====================
    dict(
        key="تجنب أسماء الدوال المدمجة", group="style", level="تدرسها الآن",
        real="تخيّل أنك سمّيت قطتك «طبيب». في المرة القادمة التي تنادي فيها «طبيب!» في البيت ستأتي القطة بدل الطبيب.",
        what="لا تسمّي متغيراتك بأسماء دوال بايثون الجاهزة مثل list و str و sum و len و max.",
        name="تسمى «طمس الأسماء» (Shadowing) لأن متغيرك يغطي على الدالة الأصلية كما يغطي الظل على ما تحته.",
        why="بايثون تسمح بذلك دون خطأ، لكن الدالة الأصلية تتوقف عن العمل في بقية البرنامج، فيظهر خطأ غامض لاحقاً.",
        goal="الحفاظ على الدوال المدمجة صالحة للاستخدام.",
        syntax="readings = [1, 2]   ✓\nlist = [1, 2]       ✗ (يطمس list)",
        good=C("""
            readings = [120, 130]
            print(sum(readings))
        """), good_out="250",
        bad="sum = 10\nprint(sum([1, 2, 3]))", bad_err="TypeError",
        bad_why="بعد السطر الأول صار sum رقماً لا دالة، فلا يمكن استدعاؤه.",
        explain_q="لماذا ينجح السطر الأول ويفشل الثاني؟", explain='str = "DNA"\nprint(str)',
        explain_ans="يطبع DNA بلا خطأ، لأن التخزين نفسه مسموح. لكن أي استخدام لاحق لـ str() لتحويل رقم إلى نص سيفشل.",
        write="خزّن قائمة الأعمار [34, 52] في متغير باسم لا يطمس أي دالة مدمجة، ثم اطبع أكبرها باستخدام max.",
        write_ans="ages = [34, 52]\nprint(max(ages))",
        fix="max = 100\nprint(max([3, 7]))", fix_err="TypeError",
        fix_ans="max_score = 100\nprint(max([3, 7]))",
        fix_why="غيّر اسم المتغير إلى اسم وصفي مثل max_score.",
        bonus="لمعرفة أسماء كل الدوال المدمجة اكتب: print(dir(__builtins__)).",
    ),
    dict(
        key="snake_case للمتغيرات والدوال", group="style", level="تدرسها الآن",
        real="الكلمات المكتوبة على الأرض متصلة بخط سفلي مثل أفعى تزحف: patient_age.",
        what="تُكتب أسماء المتغيرات والدوال بحروف صغيرة، وتُفصل الكلمات بشرطة سفلية _.",
        name="snake_case تعني «أسلوب الأفعى» لأن الشرطات السفلية تجعل الاسم ممتداً على الأرض مثل الأفعى، وهي مناسبة للغة اسمها بايثون (نوع من الثعابين).",
        why="هي الاتفاقية الرسمية في PEP 8؛ الكود المكتوب بها يقرؤه كل مبرمجي بايثون في العالم بسهولة.",
        goal="توحيد شكل الأسماء في كل المشاريع.",
        syntax="calculate_bmi   ✓\nCalculateBMI    ✗ (للأصناف فقط)",
        good=C("""
            def calculate_bmi(weight, height):
                return weight / height ** 2

            print(round(calculate_bmi(70, 1.75), 1))
        """), good_out="22.9",
        bad="def CalculateBMI(weight, height):\n    return weight / height ** 2\n\nprint(round(CalculateBMI(70, 1.75), 1))", bad_err="مخالفة أسلوب",
        bad_why="الكود يعمل ويطبع 22.9، لكن الاسم يوحي بأنه صنف (class) لا دالة، فيربك القارئ.",
        bad_out="22.9",
        explain_q="أي الأسماء الثلاثة يتبع snake_case؟", explain="gc_percent = 52\ngcPercent = 52\nGCPercent = 52\nprint(gc_percent)",
        explain_ans="gc_percent فقط. أما gcPercent فهو camelCase، و GCPercent أقرب إلى PascalCase. الكود يطبع 52.",
        write="سمِّ متغيراً يخزن «عدد زيارات المريض» بأسلوب snake_case وأعطه القيمة 4.",
        write_ans="patient_visit_count = 4\nprint(patient_visit_count)",
        fix="bloodPressure = 120\nprint(bloodPressure)", fix_err="مخالفة أسلوب",
        fix_ans="blood_pressure = 120\nprint(blood_pressure)",
        fix_why="الكود يعمل، لكن بايثون تعتمد snake_case لا camelCase.",
        bonus="أداة مثل flake8 أو pylint تفحص الكود تلقائياً وتنبهك إلى أي اسم يخالف PEP 8.",
    ),
    dict(
        key="PascalCase لأسماء الأصناف", group="style", level="تعرّف عليها الآن، وتدرسها بعمق في الوحدة 12 (البرمجة الكائنية)",
        real="أسماء الشركات تُكتب بحروف كبيرة في بداية كل كلمة: «PlayStation» و «YouTube».",
        what="أسماء الأصناف (classes) تبدأ كل كلمة فيها بحرف كبير، دون شرطات: PatientRecord.",
        name="سُمّيت PascalCase نسبة إلى لغة البرمجة القديمة Pascal التي اشتهرت بهذا الأسلوب.",
        why="تميّز الأصناف عن الدوال من النظرة الأولى: Patient() تصنع كائناً، أما patient() فدالة عادية.",
        goal="تمييز نوع الاسم من شكله.",
        syntax="class PatientRecord:   ✓\nclass patient_record:  ✗",
        good=C("""
            class PatientRecord:
                pass

            print(PatientRecord.__name__)
        """), good_out="PatientRecord",
        bad="class patient_record:\n    pass", bad_err="مخالفة أسلوب",
        bad_why="يعمل، لكن من يقرأ patient_record() سيظنها دالة عادية لا صنفاً.",
        explain_q="أي سطر يُنشئ كائناً، وأيّها يستدعي دالة؟ (حسب الاتفاقية فقط)", explain="def lab_test():\n    return 5\n\nclass LabTest:\n    pass\n\nprint(lab_test(), LabTest.__name__)",
        explain_ans="LabTest صنف (PascalCase)، و lab_test دالة (snake_case). الكود يطبع: 5 LabTest.",
        write="اكتب سطر تعريف صنف يمثل «نتيجة تحليل مخبري» بأسلوب PascalCase.",
        write_ans="class LabResult:\n    pass",
        fix="class dna_sequence:\n    pass", fix_err="مخالفة أسلوب",
        fix_ans="class DnaSequence:\n    pass",
        fix_why="اسم الصنف يُكتب PascalCase.",
        bonus="الاختصارات داخل PascalCase تُكتب عادة بحرف كبير أول فقط: HttpRequest أوضح من HTTPRequest، و DnaSequence من DNASequence (كلاهما مقبول).",
    ),
    dict(
        key="UPPER_CASE للثوابت", group="style", level="تدرسها الآن",
        real="لافتات الطوارئ تُكتب بحروف كبيرة بارزة (EXIT) لأنها قيم ثابتة مهمة لا تتغير.",
        what="القيم الثابتة التي لا تتغير في البرنامج تُكتب أسماؤها بحروف كبيرة مع _ مثل MAX_HEART_RATE.",
        name="UPPER_CASE تعني «الحروف الكبيرة»؛ وتسمى هذه القيم «ثوابت» (Constants) لأنها لا تتغير.",
        why="تنبّه القارئ: «لا تغيّر هذه القيمة». بايثون لا تمنع التغيير، لكن الاتفاقية تحمي من الخطأ.",
        goal="تمييز القيم الثابتة مثل الحدود الطبية والمعاملات العلمية.",
        syntax="MAX_HEART_RATE = 220\nNORMAL_TEMP = 37.0",
        good=C("""
            MAX_HEART_RATE = 220
            age = 20
            print(MAX_HEART_RATE - age)
        """), good_out="200",
        bad="maxheartrate = 220\nprint(maxheartrate - 20)", bad_err="مخالفة أسلوب",
        bad_why="يعمل ويطبع 200، لكن الاسم لا يوضح أنها قيمة ثابتة، ويصعب قراءة الكلمات الملتصقة.",
        bad_out="200",
        explain_q="ماذا يطبع هذا الكود؟ وما الذي يخبرك به اسم المتغير الأول؟", explain="BMI_NORMAL_MAX = 25\nbmi = 27\nprint(bmi > BMI_NORMAL_MAX)",
        explain_ans="يطبع True. والاسم المكتوب بحروف كبيرة يخبرك أنه حد ثابت لا يجب تعديله.",
        write="عرّف ثابتاً يخزن عدد أيام الأسبوع (7) بالأسلوب الصحيح.",
        write_ans="DAYS_PER_WEEK = 7\nprint(DAYS_PER_WEEK)",
        fix="normal_temp = 37.0  # قيمة ثابتة لا تتغير", fix_err="مخالفة أسلوب",
        fix_ans="NORMAL_TEMP = 37.0",
        fix_why="بما أنها قيمة ثابتة، اكتب اسمها بحروف كبيرة.",
        bonus="تُكتب الثوابت عادة في أعلى الملف، مباشرة بعد أسطر import، لتسهل رؤيتها وتعديلها عند الحاجة.",
    ),
    dict(
        key="أسماء وصفية ذات معنى", group="style", level="تدرسها الآن",
        real="لو كُتب على كل صناديق البيت «صندوق 1» و«صندوق 2»، فستضطر لفتحها كلها للبحث عن الشاحن.",
        what="الاسم يجب أن يصف ما بداخله: gc_percent أفضل بكثير من x1.",
        name="«وصفي» لأن الاسم يصف المحتوى ويشرحه دون حاجة إلى تعليق.",
        why="الكود يُقرأ أكثر مما يُكتب؛ ستعود إليه بعد شهر ولن تتذكر ماذا كان x1.",
        goal="جعل الكود يشرح نفسه.",
        syntax="gc_percent = 48.5   ✓\nx1 = 48.5           ✗",
        good=C("""
            weight_kg = 70
            height_m = 1.75
            bmi = weight_kg / height_m ** 2
            print(round(bmi, 1))
        """), good_out="22.9",
        bad="a = 70\nb = 1.75\nc = a / b ** 2\nprint(round(c, 1))", bad_err="مخالفة أسلوب",
        bad_why="النتيجة صحيحة (22.9) لكن لا أحد يعرف ماذا تمثل a و b و c دون تخمين.",
        bad_out="22.9",
        explain_q="ماذا يحسب هذا الكود؟ حاول التخمين من الأسماء فقط.", explain="total_bases = 10\ngc_bases = 4\ngc_percent = gc_bases / total_bases * 100\nprint(gc_percent)",
        explain_ans="يحسب نسبة GC في تسلسل طوله 10 قواعد منها 4 من نوع G أو C، ويطبع 40.0. الأسماء كشفت المعنى دون أي شرح.",
        write="أعد تسمية المتغيرين: t = 38.2 و f = t > 37.5 بأسماء وصفية.",
        write_ans="temperature = 38.2\nhas_fever = temperature > 37.5\nprint(has_fever)",
        fix="d = 500\nw = 20\nprint(d / w)", fix_err="مخالفة أسلوب",
        fix_ans="dose_mg = 500\nweight_kg = 20\nprint(dose_mg / weight_kg)",
        fix_why="أسماء من حرف واحد لا تقول شيئاً؛ أضف الوحدة إلى الاسم أيضاً (mg، kg) لتجنب أخطاء الجرعات.",
        bonus="إضافة وحدة القياس إلى الاسم (weight_kg، height_m) عادة ممتازة في البرامج الطبية، لأن الخلط بين الكيلوغرام والرطل قد يكون خطيراً.",
    ),
    dict(
        key="أسماء المتغيرات المنطقية تبدأ بـ is_ / has_", group="style", level="تدرسها الآن",
        real="في استمارة المريض أسئلة جوابها «نعم/لا»: «هل أنت مدخن؟»، «هل لديك حساسية؟».",
        what="المتغير الذي يخزن True أو False يُفضّل أن يبدأ اسمه بـ is_ أو has_ مثل is_smoker.",
        name="is تعني «هل هو»، و has تعني «هل لديه»؛ فيُقرأ الاسم كسؤال جوابه نعم أو لا.",
        why="يجعل الشروط مقروءة كجملة: if is_smoker: «إذا كان مدخناً».",
        goal="توضيح أن المتغير قيمة منطقية.",
        syntax="is_diabetic = True\nhas_allergy = False",
        good=C("""
            is_smoker = False
            if not is_smoker:
                print("غير مدخن")
        """), good_out="غير مدخن",
        bad='smoker = "no"\nif smoker:\n    print("مدخن")', bad_err="خطأ منطقي",
        bad_why="يطبع «مدخن» رغم أن القيمة no! لأن أي نص غير فارغ يُعامل True. استخدم True/False واسماً يبدأ بـ is_.",
        bad_out="مدخن",
        explain_q="اقرأ الشرط بصوت عالٍ كجملة عربية. ماذا يطبع؟", explain='has_allergy = True\nif has_allergy:\n    print("انتبه للأدوية")',
        explain_ans="«إذا كان لديه حساسية: انتبه للأدوية». يطبع «انتبه للأدوية».",
        write="أنشئ متغيراً منطقياً يعبّر عن «هل المريض منوّم في المستشفى» وأعطه القيمة True.",
        write_ans="is_admitted = True\nprint(is_admitted)",
        fix='pregnant = "yes"\nif pregnant == True:\n    print("حامل")', fix_err="خطأ منطقي",
        fix_out="",
        fix_ans='is_pregnant = True\nif is_pregnant:\n    print("حامل")',
        fix_why="لا يطبع شيئاً لأن النص \"yes\" لا يساوي True. خزّن قيمة منطقية حقيقية، ولا داعي لكتابة == True.",
        bonus="كتابة if is_valid == True زائدة عن الحاجة؛ يكفي if is_valid.",
    ),
    dict(
        key="تجنب الأحرف المربكة l و O و I منفردة", group="style", level="تدرسها الآن",
        real="في بعض الخطوط يصعب التمييز بين حرف O والرقم 0، وبين الحرف l والرقم 1، كما يحدث عند قراءة رمز تفعيل.",
        what="لا تستخدم الأحرف l (إل صغيرة) و O (أو كبيرة) و I (آي كبيرة) أسماءً منفردة.",
        name="تسمى «الأحرف المربكة» لأنها تشبه الأرقام 1 و 0 في كثير من الخطوط.",
        why="قد تقرأ l = 1 على أنها 1 = 1، فتخطئ في فهم الكود.",
        goal="منع الالتباس البصري.",
        syntax="length = 1   ✓\nl = 1        ✗",
        good=C("""
            length = 10
            print(length * 2)
        """), good_out="20",
        bad="l = 1\nO = 0\nprint(l + O)", bad_err="مخالفة أسلوب",
        bad_why="يعمل ويطبع 1، لكن السطر الأخير يبدو كأنه print(1 + 0)، وهذا مربك.",
        bad_out="1",
        explain_q="ماذا يطبع هذا الكود؟ (اقرأه بتمعّن)", explain="I = 10\nl = 1\nprint(I - l)",
        explain_ans="يطبع 9. وقد تكون احتجت لحظة للتمييز بين I و l؛ هذا بالضبط سبب القاعدة.",
        write="أعد كتابة السطر O = 5 باسم واضح يمثل «عدد الملاحظات».",
        write_ans="observations = 5\nprint(observations)",
        fix="I = 3\nprint(I)", fix_err="مخالفة أسلوب",
        fix_ans="index = 3\nprint(index)",
        fix_why="استبدل الحرف المربك باسم كامل.",
        bonus="خطوط البرمجة مثل Fira Code مصممة لتمييز هذه الأحرف بوضوح، لذلك يستخدمها المبرمجون في المحررات.",
    ),
    dict(
        key="أسماء الملفات والوحدات بحروف صغيرة", group="style", level="تعرّف عليها الآن، وتدرسها بعمق في الوحدة 13 (الوحدات والمكتبات)",
        real="عندما ترسل ملفاً لزميلك على نظام تشغيل مختلف، قد يفشل فتح ملف اسمه «تقرير نهائي (2).docx» بسبب المسافات والأقواس.",
        what="أسماء ملفات بايثون (.py) تكون بحروف صغيرة وشرطة سفلية، دون مسافات: dna_tools.py.",
        name="تسمى «وحدات» (modules) لأن كل ملف .py يمكن استيراده كوحدة في برنامج آخر.",
        why="اسم الملف يصبح اسماً في الكود عند import؛ فإن احتوى مسافة أو شرطة لن تستطيع استيراده.",
        goal="تمكين استيراد الملفات في برامج أخرى.",
        syntax="dna_tools.py    ✓\nDNA Tools.py    ✗\ndna-tools.py    ✗",
        good=C("""
            module_name = "dna_tools"
            print(module_name.isidentifier())
        """), good_out="True",
        bad='module_name = "dna-tools"\nprint(module_name.isidentifier())', bad_err="خطأ منطقي",
        bad_why="يطبع False: الاسم dna-tools لا يصلح اسماً في بايثون، فلن تستطيع كتابة import dna-tools.",
        bad_out="False",
        explain_q="ماذا تفعل الدالة isidentifier؟ وماذا يطبع الكود؟", explain='print("patient_utils".isidentifier(), "patient utils".isidentifier())',
        explain_ans="تفحص هل النص يصلح اسماً في بايثون. يطبع True False لأن الثاني فيه مسافة.",
        write="اقترح اسم ملف لبرنامج يحسب مؤشر كتلة الجسم.",
        write_ans='file_name = "bmi_calculator.py"\nprint(file_name)',
        fix='print("Lab-Results".isidentifier())', fix_err="خطأ منطقي",
        fix_out="False",
        fix_ans='print("lab_results".isidentifier())',
        fix_why="الشرطة والحرف الكبير غير مناسبين؛ الاسم الصحيح lab_results.",
        bonus="لا تسمِّ ملفك باسم مكتبة موجودة مثل random.py أو math.py، وإلا استوردت بايثون ملفك بدلاً من المكتبة الحقيقية.",
    ),
    dict(
        key="يفضل استخدام أسماء إنجليزية", group="style", level="تدرسها الآن",
        real="لغة الطيران العالمية هي الإنجليزية، حتى يفهم الطيار أي برج مراقبة في العالم. والبرمجة كذلك.",
        what="بايثون تقبل الأسماء العربية، لكن الاتفاق أن تُكتب الأسماء بالإنجليزية.",
        name="تسمى أحياناً «معرّفات ASCII» لأن الحروف الإنجليزية جزء من جدول ASCII القديم الذي تدعمه كل الأنظمة.",
        why="الكود سيقرؤه زملاء ومراجعون من بلدان مختلفة، والمكتبات كلها بالإنجليزية، ولوحة المفاتيح تحتاج تبديل اللغة باستمرار.",
        goal="كود قابل للمشاركة عالمياً.",
        syntax="patient_age = 30    ✓ (مفضّل)\nعمر_المريض = 30     ✓ (يعمل لكنه غير مستحسن)",
        good=C("""
            patient_age = 30
            print(patient_age)
        """), good_out="30",
        bad="عمر_المريض = 30\nprint(عمر_المريض)", bad_err="مخالفة أسلوب",
        bad_why="يعمل ويطبع 30، لكن الخلط بين العربية والإنجليزية في السطر نفسه يربك اتجاه الكتابة ويصعّب التعاون.",
        bad_out="30",
        explain_q="هل هذا الكود يعمل؟ ماذا يطبع؟", explain='الاسم = "سارة"\nprint(الاسم)',
        explain_ans="نعم يعمل ويطبع «سارة». بايثون 3 تدعم Unicode في الأسماء، لكن هذا لا يعني أنه أسلوب جيد.",
        write="ترجم اسم المتغير ضغط_الدم إلى اسم إنجليزي صحيح وأعطه القيمة 120.",
        write_ans="blood_pressure = 120\nprint(blood_pressure)",
        fix="درجة_الحرارة = 37\nprint(درجة_الحرارة)", fix_err="مخالفة أسلوب",
        fix_ans="temperature = 37\nprint(temperature)",
        fix_why="استخدم اسماً إنجليزياً؛ أما النصوص المعروضة للمستخدم (داخل علامات التنصيص) فتبقى بالعربية بلا مشكلة.",
        bonus="القاعدة الذهبية: الأسماء بالإنجليزية، والتعليقات والرسائل للمستخدم بالعربية كما يناسب جمهورك.",
    ),
    # ==================== أسماء خاصة ====================
    dict(
        key="_ لمتغير لا نحتاج قيمته", group="special", level="تدرسها الآن",
        real="تأخذ ثلاث حبات دواء يومياً، ولا يهمك ترتيب الحبة (الأولى أم الثانية)؛ المهم أن تأخذها ثلاث مرات.",
        what="الشرطة السفلية وحدها _ اسم متغير يعني «لا أحتاج هذه القيمة».",
        name="تسمى «المتغير المهمل» (Throwaway variable) لأن قيمته تُرمى ولا تُستخدم.",
        why="توضح للقارئ أن الحلقة تتكرر عدداً من المرات فقط، دون الحاجة إلى رقم الدورة.",
        goal="التكرار دون متغير لا معنى له.",
        syntax="for _ in range(3):",
        good=C("""
            for _ in range(3):
                print("قياس الضغط")
        """), good_out="قياس الضغط\nقياس الضغط\nقياس الضغط",
        bad='for i in range(2):\n    print("قياس")', bad_err="مخالفة أسلوب",
        bad_why="يعمل، لكن i معرّف ولم يُستخدم، فيتساءل القارئ: أين يُستخدم i؟",
        bad_out="قياس\nقياس",
        explain_q="ماذا يطبع هذا الكود؟", explain='name, _ = ("Ali", 52)\nprint(name)',
        explain_ans="يطبع Ali. القيمة الثانية (52) وُضعت في _ لأننا لا نحتاجها.",
        write="اطبع كلمة «تمرين» أربع مرات باستخدام _ في الحلقة.",
        write_ans='for _ in range(4):\n    print("تمرين")',
        fix='for counter in range(2):\n    print("جرعة")', fix_err="مخالفة أسلوب",
        fix_ans='for _ in range(2):\n    print("جرعة")',
        fix_why="counter لا يُستخدم داخل الحلقة؛ استبدله بـ _.",
        bonus="في الطرفية التفاعلية (Python Shell) تحفظ _ ناتج آخر عملية حسابية تلقائياً.",
    ),
    dict(
        key="بادئة _ واحدة = استخدام داخلي", group="special", level="تعرّف عليها الآن، وتدرسها بعمق في الوحدة 12 (البرمجة الكائنية)",
        real="باب في المستشفى مكتوب عليه «للموظفين فقط». الباب غير مقفل، لكنه رسالة واضحة: هذا ليس لك.",
        what="الاسم الذي يبدأ بشرطة سفلية واحدة (_cache) يعني «هذا للاستخدام الداخلي، لا تستخدمه من الخارج».",
        name="تسمى «الاستخدام الداخلي» (Internal use) لأنها تخص داخل الصنف أو الملف.",
        why="تحمي الأجزاء الداخلية من العبث، وتخبر المستخدمين بما يمكنهم الاعتماد عليه.",
        goal="فصل الأجزاء الداخلية عن الواجهة العامة.",
        syntax="self._cache = {}",
        good=C("""
            class Lab:
                def __init__(self):
                    self._raw = [5.1, 6.3]
                def average(self):
                    return round(sum(self._raw) / len(self._raw), 2)

            print(Lab().average())
        """), good_out="5.7",
        bad="class Lab:\n    def __init__(self):\n        self._raw = [5.1]\n\nlab = Lab()\nlab._raw.append(999)\nprint(lab._raw)", bad_err="مخالفة أسلوب",
        bad_why="يعمل، لكنك عدّلت بيانات داخلية من خارج الصنف، فأفسدت القراءات.",
        bad_out="[5.1, 999]",
        explain_q="ماذا يطبع هذا الكود؟", explain="_secret = 42\nprint(_secret)",
        explain_ans="يطبع 42. الشرطة لا تمنع الوصول؛ هي مجرد اتفاقية بين المبرمجين.",
        write="عرّف متغيراً داخلياً يخزن عدد المحاولات (0) بالأسلوب الصحيح.",
        write_ans="_attempts = 0\nprint(_attempts)",
        fix="class Device:\n    def __init__(self):\n        self.calibration = 1.02  # قيمة داخلية لا يغيّرها المستخدم", fix_err="مخالفة أسلوب",
        fix_ans="class Device:\n    def __init__(self):\n        self._calibration = 1.02",
        fix_why="بما أنها قيمة داخلية، أضف _ في بدايتها.",
        bonus="عند تنفيذ from module import * لا تُستورد الأسماء التي تبدأ بـ _.",
    ),
    dict(
        key="بادئتان __ = تشويه الاسم (name mangling)", group="special", level="تعرّف عليها الآن، وتدرسها بعمق في الوحدة 12 (البرمجة الكائنية)",
        real="ملف المريض السري في خزانة مقفلة باسم مرمّز؛ لا يكفي أن تعرف اسم المريض لتصل إليه.",
        what="الاسم الذي يبدأ بشرطتين (__national_id) داخل صنف تغيّر بايثون اسمه داخلياً حتى يصعب الوصول إليه من الخارج.",
        name="«تشويه الاسم» (Name mangling) لأن بايثون تحوّل __id إلى _Patient__id، أي «تشوّه» الاسم الأصلي.",
        why="تحمي البيانات الحساسة من التعديل العرضي، وتمنع تصادم الأسماء عند الوراثة.",
        goal="حماية أقوى من الشرطة الواحدة.",
        syntax="self.__national_id = nid",
        good=C("""
            class Patient:
                def __init__(self, nid):
                    self.__nid = nid
                def masked(self):
                    return "****" + self.__nid[-3:]

            print(Patient("9901234567").masked())
        """), good_out="****567",
        bad='class Patient:\n    def __init__(self):\n        self.__nid = "123"\n\nprint(Patient().__nid)', bad_err="AttributeError",
        bad_why="من خارج الصنف لا يوجد اسم __nid، لأن بايثون غيّرته إلى _Patient__nid.",
        explain_q="ماذا يطبع هذا الكود؟", explain='class A:\n    def __init__(self):\n        self.__x = 1\n\nprint(A()._A__x)',
        explain_ans="يطبع 1. هذا هو الاسم بعد التشويه؛ الحماية إذن ليست سرية مطلقة بل منع للعبث العرضي.",
        write="عرّف صنفاً Account فيه خاصية محمية بشرطتين اسمها __balance قيمتها 0.",
        write_ans="class Account:\n    def __init__(self):\n        self.__balance = 0\n\nprint(Account()._Account__balance)",
        fix='class Patient:\n    def __init__(self):\n        self.__pin = "1234"\n\np = Patient()\nprint(p.__pin)', fix_err="AttributeError",
        fix_ans='class Patient:\n    def __init__(self):\n        self.__pin = "1234"\n    def has_pin(self):\n        return len(self.__pin) == 4\n\np = Patient()\nprint(p.has_pin())',
        fix_why="لا تصل إلى الخاصية المحمية من الخارج؛ أضف تابعاً داخل الصنف يقدم ما تحتاجه فقط.",
        bonus="لا تستخدم __ إلا عند الحاجة الحقيقية؛ أغلب المبرمجين يكتفون بشرطة واحدة.",
    ),
    dict(
        key="__dunder__ محجوزة للغة", group="special", level="تعرّف عليها الآن، وتدرسها بعمق في الوحدة 12 (البرمجة الكائنية)",
        real="أرقام الطوارئ مثل 911 أو 112 محجوزة للدولة؛ لا يمكنك أن تحجز رقماً بهذا الشكل لنفسك.",
        what="الأسماء المحاطة بشرطتين من الجهتين مثل __init__ و __name__ لها معانٍ خاصة في بايثون.",
        name="dunder اختصار double underscore أي «شرطتان سفليتان مزدوجتان». وتسمى أيضاً «التوابع السحرية» (magic methods).",
        why="بايثون تستدعيها تلقائياً في مواقف معينة (عند إنشاء كائن، عند الطباعة...)؛ واختراع أسماء بهذا الشكل قد يتصادم مع إصدار مستقبلي.",
        goal="ترك هذا الشكل من الأسماء للغة وحدها.",
        syntax="def __init__(self):   ✓ (اسم تعرّفه بايثون)\ndef __calc__(self):   ✗ (اسم مخترع)",
        good=C("""
            class Patient:
                def __init__(self, name):
                    self.name = name
                def __str__(self):
                    return "المريض: " + self.name

            print(Patient("Sara"))
        """), good_out="المريض: Sara",
        bad="class Patient:\n    def __calc_bmi__(self):\n        return 22\n\nprint(Patient().__calc_bmi__())", bad_err="مخالفة أسلوب",
        bad_why="يعمل ويطبع 22، لكنك اخترعت اسماً بشكل dunder، وهذا محجوز لبايثون.",
        bad_out="22",
        explain_q="ماذا يطبع هذا الكود إذا شغّلته مباشرة؟", explain="print(__name__)",
        explain_ans="يطبع __main__، وهو اسم dunder تضعه بايثون تلقائياً للملف الذي يتم تشغيله.",
        write="اكتب الصنف Course بتابع __init__ يستقبل اسم المقرر ويخزنه.",
        write_ans='class Course:\n    def __init__(self, title):\n        self.title = title\n\nprint(Course("Python").title)',
        fix="class Dna:\n    def __gc__(self):\n        return 50", fix_err="مخالفة أسلوب",
        fix_ans="class Dna:\n    def gc_content(self):\n        return 50",
        fix_why="سمِّ توابعك أسماء عادية بأسلوب snake_case.",
        bonus="من أشهر توابع dunder: __init__ (الإنشاء)، و __str__ (الطباعة)، و __len__ (تجعل len تعمل على كائنك).",
    ),
]
