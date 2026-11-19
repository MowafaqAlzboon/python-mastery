# -*- coding: utf-8 -*-
"""
teacher_hash.py — يحسب بصمة كلمة مرور «وضع المدرس» لوضعها في assets/js/config.js (teacherHash).

التشغيل:
    python tools/teacher_hash.py "كلمة-المرور-الجديدة"
"""
import sys

SALT = "aau-camS-2026"   # نفس الملح الموجود في app.js


def fnv1a_base36(s):
    """نفس دالة hash() في app.js: FNV-1a بطول 32 بت، ثم تمثيل بالأساس 36."""
    h = 2166136261
    data = s.encode("utf-16-le")          # JavaScript يعمل على وحدات UTF-16؛ نحاكيه لتتطابق البصمة مع العربية
    for i in range(0, len(data), 2):
        h ^= int.from_bytes(data[i:i + 2], "little")
        h = (h * 16777619) & 0xFFFFFFFF
    digits, out = "0123456789abcdefghijklmnopqrstuvwxyz", ""
    while True:
        h, r = divmod(h, 36)
        out = digits[r] + out
        if h == 0:
            return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('الاستخدام: python tools/teacher_hash.py "كلمة-المرور"')
    print(f'teacherHash: "{fnv1a_base36(sys.argv[1] + SALT)}",')
