# استقرار

## محیط توسعه

```bash
python app.py
```

## محیط تولید (WSGI)

```bash
# Gunicorn + Eventlet
pip install gunicorn eventlet
gunicorn --worker-class eventlet -w 1 app:app -b 0.0.0.0:5000

# Waitress (ویندوز)
pip install waitress
waitress-serve --port=5000 app:app
```

## Docker

```bash
docker build -t cachelab .
docker run -p 5000:5000 -p 8080:8080 cachelab
```

## متغیرهای محیطی

| متغیر | پیش‌فرض | توضیح |
|---|---|---|
| `FLASK_ENV` | `production` | محیط Flask |
| `SECRET_KEY` | `cachelab-secret-key-2026` | در تولید تغییر دهید! |
| `ADMIN_TOKEN` | `cachelab-admin-2026` | در تولید تغییر دهید! |

## چک‌لیست امنیتی

- [ ] `SECRET_KEY` را تغییر دهید
- [ ] `ADMIN_TOKEN` را تغییر دهید
- [ ] از HTTPS استفاده کنید
- [ ] CORS را محدود کنید
- [ ] RBAC تنظیم کنید
