# از اینجا شروع کنید

این پروژه آمادهٔ انتقال به GitHub Desktop است و برای اجرای اولیه به هیچ کلید API نیاز ندارد.

## اجرای فوری در ویندوز

در پوشهٔ پروژه PowerShell را باز کنید و دستورهای زیر را اجرا کنید:

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

سپس وارد این آدرس شوید:

```text
http://127.0.0.1:8000
```

Provider پیش‌فرض `Sample data` است و بدون اینترنت اجرا می‌شود.

برای انتقال به GitHub Desktop، راهنمای کامل زیر را بخوانید:

```text
docs/GITHUB_DESKTOP_GUIDE_FA.md
```

فایل `.env` شامل تنظیمات شخصی است و نباید وارد GitHub شود. فایل `.gitignore` از قبل جلوی Commit شدن آن را می‌گیرد.
