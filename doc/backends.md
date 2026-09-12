# Backends

recall-cache provides 4 built-in backends for different use cases.

## Memory Backend (Default)

In-memory cache with LRU eviction. Fastest option, data lost on restart.

```python
from recall import cache, MemoryBackend

backend = MemoryBackend(maxsize=1000, compression=False)
@cache(ttl="1h", backend=backend)
def func(x):
    return x * 2
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `maxsize` | int | `None` | Maximum items (None = unlimited) |
| `compression` | bool | `False` | Enable zlib compression |
| `compression_level` | int | `6` | zlib level 1-9 |

### Performance

- Read: ~250,000 ops/s
- Write: ~200,000 ops/s
- Latency: <1ms

## Disk Backend

Persistent file-based cache. Survives restarts.

```python
from recall import cache, DiskBackend

backend = DiskBackend(
    directory="/tmp/my_cache",
    compression=True,
    max_bytes=100*1024*1024  # 100MB limit
)
@cache(ttl="24h", backend=backend)
def func(x):
    return x * 2
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `directory` | str | `".cache"` | Cache directory path |
| `compression` | bool | `False` | Enable zlib compression |
| `compression_level` | int | `6` | zlib level 1-9 |
| `max_bytes` | int | `None` | Max total size in bytes |
| `encryption_key` | bytes | `None` | AES-256-GCM encryption key |

### Performance

- Read: ~45,000 ops/s
- Write: ~35,000 ops/s
- Latency: 2-5ms

## Redis Backend

Distributed cache using Redis. Shared across multiple processes/servers.

```python
from recall import cache, RedisBackend

backend = RedisBackend(
    url="redis://localhost:6379",
    max_connections=10,
    retry_on_timeout=True
)
@cache(ttl="1h", backend=backend)
def func(x):
    return x * 2
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | str | `"redis://localhost:6379"` | Redis connection URL |
| `max_connections` | int | `10` | Connection pool size |
| `retry_on_timeout` | bool | `True` | Retry on timeout |
| `socket_timeout` | float | `5.0` | Socket timeout in seconds |
| `key_prefix` | str | `"recall:"` | Prefix for all keys |

### Performance

- Read: ~120,000 ops/s (local Redis)
- Write: ~100,000 ops/s (local Redis)
- Latency: 1-3ms (local), 5-15ms (remote)

## Multi-Tier Backend

Combines L1 (fast) and L2 (large) backends with automatic fallback.

```python
from recall import cache, MemoryBackend, DiskBackend, MultiTierBackend

l1 = MemoryBackend(maxsize=100)
l2 = DiskBackend("/tmp/l2_cache")
multi = MultiTierBackend(l1=l1, l2=l2)

@cache(ttl="1h", backend=multi)
def func(x):
    return x * 2
```

### How It Works

1. **Read**: Try L1 first, fall back to L2, return None if miss
2. **Write**: Write to both L1 and L2
3. **Backfill**: If L2 hit, automatically populate L1

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `l1` | Backend | Required | Fast backend (Memory) |
| `l2` | Backend | Required | Large backend (Disk/Redis) |
| `l1_ttl` | str/int | `None` | Override TTL for L1 |
| `l2_ttl` | str/int | `None` | Override TTL for L2 |
| `backfill` | bool | `True` | Auto-populate L1 on L2 hit |

### Performance

- L1 hit: Same as Memory backend
- L2 hit: Same as L2 backend + L1 backfill
- Miss: L1 + L2 lookup time

## Custom Backend

Create your own backend by extending `CacheBackend`:

```python
from recall import CacheBackend

class MyBackend(CacheBackend):
    def get(self, key):
        # Return (expire_time, value) or None
        pass

    def set(self, key, value, ttl):
        pass

    def delete(self, key):
        pass

    def clear(self):
        pass

    def keys(self):
        pass

    def health(self):
        pass
```

## Backend Comparison

| Feature | Memory | Disk | Redis | Multi-Tier |
|---|---|---|---|---|
| Persistence | ❌ | ✅ | ✅ | ✅ |
| Distributed | ❌ | ❌ | ✅ | ❌ |
| Encryption | ❌ | ✅ | ❌ | Depends |
| LRU Eviction | ✅ | ❌ | ✅ (Redis) | L1 only |
| Compression | Optional | Optional | ❌ | L1 only |
| Speed | Fastest | Slow | Fast | Fast |
| Capacity | RAM limited | Disk limited | RAM limited | Combined |

## Choosing a Backend

| Use Case | Recommended Backend |
|---|---|
| Simple caching, single process | Memory |
| Survive restarts, single server | Disk |
| Multiple servers/processes | Redis |
| Best performance, large dataset | Multi-Tier (Memory + Disk) |
