# Advanced Patterns

recall-cache provides 20 advanced caching patterns for production use.

## 1. Request Coalescing

Merge concurrent duplicate requests into a single fetch.

```python
from recall.advanced import RequestCoalescer

coalescer = RequestCoalescer()

@coalescer.coalesce(ttl="1h")
def get_user(user_id):
    return db.query(user_id)
```

## 2. Probabilistic Early Expiration

Facebook-style probabilistic early expiration to prevent thundering herd.

```python
from recall.advanced import ProbabilisticEarlyExpiration

@ProbabilisticEarlyExpiration(beta=1.0)
@cache(ttl="1h")
def get_data(key):
    return fetch(key)
```

## 3. Negative Cache

Cache None results to prevent repeated queries for missing data.

```python
from recall.advanced import NegativeCache

@NegativeCache(ttl="5m")
def find_user(email):
    return db.query(email)  # None is cached
```

## 4. Cache Patterns

Read-Through, Write-Through, Write-Behind patterns.

```python
from recall.advanced import CachePatterns

patterns = CachePatterns(
    read_through=db.query,
    write_through=db.save,
    write_behind=db.async_save
)

@patterns.cached(ttl="1h")
def get_user(user_id):
    return db.query(user_id)
```

## 5. Dependency Invalidation

Invalidate related keys when data changes.

```python
from recall.advanced import DependencyInvalidator

invalidator = DependencyInvalidator()

@invalidator.dependent_on(["users", "profiles"])
@cache(ttl="1h")
def get_user(user_id):
    return db.query(user_id)

# Invalidate all dependent keys
invalidator.invalidate("users")
```

## 6. Transaction Integration

Commit/rollback cache operations with database transactions.

```python
from recall.advanced import TransactionIntegration

tx_cache = TransactionIntegration()

@tx_cache.transactional(ttl="1h")
def update_user(user_id, data):
    return db.update(user_id, data)
```

## 7. Schema Versioning

Version cache keys for schema migrations.

```python
from recall.advanced import SchemaVersioning

@SchemaVersioning(schema_version="v2")
@cache(ttl="1h")
def get_user(user_id):
    return db.query(user_id)
```

## 8. HTTP Cache (ETag)

HTTP caching with ETag support.

```python
from recall.advanced import HTTPCache

http_cache = HTTPCache()

@http_cache.etag(ttl="1h")
def get_api_data(endpoint):
    return requests.get(endpoint)
```

## 9. Cache-Control Headers

Parse and respect Cache-Control headers.

```python
from recall.advanced import CacheControl

@CacheControl(max_age=3600, stale_while_revalidate=60)
@cache(ttl="1h")
def get_resource(url):
    return requests.get(url)
```

## 10. Adaptive TTL

Automatically adjust TTL based on hit rate.

```python
from recall.advanced import AdaptiveTTL

@AdaptiveTTL(min_ttl="30s", max_ttl="24h", target_hit_rate=0.95)
@cache(ttl="1h")
def get_data(key):
    return fetch(key)
```

## 11. Hot Key Detection

Detect frequently accessed keys.

```python
from recall.advanced import HotKeyDetector

detector = HotKeyDetector(threshold=100)

@detector.monitor(ttl="1h")
def get_user(user_id):
    return db.query(user_id)
```

## 12. Large Key Detection

Detect keys with large values.

```python
from recall.advanced import LargeKeyDetector

detector = LargeKeyDetector(max_size_bytes=1024*1024)  # 1MB

@detector.monitor(ttl="1h")
def get_data(key):
    return fetch(key)
```

## 13. Compression Monitoring

Track compression ratios.

```python
from recall.advanced import CompressionRatioMonitoring

monitor = CompressionRatioMonitoring()

@monitor.track(ttl="1h", compression=True)
def get_large_data():
    return list(range(100000))
```

## 14. Memory Fragmentation Tracking

Monitor memory fragmentation in the cache.

```python
from recall.advanced import MemoryFragmentationTracker

tracker = MemoryFragmentationTracker()

@tracker.monitor(ttl="1h")
def get_data(key):
    return fetch(key)
```

## 15. Stale Data Detection

Detect data that hasn't been refreshed recently.

```python
from recall.advanced import StaleDataDetector

detector = StaleDataDetector(max_age="1h")

@detector.monitor(ttl="1h")
def get_config():
    return fetch_config()
```

## 16. Startup Warmer

Pre-populate cache at application startup.

```python
from recall.advanced import StartupWarmer

warmer = StartupWarmer()

@warmer.warmup(keys=[(1,), (2,), (3,)], ttl="1h")
def get_user(user_id):
    return db.query(user_id)

# Run at startup
warmer.execute()
```

## 17. Graceful Degradation

Serve stale data when backend is unavailable.

```python
from recall.advanced import GracefulDegradation

@GracefulDegradation(stale_ttl="24h")
@cache(ttl="1h")
def get_data(key):
    return fetch(key)  # Returns stale data on failure
```

## 18. Idempotency Key Support

Prevent duplicate operations (e.g., payments).

```python
from recall.advanced import IdempotencyKeySupport

idempotency = IdempotencyKeySupport()

@idempotency.keyed(ttl="24h")
def process_payment(payment_id, amount):
    return gateway.charge(amount)
```

## 19. Request Deduplication

Remove duplicate requests within a time window.

```python
from recall.advanced import RequestDeduplication

dedup = RequestDeduplication(window="5s")

@dedup.deduplicate(ttl="1h")
def get_data(key):
    return fetch(key)
```

## 20. Cache Efficiency Tracking

Track hit rate over time.

```python
from recall.advanced import CacheEfficiencyTracker

tracker = CacheEfficiencyTracker()

@tracker.track(ttl="1h")
def get_user(user_id):
    return db.query(user_id)

# Get efficiency report
report = tracker.report()
print(report.hit_rate)
print(report.trend)
```

## Pattern Selection Guide

| Pattern | Use Case |
|---|---|
| Request Coalescing | High concurrency, same key |
| Probabilistic Early Expiration | Prevent thundering herd |
| Cache Patterns | Database caching layer |
| Dependency Invalidation | Related data changes |
| Transaction Integration | ACID compliance |
| Schema Versioning | API/schema migrations |
| HTTP Cache | REST API responses |
| Adaptive TTL | Variable access patterns |
| Hot Key Detection | Performance optimization |
| Large Key Detection | Memory optimization |
| Graceful Degradation | High availability |
| Idempotency Keys | Payment operations |
| Request Deduplication | Duplicate prevention |
| Startup Warmer | Fast cold start |
