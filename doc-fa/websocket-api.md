# WebSocket API

CacheLab uses Flask-SocketIO for real-time communication between the server and clients.

## Connection

```javascript
const socket = io();

socket.on('connect', () => {
    console.log('Connected to CacheLab monitor');
});
```

## Events (Client → Server)

### Start Monitor

```javascript
socket.emit('start_monitor');
```

### Stop Monitor

```javascript
socket.emit('stop_monitor');
```

## Events (Server → Client)

### Status

```javascript
socket.on('status', (data) => {
    console.log(data.message);
});
```

### Live Stats

```javascript
socket.on('live_stats', (data) => {
    console.log('Memory:', data.memory);
    console.log('Disk:', data.disk);
    console.log('Total Tests:', data.total_tests);
});
```

### Metric

```javascript
socket.on('metric', (data) => {
    console.log('Type:', data.type);
    console.log('Data:', data.data);
});
```

## Live Stats Data Format

```json
{
    "memory": {
        "type": "memory",
        "size": 42,
        "maxsize": 1000,
        "status": "healthy"
    },
    "disk": {
        "type": "disk",
        "size": 5,
        "status": "healthy"
    },
    "total_tests": 15,
    "timestamp": 1726175823.456
}
```

## Metric Types

| Type | Description |
|---|---|
| `test_complete` | A core test finished |
| `benchmark_complete` | Benchmark suite finished |

## Client Integration Example

```html
<script src="https://cdn.socket.io/4.7.4/socket.io.min.js"></script>
<script>
    const socket = io();
    
    socket.on('connect', () => {
        console.log('Connected!');
        socket.emit('start_monitor');
    });
    
    socket.on('live_stats', (data) => {
        document.getElementById('memory-size').textContent = data.memory.size;
    });
</script>
```
