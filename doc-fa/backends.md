# بک‌اندها

| ویژگی | حافظه | دیسک | Redis | چندلایه |
|---|---|---|---|---|
| ماندگاری | ❌ | ✅ | ✅ | ✅ |
| توزیع‌شده | ❌ | ❌ | ✅ | ❌ |
| رمزنگاری | ❌ | ✅ | ❌ | بستگی دارد |
| LRU Eviction | ✅ | ❌ | ✅ (Redis) | فقط L1 |
| سرعت | سریع‌ترین | کند | سریع | سریع |

## حافظه (پیش‌فرض)

```python
from recall import MemoryBackend
backend = MemoryBackend(maxsize=1000)
```

- خواندن: ~250,000 ops/s
- نوشتن: ~200,000 ops/s

## دیسک

```python
from recall import DiskBackend
backend = DiskBackend("/tmp/cache", compression=True)
```

- خواندن: ~45,000 ops/s
- نوشتن: ~35,000 ops/s

## Redis

```python
from recall import RedisBackend
backend = RedisBackend("redis://localhost:6379")
```

- خواندن: ~120,000 ops/s (محلی)
- نوشتن: ~100,000 ops/s (محلی)

## چندلایه

```python
from recall import MultiTierBackend
l1 = MemoryBackend(maxsize=100)
l2 = DiskBackend("/tmp/l2")
multi = MultiTierBackend(l1=l1, l2=l2)
```

## انتخاب بک‌اند

| مورد استفاده | بک‌اند توصیه‌شده |
|---|---|
| کش ساده، تک پروسه | حافظه |
| ماندگار بعد از restart | دیسک |
| چندین سرور | Redis |
| بهترین عملکرد | چندلایه |
