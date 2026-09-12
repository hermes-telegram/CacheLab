# Core API

## دکوریتور Cache

دکوریتور `@cache` رابط اصلی برای کش کردن نتایج توابع است.

```python
from recall import cache

@cache(ttl="1h", maxsize=1000)
def get_user(user_id):
    return db.query(user_id)
```

## پارامترهای دکوریتور

| پارامتر | نوع | پیش‌فرض | توضیح |
|---|---|---|---|
| `ttl` | str/int | `"1h"` | زمان انقضا: `"30s"`, `"5m"`, `"1h"`, `"1d"`, یا ثانیه خام |
| `maxsize` | int | `None` | حداکثر آیتم (حذف LRU هنگام رسیدن) |
| `backend` | Backend | `MemoryBackend()` | نمونه بک‌اند |
| `sliding` | bool | `False` | ریست TTL در هر دسترسی |
| `stampede_protection` | bool | `False` | جلوگیری از stampede |
| `background_refresh` | int | `None` | ثانیه قبل از انقضا برای تازه‌سازی |
| `compression` | bool | `False` | فعال‌سازی فشرده‌سازی zlib |
| `serializer` | str | `"pickle"` | `"pickle"`, `"json"`, `"msgpack"` |
| `prefix` | str | `None` | پیشوند کلید (نیم‌اسپیس) |
| `version` | str | `None` | نسخه کش (تغییر برای invalidate همه) |

## مدیریت کش

```python
get_user.cache_clear()           # پاک کردن
get_user.cache_delete(42)        # حذف کلید
get_user.cache_get(42)           # دریافت بدون محاسبه
get_user.cache_set("k", "v")     # تنظیم دستی
get_user.cache_warm([(1,), (2,)])  # گرم کردن

# آمار
stats = get_user.cache_stats
print(stats.hits, stats.misses, stats.hit_rate)

# عملیات گروهی
get_user.cache_get_many(["k1", "k2"])
get_user.cache_set_many({"k1": 1, "k2": 2})
get_user.cache_delete_many(["k1"])

# بررسی سلامت
health = get_user.cache_health()
```

## شماره‌گذاری نسخه

```python
@cache(ttl="1h", version="2")  # همه entryهای v1 کهنه می‌شوند
def get_data(key):
    return fetch(key)
```

## TTL لغزشی

```python
@cache(ttl="5m", sliding=True)
def get_session(session_id):
    return db.query(session_id)
```

## کش منفی

```python
@cache(ttl="1h", negative_cache=True)
def find_user(email):
    return db.query(email)  # None هم کش می‌شود
```

## تازه‌سازی پس‌زمینه

```python
@cache(ttl="1h", background_refresh=300)
def get_config():
    return fetch_config()
```

## استفاده از async

```python
@cache(ttl="1h")
async def get_user_async(user_id):
    return await db.query(user_id)

result = await get_user_async(1)
await get_user_async.cache_warm([(1,), (2,)])
```
