# چک‌لیست انتشار نسخهٔ ۱.۲

## ۱. انتقال و Commit

- تمام فایل‌های بسته را روی پوشهٔ مخزن کپی کنید.
- در GitHub Desktop تغییرات را بررسی کنید.
- `.env`، `.venv`، `dist` و `build` نباید در Changes باشند.
- Commit پیشنهادی:

```text
Add Render deployment, Windows edition, and OSM service safeguards
```

- `Push origin` را بزنید.

## ۲. کنترل GitHub Actions

- Workflow با نام `CI` باید سبز شود.
- Workflow `Deploy GitHub Pages` باید سبز بماند.
- Workflow `Build Windows Edition` فقط دستی یا هنگام انتشار Release اجرا می‌شود.

## ۳. ایجاد Web App در Render

آدرس زیر را باز کنید:

```text
https://render.com/deploy?repo=https://github.com/FaramarzKowsari/geo-business-intelligence-studio
```

پس از ساخت سرویس:

- `/api/health` را باز کنید.
- جست‌وجوی Sample را آزمایش کنید.
- سپس یک جست‌وجوی محدود OpenStreetMap انجام دهید.
- URL نهایی Render را یادداشت کنید تا در README و GitHub Pages به دکمهٔ Live App افزوده شود.

## ۴. ساخت نسخهٔ Windows

```text
Actions → Build Windows Edition → Run workflow
```

Artifact را دانلود و EXE را روی یک سیستم ویندوز آزمایش کنید. پنجرهٔ کنترل کوچک باید باز شود و مرورگر را اجرا کند. بستن پنجره با دکمهٔ Stop application سرور محلی را متوقف می‌کند.

## ۵. ساخت Release و DOI

- در صورت تمایل، ابتدا Windows Artifact را آزمایش کنید.
- یک GitHub Release با Tag مناسب، مانند `v1.2.0`، منتشر کنید.
- Workflow ویندوز، EXE و SHA-256 را به Release متصل می‌کند.
- اگر اتصال Zenodo فعال باشد، Zenodo نسخه را آرشیو و DOI واقعی صادر می‌کند.
- فقط پس از صدور DOI، Badge و Citation را با شناسهٔ واقعی به‌روزرسانی کنید.
