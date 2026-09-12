# Core API

## Cache Decorator

The `@cache` decorator is the primary API for caching function results.

```python
from recall import cache

@cache(ttl="1h", maxsize=1000)
def get_user(user_id):
    return db.query(user_id)
```

### Decorator Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ttl` | str/int | `"1h"` | Time-to-live: `"30s"`, `"5m"`, `"1h"`, `"1d"`, or raw seconds |
| `maxsize` | int | `None` | Maximum items (LRU eviction when reached) |
| `backend` | Backend | `MemoryBackend()` | Backend instance |
| `sliding` | bool | `False` | Reset TTL on each access |
| `stampede_protection` | bool | `False` | Prevent cache stampede |
| `background_refresh` | int | `None` | Seconds before expiry to refresh |
| `compression` | bool | `False` | Enable zlib compression |
| `compression_level` | int | `6` | zlib level 1-9 |
| `serializer` | str | `"pickle"` | `"pickle"`, `"json"`, `"msgpack"` |
| `key_fn` | callable | `None` | Custom key function |
| `prefix` | str | `None` | Key prefix (namespacing) |
| `version` | str | `None` | Cache version (change to invalidate all) |
| `negative_cache` | bool | `False` | Cache None results |

## Cache Management

### Clear Cache

```python
get_user.cache_clear()
```

### Delete Key

```python
get_user.cache_delete(42)
```

### Get Without Computing

```python
result = get_user.cache_get(42)
```

### Set Manually

```python
get_user.cache_set("custom_key", "custom_value")
```

### Cache Warming

```python
get_user.cache_warm([(1,), (2,), (3,)])
```

### Cache Statistics

```python
stats = get_user.cache_stats
print(stats.hits)       # Number of hits
print(stats.misses)     # Number of misses
print(stats.hit_rate)   # Hit rate (0.0 to 1.0)
print(stats.size)       # Current cache size
```

### Bulk Operations

```python
# Get multiple keys
results = get_user.cache_get_many(["key1", "key2", "key3"])

# Set multiple keys
get_user.cache_set_many({"key1": 1, "key2": 2, "key3": 3})

# Delete multiple keys
get_user.cache_delete_many(["key1", "key2"])
```

### Health Check

```python
health = get_user.cache_health()
print(health.status)    # "healthy" or "unhealthy"
print(health.type)      # "memory", "disk", "redis", etc.
```

## Cache Stats Object

```python
from recall import CacheStats

stats = CacheStats()
stats.hits = 0
stats.misses = 0
stats.hit_rate = 0.0  # hits / (hits + misses)
stats.size = 0
stats.maxsize = None
```

## TTL Formats

| Shorthand | Meaning |
|---|---|
| `"30s"` | 30 seconds |
| `"5m"` | 5 minutes |
| `"1h"` | 1 hour |
| `"1d"` | 1 day |
| `"1w"` | 1 week |
| `3600` | Raw seconds (int/float) |

## Thread Safety

All cache operations are thread-safe. Multiple threads can safely call the same cached function:

```python
import concurrent.futures

@cache(ttl="1h")
def compute(x):
    return x * 2

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
    results = list(pool.map(compute, range(100)))
```

## Async Support

```python
@cache(ttl="1h")
async def get_user_async(user_id):
    return await db.query(user_id)

# Works with async functions
result = await get_user_async(1)

# Cache warming in async
await get_user_async.cache_warm([(1,), (2,)])
```

## Custom Key Function

```python
@cache(ttl="1h", key_fn=lambda f, a, k: f"{a[0]}_{k.get('mode', '')}")
def process(data, mode="default"):
    return f"{data}_{mode}"
```

## Cache Versioning

Change version to invalidate all existing cache entries:

```python
@cache(ttl="1h", version="2")  # All "v1" entries become stale
def get_data(key):
    return fetch(key)
```

## Namespacing with Prefix

```python
@cache(ttl="1h", prefix="myapp")
def get_user(user_id):
    return db.query(user_id)

# Keys stored as: "myapp:get_user:user_id=42"
```

## Serialization Formats

```python
# Pickle (default)
@cache(ttl="1h", serializer="pickle")
def get_data():
    return {"key": "value"}

# JSON (human-readable, larger)
@cache(ttl="1h", serializer="json")
def get_data():
    return {"key": "value"}

# Msgpack (compact, fast)
@cache(ttl="1h", serializer="msgpack")
def get_data():
    return {"key": "value"}
```

## Sliding TTL

Reset TTL on each access — perfect for session caching:

```python
@cache(ttl="5m", sliding=True)
def get_session(session_id):
    return db.query(session_id)
```

Each access resets the TTL to 5 minutes.

## Negative Cache

Cache None results to prevent repeated queries for missing data:

```python
@cache(ttl="1h", negative_cache=True)
def find_user(email):
    return db.query(email)  # None is cached too
```

## Background Refresh

Auto-refresh before expiry to prevent cache misses:

```python
@cache(ttl="1h", background_refresh=300)  # Refresh 5min before expiry
def get_config():
    return fetch_config()
```

## Compression

Enable zlib compression for large values:

```python
@cache(ttl="1h", compression=True, compression_level=6)
def get_large_data():
    return list(range(100000))
```

## Error Handling

```python
@cache(ttl="1h", fallback_on_error=True)
def get_data():
    return fetch_external()  # Returns stale data on error
```
