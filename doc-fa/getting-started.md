# شروع کار

## CacheLab چیست؟

CacheLab یک پلتفرم وب تعاملی برای تست، بنچمارک و مانیتورینگ کتابخانه [recall-cache](https://pypi.org/project/recall-cache) است. این پلتفرم شامل:

- **داشبورد زنده** — آمار لحظه‌ای با WebSocket و چارت‌های تحلیلی
- **تست‌های Core** — ۷ تست تعاملی برای عملیات پایه کش
- **الگوهای پیشرفته** — ۲۰ الگوی پیشرفته کشینگ
- **بنچمارک** — مقایسه کامل عملکرد
- **پنل ادمین** — پنل داخلی recall با RBAC

## پیش‌نیازها

- Python 3.8+
- pip یا uv

## نصب

### ۱. کلون کردن

```bash
git clone https://github.com/sepehrhi/CacheLab.git
cd CacheLab
```

### ۲. محیط مجازی

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### ۳. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### ۴. اجرا

```bash
python app.py
```

### ۵. باز کردن در مرورگر

- **CacheLab**: http://localhost:5000
- **پنل ادمین**: http://localhost:8080 (Token: `cachelab-admin-2026`)

## تنظیمات

| متغیر | پیش‌فرض | توضیح |
|---|---|---|
| `SECRET_KEY` | `cachelab-secret-key-2026` | کلید مخفی Flask |
| `ADMIN_PORT` | `8080` | پورت پنل ادمین |
| `ADMIN_TOKEN` | `cachelab-admin-2026` | توکن ادمین |
| `MEMORY_MAXSIZE` | `1000` | حداکثر آیتم‌های حافظه |

## مشارکت

از مشارکت‌ها استقبال می‌شود! لطفاً issue یا PR باز کنید.

## لایسنس

MIT

---

**لینک‌های مفید:**
- 📦 [PyPI: recall-cache](https://pypi.org/project/recall-cache)
- 🐙 [GitHub: hermes-telegram/recall](https://github.com/hermes-telegram/recall)
