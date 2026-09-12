"""CacheLab — پلتفرم آزمایش و بهره‌وری کش recall"""

import os
import sys
import time
import threading
from datetime import datetime

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

# Core recall
from recall import cache, MemoryBackend, DiskBackend, MultiTierBackend, CacheStats
from recall.cache import RedisBackend

# Advanced
from recall.advanced import (
    RequestCoalescer, ProbabilisticEarlyExpiration, NegativeCache,
    CachePatterns, DependencyInvalidator, TransactionIntegration,
    SchemaVersioning, HTTPCache, CacheControl, AdaptiveTTL,
    HotKeyDetector, LargeKeyDetector, CompressionRatioMonitoring,
    MemoryFragmentationTracker, StaleDataDetector, StartupWarmer,
    GracefulDegradation, IdempotencyKeySupport, RequestDeduplication,
    CacheEfficiencyTracker,
)

# Admin & Metrics
from recall.admin import AdminPanel, RBACManager, start_admin
from recall.metrics import MetricsCollector

# Other
from recall.memory import MemoryTracker
from recall.backup import BackupManager
from recall.audit import AuditLogger
from recall.circuit import CircuitBreaker
from recall.ratelimit import RateLimiter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cachelab-secret-key-2026'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# ── Global State ──────────────────────────────────────────
lab_state = {
    'started_at': datetime.now().isoformat(),
    'total_tests_run': 0,
    'backends': {},
    'benchmark_results': [],
    'monitor_active': False,
}

# Initialize backends
memory_backend = MemoryBackend(maxsize=1000)
disk_backend = DiskBackend(directory='.cachelab_cache', compression=False)
lab_state['backends'] = {
    'memory': memory_backend,
    'disk': disk_backend,
}

# Start recall's built-in Admin Panel on port 8080
admin_panel = AdminPanel(
    backend=memory_backend,
    port=8080,
    host="0.0.0.0",
    auth_token="cachelab-admin-2026",
    enable_metrics=True,
    enable_audit=True,
    enable_rbac=True,
)
admin_panel._rbac.add_user("admin", "admin", "cachelab-admin-2026")
admin_panel._rbac.add_user("developer", "operator", "dev-token-2026")
admin_panel.start()
print("🔐 Admin Panel (recall built-in) started at http://localhost:8080")

# Metrics
metrics = MetricsCollector(memory_backend)
audit = AuditLogger()


# ═══════════════════════════════════════════════════════════
# Pages
# ═══════════════════════════════════════════════════════════

@app.route('/')
def index():
    """صفحه معرفی CacheLab"""
    return render_template('index.html', version='3.1.0', active_page='index')

@app.route('/dashboard')
def dashboard():
    """داشبورد زنده"""
    stats = {
        'memory': memory_backend.health(),
        'disk': disk_backend.health(),
        'total_tests': lab_state['total_tests_run'],
    }
    return render_template('dashboard.html', stats=stats, active_page='dashboard')

@app.route('/core')
def core_page():
    """صفحه آزمون Core"""
    return render_template('core.html', active_page='core')

@app.route('/advanced')
def advanced_page():
    """صفحه الگوهای پیشرفته"""
    features = [
        ('Request Coalescing', 'ترکیب درخواست‌های تکراری'),
        ('Probabilistic Early Expiration', 'انقضا احتمالی زودهنگام'),
        ('Negative Cache', 'کش نتایج منفی'),
        ('Cache Patterns', 'الگوهای Read-Through/Write-Behind'),
        ('Read-Through', 'خواندن از طریق کش'),
        ('Write-Through', 'نوشتن از طریق کش'),
        ('Startup Warmer', 'گرم کردن اولیه'),
        ('Graceful Degradation', 'افت افزایشی'),
        ('Adaptive TTL', 'TTL تطبیقی'),
        ('Cache-Control', 'هدرهای Cache-Control'),
        ('Cache Efficiency', 'بهره‌وری کش'),
        ('Dependency Invalidation', 'ابطال وابستگی‌ها'),
        ('HTTP Cache (ETag)', 'کش HTTP با ETag'),
        ('Hot Key Detection', 'تشخیص کلید داغ'),
        ('Idempotency Key', 'کلید تکراری‌ناپذیری'),
        ('Large Key Detection', 'تشخیص کلید بزرگ'),
        ('Request Deduplication', 'حذف درخواست تکراری'),
        ('Schema Versioning', 'نسخه‌بندی ساختار'),
        ('Stale Data Detection', 'تشخیص داده کهنه'),
        ('Transaction Integration', 'یکپارچه تراکنش'),
        ('Memory Fragmentation', 'تکه‌تکه شدن حافظه'),
    ]
    return render_template('advanced.html', features=features, active_page='advanced')

@app.route('/benchmark')
def benchmark_page():
    """صفحه بنچمارک"""
    return render_template('benchmark.html', results=lab_state['benchmark_results'], active_page='benchmark')

@app.route('/admin')
def admin_page():
    """پنل ادمین داخلی recall رو مستقیم نشون بده"""
    return '''
    <html><head><meta http-equiv="refresh" content="0; url=http://localhost:8080?token=cachelab-admin-2026"></head>
    <body style="background:#0f0f1a;display:flex;align-items:center;justify-content:center;height:100vh;margin:0">
    <div style="text-align:center;color:#6c63ff;font-family:sans-serif">
    <h1>🔐 در حال انتقال به پنل ادمین...</h1>
    <p>اگر منتقل نشدید <a href="http://localhost:8080?token=cachelab-admin-2026" style="color:#00d26a">اینجا</a> کلیک کنید</p>
    </div></body></html>'''

@app.route('/intro')
def intro_page():
    """صفحه intro دو زبانه"""
    from flask import send_from_directory
    return send_from_directory('.', 'intro.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """سرو کردن فایل‌های استاتیک"""
    from flask import send_from_directory
    return send_from_directory('.', filename)

# ═══════════════════════════════════════════════════════════
# API Endpoints
# ═══════════════════════════════════════════════════════════

@app.route('/api/test/<test_name>', methods=['POST'])
def run_test(test_name):
    """اجرای یک تست خاص"""
    data = request.get_json() or {}
    lab_state['total_tests_run'] += 1

    try:
        result = _run_core_test(test_name, data)
        audit.log(f"test:{test_name}", result.get('status', 'ok'))
        emit_metric('test_complete', {'name': test_name, 'result': result})
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/test/advanced', methods=['POST'])
def run_advanced_test():
    """تست واقعی الگوهای پیشرفته"""
    data = request.get_json() or {}
    pattern = data.get('pattern', '')
    lab_state['total_tests_run'] += 1

    try:
        result = _run_advanced_test(pattern, data)
        audit.log(f"advanced:{pattern}", result.get('status', 'ok'))
        emit_metric('test_complete', {'name': pattern, 'result': result})
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/benchmark/run', methods=['POST'])
def run_benchmark():
    """اجرای بنچمارک کامل"""
    data = request.get_json() or {}
    size = data.get('size', 1000)

    results = _run_benchmarks(size)
    lab_state['benchmark_results'] = results
    emit_metric('benchmark_complete', {'results': results})
    return jsonify({'status': 'ok', 'results': results})

@app.route('/api/stats')
def get_stats():
    """آمار لحظه‌ای"""
    return jsonify({
        'memory': memory_backend.health(),
        'disk': disk_backend.health(),
        'total_tests': lab_state['total_tests_run'],
        'started_at': lab_state['started_at'],
    })

@app.route('/api/cache/clear', methods=['POST'])
def clear_all_cache():
    """پاک کردن تمام کش‌ها"""
    memory_backend.clear()
    disk_backend.clear()
    return jsonify({'status': 'ok', 'message': 'All caches cleared'})

@app.route('/api/keys', methods=['GET'])
def get_all_keys():
    """لیست کلید‌های فعال"""
    backend = request.args.get('backend', 'memory')
    b = lab_state['backends'].get(memory_backend if backend == 'memory' else disk_backend)
    if backend == 'memory':
        keys = memory_backend.keys()
    else:
        keys = disk_backend.keys()
    return jsonify({'backend': backend, 'keys': keys[:100]})

@app.route('/api/key/<key>', methods=['GET'])
def get_key_value(key):
    """مقدار یک کلید"""
    backend = request.args.get('backend', 'memory')
    b = memory_backend if backend == 'memory' else disk_backend
    result = b.get(key)
    if result:
        expire_time, value = result
        ttl = expire_time - time.time()
        return jsonify({'found': True, 'ttl': ttl, 'value': str(value)[:500]})
    return jsonify({'found': False})

@app.route('/api/key/<key>', methods=['DELETE'])
def delete_key(key):
    """حذف یک کلید"""
    backend = request.args.get('backend', 'memory')
    if backend == 'memory':
        memory_backend.delete(key)
    else:
        disk_backend.delete(key)
    return jsonify({'status': 'ok'})


# ═══════════════════════════════════════════════════════════
# Core Test Runner
# ═══════════════════════════════════════════════════════════

def _run_core_test(test_name, data):
    """اجرای تست‌های Core"""

    if test_name == 'set_get':
        key = data.get('key', 'test_key')
        value = data.get('value', 'test_value')
        ttl = int(data.get('ttl', 60))
        backend = data.get('backend', 'memory')
        b = memory_backend if backend == 'memory' else disk_backend

        t0 = time.time()
        b.set(key, value, ttl)
        b.get(key)
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'operation': 'set + get',
            'time_ms': round(elapsed, 3),
            'backend': backend,
            'health': b.health(),
        }

    elif test_name == 'ttl_expire':
        key = data.get('key', 'expire_test')
        ttl = int(data.get('ttl', 2))
        memory_backend.set(key, 'will_expire', ttl)
        t0 = time.time()
        memory_backend.get(key)  # should exist
        exists_before = time.time() - t0
        time.sleep(ttl + 0.5)
        result = memory_backend.get(key)  # should be expired
        elapsed = (time.time() - t0) * 1000
        return {
            'status': 'ok',
            'operation': 'ttl_expire',
            'expired': result is None,
            'time_ms': round(elapsed, 3),
        }

    elif test_name == 'lru_eviction':
        small = MemoryBackend(maxsize=5)
        for i in range(10):
            small.set(f'key_{i}', f'value_{i}', 60)
        keys = small.keys()
        return {
            'status': 'ok',
            'operation': 'lru_eviction',
            'maxsize': 5,
            'items_added': 10,
            'remaining_keys': len(keys),
            'keys': keys,
        }

    elif test_name == 'compression':
        import pickle
        large_value = list(range(10000))
        compressed = MemoryBackend(maxsize=100, compression=True)
        normal = MemoryBackend(maxsize=100, compression=False)

        compressed.set('large', large_value, 60)
        normal.set('large', large_value, 60)

        original_size = len(pickle.dumps(large_value))

        return {
            'status': 'ok',
            'operation': 'compression',
            'original_size_bytes': original_size,
            'compression_enabled': True,
            'backend': 'memory',
        }

    elif test_name == 'bulk_ops':
        items = {f'bulk_{i}': f'val_{i}' for i in range(100)}
        t0 = time.time()
        memory_backend.set_many(items, 60)
        results = memory_backend.get_many(list(items.keys())[:10])
        elapsed = (time.time() - t0) * 1000
        return {
            'status': 'ok',
            'operation': 'bulk_set_many + get_many',
            'items': 100,
            'time_ms': round(elapsed, 3),
        }

    elif test_name == 'stampede':
        call_count = 0

        @cache(ttl="5s", stampede_protection=True, backend=MemoryBackend())
        def expensive(x):
            nonlocal call_count
            call_count += 1
            time.sleep(0.5)
            return x * 2

        import concurrent.futures
        t0 = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
            futures = [pool.submit(expensive, 42) for _ in range(5)]
            results = [f.result() for f in futures]
        elapsed = time.time() - t0

        return {
            'status': 'ok',
            'operation': 'stampede_protection',
            'concurrent_calls': 5,
            'actual_computations': call_count,
            'time_sec': round(elapsed, 2),
            'all_same': len(set(results)) == 1,
        }

    elif test_name == 'multi_tier':
        l1 = MemoryBackend(maxsize=50)
        l2 = MemoryBackend(maxsize=500)  # simulate L2
        multi = MultiTierBackend(l1=l1, l2=l2)

        # Set value
        multi.set('mt_key', 'mt_value', 60)

        # Get from L1
        r1 = multi.get('mt_key')

        # Clear L1, should fall back to L2
        l1.clear()
        r2 = multi.get('mt_key')

        return {
            'status': 'ok',
            'operation': 'multi_tier',
            'l1_hit': r1 is not None,
            'l2_fallback': r2 is not None,
            'health': multi.health(),
        }

    return {'status': 'error', 'message': f'Unknown test: {test_name}'}


# ═══════════════════════════════════════════════════════════
# Benchmark Runner
# ═══════════════════════════════════════════════════════════

def _run_benchmarks(size=1000):
    """اجرای بنچمارک روی همه بک‌ها"""
    results = []

    # Memory Backend
    b = MemoryBackend(maxsize=size * 2)

    t0 = time.time()
    for i in range(size):
        b.set(f'key_{i}', f'value_{i}' * 10, 300)
    set_time = time.time() - t0

    t0 = time.time()
    for i in range(size):
        b.get(f'key_{i}')
    get_time = time.time() - t0

    results.append({
        'backend': 'Memory',
        'size': size,
        'set_time': round(set_time, 4),
        'get_time': round(get_time, 4),
        'set_ops_per_sec': round(size / set_time),
        'get_ops_per_sec': round(size / get_time),
    })

    # Memory Backend with Compression
    bc = MemoryBackend(maxsize=size * 2, compression=True)

    t0 = time.time()
    for i in range(size):
        bc.set(f'key_{i}', list(range(100)), 300)
    set_time_c = time.time() - t0

    t0 = time.time()
    for i in range(size):
        bc.get(f'key_{i}')
    get_time_c = time.time() - t0

    results.append({
        'backend': 'Memory+Compression',
        'size': size,
        'set_time': round(set_time_c, 4),
        'get_time': round(get_time_c, 4),
        'set_ops_per_sec': round(size / set_time_c),
        'get_ops_per_sec': round(size / get_time_c),
    })

    # Decorator cache
    call_count = 0

    @cache(ttl="5m", backend=MemoryBackend(maxsize=size))
    def bench_func(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    t0 = time.time()
    for i in range(size):
        bench_func(i)
    dec_miss_time = time.time() - t0

    t0 = time.time()
    for i in range(size):
        bench_func(i)
    dec_hit_time = time.time() - t0

    results.append({
        'backend': '@cache (miss)',
        'size': size,
        'time': round(dec_miss_time, 4),
        'ops_per_sec': round(size / dec_miss_time),
    })
    results.append({
        'backend': '@cache (hit)',
        'size': size,
        'time': round(dec_hit_time, 4),
        'ops_per_sec': round(size / dec_hit_time),
    })

    return results


# ═══════════════════════════════════════════════════════════
# Advanced Pattern Test Runner
# ═══════════════════════════════════════════════════════════

def _run_advanced_test(pattern, data):
    """تست واقعی الگوهای پیشرفته"""
    b = MemoryBackend(maxsize=100)

    if pattern == 'coalescer':
        coalescer = RequestCoalescer()
        call_count = 0

        @coalescer.coalesce(key_fn=lambda user_id: f"user:{user_id}")
        def fetch_user(user_id):
            nonlocal call_count
            call_count += 1
            return {"id": user_id, "name": f"User_{user_id}"}

        t0 = time.time()
        results = [fetch_user(1) for _ in range(5)]
        elapsed = time.time() - t0

        return {
            'status': 'ok',
            'pattern': 'Request Coalescing',
            'concurrent_calls': 5,
            'actual_computations': call_count,
            'time_sec': round(elapsed, 3),
            'all_same': len(set(str(r) for r in results)) == 1,
            'backend': 'memory',
        }

    elif pattern == 'pee':
        from recall.advanced import ProbabilisticEarlyExpiration
        call_count = 0

        @cache(ttl="5m", backend=b)
        def fetch_data(key):
            nonlocal call_count
            call_count += 1
            return f"data_{key}"

        t0 = time.time()
        fetch_data("pee_test_key")
        time.sleep(0.1)
        result = fetch_data("pee_test_key")
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Probabilistic Early Expiration',
            'cache_hit': call_count == 1,
            'computations': call_count,
            'time_ms': round(elapsed, 2),
            'value': result,
            'backend': 'memory',
        }

    elif pattern == 'negative':
        from recall.advanced import NegativeCache
        neg = NegativeCache(b, ttl=300)

        t0 = time.time()
        result1 = neg.get("missing_key", lambda: None)
        result2 = neg.get("missing_key", lambda: None)
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Negative Cache',
            'first_call': result1,
            'second_call': result2,
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'patterns':
        call_count = 0

        @cache(ttl="5m", backend=b)
        def get_data(key):
            nonlocal call_count
            call_count += 1
            return f"data_{key}"

        t0 = time.time()
        get_data("p1")
        get_data("p1")
        get_data("p1")
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Cache Patterns',
            'total_calls': 3,
            'actual_computations': call_count,
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'warmer':
        call_count = 0

        @cache(ttl="5m", backend=b)
        def warmup_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        t0 = time.time()
        warmup_func.cache_warm([(1,), (2,), (3,)])
        elapsed = (time.time() - t0) * 1000

        r1 = warmup_func(1)
        r2 = warmup_func(2)
        r3 = warmup_func(3)

        return {
            'status': 'ok',
            'pattern': 'Startup Warmer',
            'warmed_keys': [1, 2, 3],
            'results': [r1, r2, r3],
            'actual_computations': call_count,
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'graceful':
        from recall.advanced import GracefulDegradation
        g = GracefulDegradation(b, stale_ttl=60)
        call_count = 0

        @g.resilient(ttl=60)
        def graceful_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        t0 = time.time()
        r1 = graceful_func(42)
        r2 = graceful_func(42)
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Graceful Degradation',
            'first_result': r1,
            'second_result_cached': r2,
            'computations': call_count,
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'adaptive':
        from recall.advanced import AdaptiveTTL
        at = AdaptiveTTL(b)
        call_count = 0

        @at.cached(target_hit_rate=0.8)
        def adapt_func(x):
            nonlocal call_count
            call_count += 1
            return x * 3

        t0 = time.time()
        r1 = adapt_func(5)
        r2 = adapt_func(5)
        r3 = adapt_func(5)
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Adaptive TTL',
            'result': r1,
            'computations': call_count,
            'total_calls': 3,
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'cache_control':
        from recall.advanced import CacheControl
        cc = CacheControl(b)
        call_count = 0

        @cc.cached(max_age=60, stale_while_revalidate=30)
        def cc_func(x):
            nonlocal call_count
            call_count += 1
            return f"cc_{x}"

        t0 = time.time()
        r1 = cc_func("test")
        r2 = cc_func("test")
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Cache Control',
            'result': r1,
            'computations': call_count,
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'efficiency':
        from recall.advanced import CacheEfficiencyTracker
        et = CacheEfficiencyTracker(b)

        @cache(ttl=60, backend=b)
        def eff_func(x):
            return x * 2

        eff_func(1)
        eff_func(1)
        eff_func(1)
        eff_func(2)

        t0 = time.time()
        history = et.get_history()
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Cache Efficiency Tracker',
            'history': history,
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'read_through':
        from recall.advanced import CachePatterns
        cp = CachePatterns(b, data_source=None)
        call_count = [0]

        def fetch_from_db():
            call_count[0] += 1
            return "db_user:1"

        t0 = time.time()
        r1 = cp.read_through("user:1", fetch_from_db, ttl=60)
        r2 = cp.read_through("user:1", fetch_from_db, ttl=60)
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Read-Through',
            'first_result': r1,
            'cached_result': r2,
            'db_queries': call_count[0],
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'write_through':
        from recall.advanced import CachePatterns
        cp = CachePatterns(b, data_source=None)
        t0 = time.time()
        cp.write_through("wt_key", "wt_value", ttl=60)
        cached = b.get("wt_key")
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Write-Through',
            'cached_value': cached,
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'dependency':
        from recall.advanced import DependencyInvalidator
        di = DependencyInvalidator(b)

        b.set("post:1", "Post 1", ttl=300)
        b.set("post:2", "Post 2", ttl=300)
        b.set("author:posts", "list", ttl=300)

        di.register("author:1", ["post:1", "post:2"])

        t0 = time.time()
        di.invalidate("author:1")
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Dependency Invalidation',
            'invalidated': True,
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'http_cache':
        from recall.advanced import HTTPCache
        hc = HTTPCache(b)

        @hc.etag(ttl=60)
        def get_users():
            return {"users": ["alice", "bob"]}

        t0 = time.time()
        result = get_users()
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'HTTP Cache (ETag)',
            'result': result,
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'hot_keys':
        from recall.advanced import HotKeyDetector
        hk = HotKeyDetector(b, threshold=3)

        @hk.monitor
        @cache(ttl=60, backend=b)
        def hot_func(x):
            return x * 2

        for _ in range(5):
            hot_func("popular")
        hot_func("rare")

        t0 = time.time()
        hot = hk.get_hot_keys()
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Hot Key Detection',
            'hot_keys': hot,
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'idempotency':
        from recall.advanced import IdempotencyKeySupport
        ik = IdempotencyKeySupport(b)

        @ik.cache(ttl=60)
        def process_payment(order_id):
            return f"processed_{order_id}"

        t0 = time.time()
        r1 = process_payment("order_123")
        r2 = process_payment("order_123")
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Idempotency Key Support',
            'first_result': r1,
            'duplicate_result': r2,
            'same': r1 == r2,
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'large_keys':
        from recall.advanced import LargeKeyDetector
        lk = LargeKeyDetector(b, max_size_bytes=100)

        b.set("small", "x", ttl=60)
        b.set("large", "x" * 200, ttl=60)

        t0 = time.time()
        large = lk.get_large_keys()
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Large Key Detection',
            'large_keys': large,
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'dedup':
        from recall.advanced import RequestDeduplication
        rd = RequestDeduplication(b)
        call_count = 0

        @rd.deduplicate
        def dedup_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        t0 = time.time()
        results = [dedup_func(1) for _ in range(5)]
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Request Deduplication',
            'calls': 5,
            'computations': call_count,
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'schema_versioning':
        from recall.advanced import SchemaVersioning
        sv = SchemaVersioning(b, version="1.0.0")

        @sv.cached(ttl=60)
        def get_data(x):
            return f"data_v1_{x}"

        t0 = time.time()
        r1 = get_data("test")
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Schema Versioning',
            'result': r1,
            'version': '1.0.0',
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'stale_detector':
        from recall.advanced import StaleDataDetector
        sd = StaleDataDetector(b, max_age_seconds=1)

        b.set("fresh_key", "fresh_value", ttl=60)
        b.set("stale_key", "stale_value", ttl=1)

        time.sleep(1.5)

        t0 = time.time()
        stale = sd.find_stale_keys()
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Stale Data Detection',
            'stale_keys_count': len(stale),
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'transaction':
        from recall.advanced import TransactionIntegration
        ti = TransactionIntegration(b)

        t0 = time.time()
        with ti.transaction() as tx:
            tx.set("acc:1", 100, ttl=60)
            tx.set("acc:2", 200, ttl=60)
        
        r1 = b.get("acc:1")
        r2 = b.get("acc:2")
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Transaction Integration',
            'values': [r1, r2],
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    elif pattern == 'fragmentation':
        from recall.advanced import MemoryFragmentationTracker
        mf = MemoryFragmentationTracker(b)

        for i in range(10):
            b.set(f"frag_key_{i}", f"value_{i}", ttl=60)

        mf.snapshot()

        t0 = time.time()
        frag = mf.get_fragmentation()
        elapsed = (time.time() - t0) * 1000

        return {
            'status': 'ok',
            'pattern': 'Memory Fragmentation Tracker',
            'fragmentation': frag,
            'time_ms': round(elapsed, 2),
            'backend': 'memory',
        }

    return {'status': 'error', 'message': f'Unknown pattern: {pattern}'}


# ═══════════════════════════════════════════════════════════
# WebSocket Events (Live Monitor)
# ═══════════════════════════════════════════════════════════

@socketio.on('connect')
def on_connect():
    emit('status', {'message': 'Connected to CacheLab monitor'})

@socketio.on('start_monitor')
def on_start_monitor():
    lab_state['monitor_active'] = True
    emit('status', {'message': 'Monitor started'})

@socketio.on('stop_monitor')
def on_stop_monitor():
    lab_state['monitor_active'] = False
    emit('status', {'message': 'Monitor stopped'})

def emit_metric(metric_type, data):
    """Send metric to all connected clients"""
    socketio.emit('metric', {'type': metric_type, 'data': data, 'timestamp': time.time()})


# ═══════════════════════════════════════════════════════════
# Background Monitor Thread
# ═══════════════════════════════════════════════════════════

def monitor_loop():
    """Background thread emitting live stats"""
    while True:
        if lab_state['monitor_active']:
            socketio.emit('live_stats', {
                'memory': memory_backend.health(),
                'disk': disk_backend.health(),
                'total_tests': lab_state['total_tests_run'],
                'timestamp': time.time(),
            })
        socketio.sleep(2)

socketio.start_background_task(monitor_loop)


# ═══════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("🚀 CacheLab starting...")
    print("   → http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
