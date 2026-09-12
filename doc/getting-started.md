# Getting Started

## What is CacheLab?

CacheLab is an interactive web platform for testing, benchmarking, and monitoring the [recall-cache](https://pypi.org/project/recall-cache) library. It provides:

- **Live Dashboard** — Real-time WebSocket-powered stats and charts
- **Core Tests** — 7 interactive cache operation tests
- **Advanced Patterns** — 20 advanced caching patterns
- **Benchmark Suite** — Full performance comparison
- **Admin Panel** — Built-in recall Admin with RBAC

## Prerequisites

- Python 3.8+
- pip or uv package manager

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sepehrhi/CacheLab.git
cd CacheLab
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or with uv:
```bash
uv pip install -r requirements.txt
```

### 4. Run CacheLab

```bash
python app.py
```

Or on Windows:
```bash
run.bat
```

### 5. Open in Browser

- **CacheLab**: http://localhost:5000
- **Admin Panel**: http://localhost:8080
  - Token: `cachelab-admin-2026`
  - Users: `admin/admin`, `developer/operator`

## First Steps

1. Open http://localhost:5000
2. Click **"شروع داشبورد"** to see the live dashboard
3. Navigate to **Core** to run interactive cache tests
4. Go to **Advanced** to explore 20 advanced patterns
5. Visit **Benchmark** to run performance comparisons

## Configuration

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `cachelab-secret-key-2026` | Flask secret key |
| `ADMIN_PORT` | `8080` | Built-in Admin Panel port |
| `ADMIN_TOKEN` | `cachelab-admin-2026` | Admin auth token |
| `MEMORY_MAXSIZE` | `1000` | Memory backend max items |
| `DISK_DIR` | `.cachelab_cache` | Disk backend directory |

## Troubleshooting

### Port Already in Use

If port 5000 or 8080 is occupied:

```bash
# Change port in app.py
socketio.run(app, host='0.0.0.0', port=5001)  # Change 5000 → 5001
```

### recall-cache Not Found

```bash
pip install recall-cache==3.1.0
```

### WebSocket Not Working

Ensure `eventlet` is installed:
```bash
pip install eventlet==0.35.1
```

## Next Steps

- Read [Core API](core-api.md) for detailed cache operations
- Explore [Backends](backends.md) for backend configuration
- Study [Advanced Patterns](advanced-patterns.md) for production patterns
- Check [WebSocket API](websocket-api.md) for real-time monitoring
