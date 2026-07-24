# راهنمای ارتقا به نسخهٔ ۱.۲

این بسته سه قابلیت اصلی را به مخزن اضافه می‌کند:

1. اجرای کامل تحت وب با Render؛
2. ساخت نسخهٔ مستقل ویندوز بدون نیاز به Python یا PowerShell برای کاربر نهایی؛
3. محافظت فنی از Nominatim و Overpass با کش، فاصلهٔ اجباری درخواست‌ها، ادغام درخواست‌های هم‌زمان و محدودیت کاربران عمومی.

## انتقال فایل‌ها

محتویات پوشهٔ این بسته را روی پوشهٔ فعلی مخزن کپی و فایل‌های هم‌نام را جایگزین کنید. فایل `.env` محلی خود را جایگزین نکنید؛ فقط `.env.example` باید وارد Git شود.

در GitHub Desktop، پیام Commit پیشنهادی:

```text
Add Render deployment, Windows edition, and OSM service safeguards
```

سپس `Push origin` را بزنید.

## کنترل CI

پس از Push، Workflow عادی CI باید سبز شود. تست محلی نسخهٔ بسته شامل ۱۳ تست موفق است.

## فعال‌کردن Render

پس از Push این نشانی را باز کنید:

```text
https://render.com/deploy?repo=https://github.com/FaramarzKowsari/geo-business-intelligence-studio
```

Render فایل `render.yaml` را می‌خواند و Web Service را ایجاد می‌کند. پس از ساخت سرویس، URL نهایی `onrender.com` را در README و صفحهٔ GitHub Pages به‌عنوان Live Application قرار دهید.

## ساخت Windows EXE

در GitHub:

```text
Actions → Build Windows Edition → Run workflow
```

پس از موفقیت Workflow، Artifact زیر را دانلود کنید:

```text
GeoBusiness-Intelligence-Studio-Windows
```

برای قرارگرفتن خودکار EXE در بخش Releases، یک GitHub Release منتشر کنید. Workflow در رویداد `release: published` فایل EXE و SHA-256 را می‌سازد و به همان Release متصل می‌کند.

## سیاست OpenStreetMap

مقادیر پیش‌فرض در `render.yaml` و `.env.example` برای استفادهٔ متوسط و کاربرمحور تنظیم شده‌اند. برای ترافیک مستمر، تجاری، چند نمونه‌ای یا چند Worker، باید از Nominatim/Overpass اختصاصی یا ارائه‌دهندهٔ ثالث و یک کش و Rate Limiter مشترک استفاده شود.
