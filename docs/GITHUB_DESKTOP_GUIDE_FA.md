# راهنمای انتقال پروژه با GitHub Desktop

## ۱. ساخت مخزن در GitHub

در حساب GitHub خود وارد شوید و یک مخزن جدید بسازید:

- Repository name: `geo-business-intelligence-studio`
- Visibility: Public
- گزینه‌های ساخت README، `.gitignore` و License را فعال نکنید؛ این فایل‌ها از قبل در پروژه وجود دارند.

پس از ساخت مخزن، صفحهٔ خالی مخزن را باز نگه دارید.

## ۲. افزودن پوشه به GitHub Desktop

1. فایل ZIP پروژه را Extract کنید.
2. GitHub Desktop را باز کنید.
3. از منوی `File` گزینهٔ `Add local repository` را انتخاب کنید.
4. پوشهٔ اصلی `geo-business-intelligence-studio` را انتخاب کنید.
5. اگر برنامه گفت این پوشه هنوز Git Repository نیست، گزینهٔ `create a repository` را بزنید.
6. در قسمت Name همان `geo-business-intelligence-studio` را بنویسید.
7. Git ignore و License جدید انتخاب نکنید، چون فایل‌های آماده داخل پروژه هستند.

## ۳. اولین Commit

در ستون Changes باید فایل‌های پروژه دیده شوند.

در کادر Summary بنویسید:

```text
Initial release: GeoBusiness Intelligence Studio
```

سپس `Commit to main` را بزنید.

## ۴. اتصال به مخزن آنلاین

دو روش وجود دارد:

### روش ساده

در GitHub Desktop دکمهٔ `Publish repository` را بزنید، نام را بررسی کنید و گزینهٔ `Keep this code private` را خاموش کنید.

### اتصال به مخزنی که قبلاً در سایت ساخته‌اید

از منوی `Repository` وارد `Repository settings` شوید و Remote را به آدرس مخزن خود تنظیم کنید:

```text
https://github.com/FaramarzKowsari/geo-business-intelligence-studio.git
```

سپس `Push origin` را بزنید.

## ۵. اجرای محلی در ویندوز

PowerShell را داخل پوشهٔ پروژه باز کنید:

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

سپس مرورگر را روی این آدرس باز کنید:

```text
http://127.0.0.1:8000
```

ابتدا Provider را روی `Sample data` نگه دارید تا بدون اینترنت و بدون کلید API پروژه را آزمایش کنید.

## ۶. نکتهٔ امنیتی

فایل `.env` را هیچ‌وقت Commit نکنید. این فایل در `.gitignore` قرار گرفته است. فقط `.env.example` باید در مخزن باشد.

## ۷. پیشنهادهای صفحهٔ مخزن

در بخش About این متن را قرار دهید:

```text
Privacy-aware local business discovery, geospatial intelligence, data-quality scoring, optional BYOK AI, FastAPI, OpenStreetMap and official Google Places integration.
```

Topics پیشنهادی:

```text
fastapi
python
openstreetmap
geospatial
data-engineering
business-intelligence
artificial-intelligence
ollama
google-places-api
portfolio-project
```
