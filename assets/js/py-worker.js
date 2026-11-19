/* ============================================================
   py-worker.js — يعمل في خيط منفصل: يحمّل Pyodide ويشغّل الكود.
   الرسائل الواردة: {id, code, stdin}
   الرسائل الصادرة: ready | load-error | started {id} | result {id, out, err, errName, figs}
   ============================================================ */
/* global loadPyodide */
const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
let py = null;

// كود بايثون مساعد: يلتقط المخرجات والأخطاء ويحفظ رسوم matplotlib كصور
const HELPER = `
import sys, io, os, tempfile, traceback, base64, importlib.util
os.environ["MPLBACKEND"] = "Agg"

# أسماء الاستيراد التي يختلف اسم حزمتها في pip
PIP_NAME = {"sklearn": "scikit-learn", "Bio": "biopython", "PIL": "pillow", "yaml": "pyyaml"}

async def ensure_packages(code):
    from pyodide.code import find_imports
    try:
        import micropip
    except ImportError:
        return          # بدون micropip نكتفي بالمكتبات المدمجة في Pyodide
    for name in find_imports(code):
        top = name.split(".")[0]
        if importlib.util.find_spec(top) is None:
            try:
                await micropip.install(PIP_NAME.get(top, top))
            except Exception:
                pass   # سيظهر ModuleNotFoundError طبيعياً عند التشغيل

def _reset_state():
    """إزالة آثار التشغيل السابق التي تبقى في المفسر نفسه (لا تحدث عند تشغيل ملف جديد في الحاسوب)."""
    if "logging" in sys.modules:
        import logging
        root = logging.getLogger()
        for h in root.handlers[:]:
            h.close()
            root.removeHandler(h)
        root.setLevel(logging.WARNING)


async def _sleep(delay, result=None):
    import time
    time.sleep(delay)          # داخل Worker يجوز الانتظار المتزامن
    return result


def _browser_asyncio_run(main, *, debug=None):
    """
    المتصفح يشغّل حلقة أحداث دائمة، فلا يعمل asyncio.run كما في الحاسوب.
    هذا البديل يقود الـ coroutine خطوة خطوة، وهو كافٍ لأمثلة الدروس (await و asyncio.sleep).
    """
    try:
        while True:
            fut = main.send(None)
            if fut is not None:
                main.close()
                raise RuntimeError("هذا المثال يحتاج حلقة أحداث كاملة (مثل asyncio.gather)؛ شغّله على حاسوبك.")
    except StopIteration as e:
        return e.value


def run_user(code, stdin, files=None):
    import asyncio
    out, err = io.StringIO(), io.StringIO()
    old = sys.stdout, sys.stderr, sys.stdin
    old_async = asyncio.run, asyncio.sleep
    _reset_state()
    work = tempfile.mkdtemp()
    os.chdir(work)                          # مجلد جديد لكل تشغيل
    for fname, content in (files or {}).items():   # ملفات تجريبية يحتاجها التمرين
        with open(fname, "w", encoding="utf-8") as fh:
            fh.write(content)
    sys.path.insert(0, work)                # كما في الحاسوب: مجلد الملف ضمن مسار الاستيراد
    importlib.invalidate_caches()
    sys.stdout, sys.stderr, sys.stdin = out, err, io.StringIO(stdin)
    asyncio.run, asyncio.sleep = _browser_asyncio_run, _sleep
    os.environ["PYTHONBREAKPOINT"] = "0"
    name = ""
    try:
        exec(compile(code, "<الكود>", "exec"), {"__name__": "__main__"})
    except SystemExit as e:
        if e.code not in (None, 0):
            print(e.code, file=err)
            name = "SystemExit"
    except BaseException as e:
        name = type(e).__name__
        tb = e.__traceback__.tb_next if e.__traceback__ else None   # إخفاء سطر exec الداخلي
        traceback.print_exception(type(e), e, tb, file=err)
    finally:
        sys.stdout, sys.stderr, sys.stdin = old
        asyncio.run, asyncio.sleep = old_async
        if work in sys.path:
            sys.path.remove(work)
        for mod_name, mod in list(sys.modules.items()):     # وحدات الطالب لا تبقى للتشغيل التالي
            f = getattr(mod, "__file__", None) or ""
            if f.startswith(work):
                del sys.modules[mod_name]
        _reset_state()
    figs = []
    if "matplotlib.pyplot" in sys.modules:
        plt = sys.modules["matplotlib.pyplot"]
        for n in plt.get_fignums():
            buf = io.BytesIO()
            plt.figure(n).savefig(buf, format="png", dpi=90, bbox_inches="tight")
            figs.append(base64.b64encode(buf.getvalue()).decode())
        plt.close("all")
    return out.getvalue()[:20000], err.getvalue()[-6000:], name, figs
`;

const boot = (async () => {
  try {
    importScripts(PYODIDE + "pyodide.js");
    py = await loadPyodide({ indexURL: PYODIDE });
    try { await py.loadPackage("micropip"); } catch (_) { /* اختياري: لتثبيت مكتبات إضافية مثل seaborn */ }
    py.runPython(HELPER);
    postMessage({ type: "ready" });
  } catch (e) {
    postMessage({ type: "load-error", msg: String(e) });
    throw e;
  }
})();

onmessage = async e => {
  const { id, code, stdin, files } = e.data;
  try {
    await boot;
    try { await py.loadPackagesFromImports(code); } catch (_) { /* نكمل بـ micropip */ }
    py.globals.set("_code", code);
    await py.runPythonAsync("await ensure_packages(_code)");
    postMessage({ type: "started", id });
    const fn = py.globals.get("run_user");
    const pyFiles = files ? py.toPy(files) : null;
    const res = fn(code, stdin, pyFiles);
    if (pyFiles) pyFiles.destroy();
    const [out, err, errName, figs] = res.toJs();
    res.destroy(); fn.destroy();
    postMessage({ type: "result", id, out, err, errName, figs: Array.from(figs) });
  } catch (ex) {
    postMessage({ type: "result", id, out: "", err: String(ex), errName: "InternalError", figs: [] });
  }
};
