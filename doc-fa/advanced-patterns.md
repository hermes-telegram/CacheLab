# الگوهای پیشرفته

| # | الگو | توضیح |
|---|---|---|
| 1 | Request Coalescing | ترکیب درخواست‌های تکراری |
| 2 | Probabilistic Early Expiration | جلوگیری از thundering herd |
| 3 | Negative Cache | کش کردن None |
| 4 | Cache Patterns | Read-Through/Write-Behind |
| 5 | Dependency Invalidation | ابطال وابستگی‌ها |
| 6 | Transaction Integration | commit/rollback |
| 7 | Schema Versioning | نسخه‌بندی ساختار |
| 8 | HTTP Cache (ETag) | کش HTTP |
| 9 | Cache-Control | هدرهای Cache-Control |
| 10 | Adaptive TTL | تنظیم خودکار TTL |
| 11 | Hot Key Detection | تشخیص کلید پرتکرار |
| 12 | Large Key Detection | تشخیص کلید بزرگ |
| 13 | Compression Monitoring | ردیابی فشرده‌سازی |
| 14 | Memory Fragmentation | تکه‌تکه شدن حافظه |
| 15 | Stale Data Detection | تشخیص داده کهنه |
| 16 | Startup Warmer | گرم کردن اولیه |
| 17 | Graceful Degradation | افت افزایشی |
| 18 | Idempotency Key | عملیات تکراری‌ناپذیر |
| 19 | Request Deduplication | حذف درخواست تکراری |
| 20 | Cache Efficiency | ردیابی hit rate |

## مثال‌ها

### Request Coalescing

```python
from recall.advanced import RequestCoalescer
coalescer = RequestCoalescer()

@coalescer.coalesce(ttl="1h")
def get_user(user_id):
    return db.query(user_id)
```

### Adaptive TTL

```python
from recall.advanced import AdaptiveTTL

@AdaptiveTTL(min_ttl="30s", max_ttl="24h", target_hit_rate=0.95)
@cache(ttl="1h")
def get_data(key):
    return fetch(key)
```

### Startup Warmer

```python
from recall.advanced import StartupWarmer
warmer = StartupWarmer()

@warmer.warmup(keys=[(1,), (2,), (3,)], ttl="1h")
def get_user(user_id):
    return db.query(user_id)

# اجرا در زمان شروع
warmer.execute()
```

### Graceful Degradation

```python
from recall.advanced import GracefulDegradation

@GracefulDegradation(stale_ttl="24h")
@cache(ttl="1h")
def get_data(key):
    return fetch(key)
```
