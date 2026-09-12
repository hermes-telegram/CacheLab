# CacheLab

**Interactive Cache Experimentation & Performance Platform powered by [recall-cache](https://pypi.org/project/recall-cache)**

[![PyPI](https://img.shields.io/pypi/v/recall-cache)](https://pypi.org/project/recall-cache)
[![GitHub](https://img.shields.io/github/license/hermes-telegram/recall)](https://github.com/hermes-telegram/recall)
[![Python](https://img.shields.io/pypi/pyversions/recall-cache)](https://python.org)

CacheLab is a Flask-SocketIO web platform for **testing, benchmarking, and monitoring** the [recall-cache](https://pypi.org/project/recall-cache) library. It provides a live dashboard, core cache tests, 20+ advanced patterns, and a full benchmark suite — all with real-time WebSocket updates.

---

## What is recall?

[recall](https://github.com/hermes-telegram/recall) ([pypi: recall-cache](https://pypi.org/project/recall-cache)) is a smart caching library for Python functions:

```python
from recall import cache

@cache(ttl="1h")
def get_user(user_id):
    return db.query(user_id)
```

### recall Features

| Feature | Description |
|---|---|
| **Simple API** | Just `@cache(ttl="1h")` on any function |
| **Multiple Backends** | Memory, Disk, Redis |
| **TTL Shorthand** | `"30m"`, `"1h"`, `"7d"` |
| **LRU Eviction** | Automatic cleanup when maxsize reached |
| **Thread-safe** | Works in concurrent environments |
| **Async Support** | Full async/await |
| **Cache Statistics** | Track hit/miss rates |
| **Stampede Protection** | Prevent cache stampede |
| **Background Refresh** | Auto-refresh before expiry |
| **Compression** | zlib compression |
| **Bulk Operations** | get_many, set_many, delete_many |
| **Serialization** | pickle, JSON, msgpack |
| **Namespacing** | Key prefix & versioning |
| **Cache Warming** | Pre-populate cache |
| **Sliding TTL** | Reset TTL on each access |
| **Zero Dependencies** | Redis optional |

**Links:**
- 📦 [PyPI: recall-cache](https://pypi.org/project/recall-cache)
- 🐙 [GitHub: hermes-telegram/recall](https://github.com/hermes-telegram/recall)

---

## CacheLab Features

### Pages

| Page | Description |
|---|---|
| **Dashboard** | Live WebSocket-powered stats, charts, and key monitor |
| **Core Tests** | Interactive tests: Set/Get, TTL expiry, LRU, compression, bulk ops, stampede, multi-tier |
| **Advanced** | 20 advanced patterns: Request Coalescing, Probabilistic Early Expiration, Negative Cache, Adaptive TTL, etc. |
| **Benchmark** | Full benchmark suite comparing backends and decorator performance |
| **Admin** | Built-in recall Admin Panel with RBAC and audit logging |

### Core Tests

1. **Set/Get** — Basic set+get with configurable TTL and backend
2. **TTL Expiration** — Verify key auto-expiry after TTL
3. **LRU Eviction** — Fill beyond maxsize, confirm oldest evicted
4. **Compression** — Compare compressed vs uncompressed size
5. **Bulk Operations** — set_many + get_many for 100 keys
6. **Stampede Protection** — 5 concurrent calls, only 1 real computation
7. **Multi-Tier** — L1 → L2 fallback after L1 clear

### Advanced Patterns (20)

Request Coalescing • Probabilistic Early Expiration • Negative Cache • Cache Patterns • Dependency Invalidation • Transaction Integration • Schema Versioning • HTTP Cache (ETag) • Cache-Control Headers • Adaptive TTL • Hot Key Detection • Large Key Detection • Compression Monitoring • Memory Fragmentation • Stale Data Detection • Startup Warmer • Graceful Degradation • Idempotency Keys • Request Deduplication • Cache Efficiency Tracking

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Contents:
```
flask==3.0.0
flask-socketio==5.3.6
recall-cache==3.1.0
eventlet==0.35.1
```

### 2. Run CacheLab

```bash
python app.py
```

Or on Windows:
```bash
run.bat
```

### 3. Open in Browser

- **CacheLab**: http://localhost:5000
- **Admin Panel**: http://localhost:8080
  - Token: `cachelab-admin-2026`
  - Users: `admin/admin`, `developer/operator`

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/stats` | Live stats (memory, disk, tests) |
| POST | `/api/test/<name>` | Run a core test |
| POST | `/api/benchmark/run` | Run full benchmark |
| POST | `/api/cache/clear` | Clear all caches |
| GET | `/api/keys?backend=memory` | List active keys |
| GET | `/api/key/<key>` | Get key value + TTL |
| DELETE | `/api/key/<key>` | Delete a key |

---

## Architecture

```
┌─────────────────────────────────────────────┐
│  Application Layer (Flask + SocketIO)        │
├─────────────────────────────────────────────┤
│  Pattern Layer (20 Advanced Patterns)        │
├─────────────────────────────────────────────┤
│  Core Layer (@cache, CacheStats, Key Builder)│
├─────────────────────────────────────────────┤
│  Backend Layer                               │
│  ┌────────┐ ┌──────┐ ┌───────┐ ┌──────────┐ │
│  │ Memory │ │ Disk │ │ Redis │ │Multi-Tier│ │
│  └────────┘ └──────┘ └───────┘ └──────────┘ │
├─────────────────────────────────────────────┤
│  Storage Layer (RAM, SSD/HDD, Redis Server)  │
└─────────────────────────────────────────────┘
```

---

## Project Structure

```
CacheLab/
├── app.py                  # Flask app + API endpoints
├── intro.html              # Animated landing page
├── app.js                  # Landing page JS
├── style.css               # Landing page styles
├── requirements.txt        # Python dependencies
├── run.bat                 # Windows launcher
├── templates/
│   ├── layout.html         # Base template (RTL, glassmorphism)
│   ├── index.html          # Home page
│   ├── dashboard.html      # Live dashboard
│   ├── core.html           # Core tests
│   ├── advanced.html       # Advanced patterns
│   ├── benchmark.html      # Benchmark suite
│   └── admin.html          # Admin panel
├── doc/                    # Full English documentation
│   ├── getting-started.md
│   ├── core-api.md
│   ├── backends.md
│   ├── advanced-patterns.md
│   ├── websocket-api.md
│   ├── benchmarking.md
│   └── deployment.md
├── doc-fa/                 # Persian (Farsi) documentation
│   ├── getting-started.md
│   ├── core-api.md
│   ├── backends.md
│   ├── advanced-patterns.md
│   ├── websocket-api.md
│   ├── benchmarking.md
│   └── deployment.md
└── README.md               # This file
```

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `cachelab-secret-key-2026` | Flask secret key |
| `ADMIN_PORT` | `8080` | Built-in Admin Panel port |
| `ADMIN_TOKEN` | `cachelab-admin-2026` | Admin auth token |
| `MEMORY_MAXSIZE` | `1000` | Memory backend max items |
| `DISK_DIR` | `.cachelab_cache` | Disk backend directory |

---

## recall Library Quick Reference

```python
from recall import cache, MemoryBackend, DiskBackend, RedisBackend, MultiTierBackend

# Default (MemoryBackend)
@cache(ttl="1h", maxsize=1000)
def get_user(user_id):
    return db.query(user_id)

# Disk (persistent)
@cache(ttl="24h", backend=DiskBackend("/tmp/my_cache"))
def get_config():
    return fetch_config()

# Redis
@cache(ttl="1h", backend=RedisBackend("redis://localhost:6379"))
def get_session(session_id):
    return db.query(session_id)

# Multi-Tier (L1=Memory, L2=Disk)
l1 = MemoryBackend(maxsize=100)
l2 = DiskBackend("/tmp/l2_cache")
multi = MultiTierBackend(l1=l1, l2=l2)
@cache(ttl="1h", backend=multi)
def get_data(key):
    return expensive_query(key)

# Management
get_user.cache_clear()           # Clear all
get_user.cache_delete(42)        # Delete key
get_user.cache_get(42)           # Get without compute
get_user.cache_set("k", "v")     # Set manually
get_user.cache_warm([(1,), (2,)])  # Pre-populate
stats = get_user.cache_stats     # hit_rate, hits, misses
keys = get_user.cache_keys()     # All keys
health = get_user.cache_health() # Backend health
```

---

## License

MIT

---

## Credits

- **recall-cache** — Smart caching library
  - [PyPI](https://pypi.org/project/recall-cache) • [GitHub](https://github.com/hermes-telegram/recall)
- **CacheLab** — This platform — built with Flask, SocketIO, Chart.js
- **Author**: sepehr H.I ([@sepehrhi](https://github.com/sepehrhi))
