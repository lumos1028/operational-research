# REST API 完整参考文档

**版本**: v2.1-stable  
**基础URL**: `http://localhost:5001`  
**内容类型**: `application/json`  
**更新**: 2026-04-17

---

## 📋 目录

1. [系统状态API](#系统状态api)
2. [机器人API](#机器人api)
3. [订单API](#订单api)
4. [指标API](#指标api)
5. [仿真控制API](#仿真控制api)
6. [数据格式](#数据格式)
7. [错误处理](#错误处理)
8. [示例](#示例)

---

## 系统状态API

### GET /api/status

获取完整的系统状态快照

**请求**:
```http
GET /api/status HTTP/1.1
Host: localhost:5001
```

**响应** (200 OK):
```json
{
  "running": true,
  "time": 1234.5,
  "total_orders": 45,
  "completed_orders": 38,
  "pending_orders": 7,
  "robots": [
    {
      "id": "R1",
      "x": 10.5,
      "y": 15.3,
      "status": "moving",
      "battery": 85.0,
      "current_task": "ORDER_123",
      "task_queue_length": 2,
      "efficiency": 0.92
    }
    // ... 更多机器人
  ],
  "orders": [
    {
      "id": "ORDER_123",
      "status": "in_progress",
      "priority": "HIGH",
      "robot_assigned": "R1",
      "created_at": 1000.0,
      "deadline": 1300.0,
      "pickup_location": {"x": 5, "y": 10},
      "delivery_location": {"x": 30, "y": 40}
    }
    // ... 更多订单
  ],
  "shelves": [
    {"id": 0, "x": 5, "y": 5, "width": 3, "height": 8},
    // ... 12个货架
  ],
  "charging_stations": [
    {"id": 0, "x": 45, "y": 5},
    {"id": 1, "x": 45, "y": 25},
    {"id": 2, "x": 45, "y": 45}
  ]
}
```

**参数**: 无

**错误**:
- `500`: 服务器错误

**使用场景**: 获取系统完整快照用于UI渲染

---

## 机器人API

### GET /api/robots

获取所有机器人的详细信息

**请求**:
```http
GET /api/robots HTTP/1.1
Host: localhost:5001
```

**响应** (200 OK):
```json
{
  "robots": [
    {
      "id": "R1",
      "position": {"x": 10.5, "y": 15.3},
      "status": "idle",
      "battery_level": 85.0,
      "current_order": null,
      "task_queue": ["ORDER_124", "ORDER_125"],
      "task_queue_length": 2,
      "efficiency_score": 0.92,
      "total_distance": 1245.6,
      "orders_completed": 38,
      "last_update": 1234.5
    },
    {
      "id": "R2",
      "position": {"x": 25.0, "y": 30.0},
      "status": "charging",
      "battery_level": 45.0,
      "current_order": null,
      "task_queue": [],
      "task_queue_length": 0,
      "efficiency_score": 0.88,
      "total_distance": 1102.3,
      "orders_completed": 35,
      "last_update": 1234.4
    }
    // ... R3-R5
  ],
  "total_robots": 5,
  "active_robots": 4,
  "idle_robots": 1,
  "charging_robots": 1
}
```

**参数**: 
- `status` (可选): 过滤机器人状态 (idle, moving, busy, charging)

**示例**:
```
GET /api/robots?status=charging
```

**错误**:
- `500`: 服务器错误

---

### GET /api/robots/{robot_id}

获取单个机器人的详细信息

**请求**:
```http
GET /api/robots/R1 HTTP/1.1
Host: localhost:5001
```

**响应** (200 OK):
```json
{
  "id": "R1",
  "position": {"x": 10.5, "y": 15.3},
  "status": "moving",
  "battery_level": 85.0,
  "current_order": "ORDER_123",
  "task_queue": ["ORDER_124", "ORDER_125"],
  "stats": {
    "total_distance": 1245.6,
    "orders_completed": 38,
    "efficiency_score": 0.92,
    "average_queue_length": 1.8,
    "last_charged": 100.5
  }
}
```

**参数**: 无

**错误**:
- `404`: 机器人未找到
- `500`: 服务器错误

---

## 订单API

### GET /api/orders

获取所有订单的列表

**请求**:
```http
GET /api/orders HTTP/1.1
Host: localhost:5001
```

**响应** (200 OK):
```json
{
  "orders": [
    {
      "id": "ORDER_001",
      "status": "completed",
      "priority": "HIGH",
      "customer_id": "CUST_001",
      "items": 5,
      "robot_assigned": "R1",
      "created_at": 1000.0,
      "assigned_at": 1010.0,
      "completed_at": 1200.0,
      "deadline": 2000.0,
      "pickup_location": {"x": 5, "y": 10},
      "delivery_location": {"x": 30, "y": 40},
      "distance": 45.6,
      "processing_time": 200.0,
      "wait_time": 10.0,
      "fulfillment_time": 190.0
    },
    {
      "id": "ORDER_002",
      "status": "in_progress",
      "priority": "MEDIUM",
      "customer_id": "CUST_002",
      "items": 3,
      "robot_assigned": "R2",
      "created_at": 1150.0,
      "assigned_at": 1160.0,
      "completed_at": null,
      "deadline": 2200.0,
      "pickup_location": {"x": 10, "y": 20},
      "delivery_location": {"x": 35, "y": 35},
      "distance": 35.4,
      "processing_time": null,
      "wait_time": 10.0,
      "fulfillment_time": null
    }
    // ... 更多订单
  ],
  "total_orders": 45,
  "status_breakdown": {
    "pending": 7,
    "assigned": 2,
    "in_progress": 3,
    "completed": 33
  }
}
```

**参数**:
- `status` (可选): 过滤订单状态 (pending, assigned, in_progress, completed)
- `priority` (可选): 过滤优先级 (LOW, MEDIUM, HIGH)
- `robot_id` (可选): 过滤指定机器人的订单
- `limit` (可选): 返回数量限制 (默认100)

**示例**:
```
GET /api/orders?status=in_progress&priority=HIGH
GET /api/orders?robot_id=R1&limit=10
```

**错误**:
- `500`: 服务器错误

---

### GET /api/orders/{order_id}

获取单个订单的详细信息

**请求**:
```http
GET /api/orders/ORDER_001 HTTP/1.1
Host: localhost:5001
```

**响应** (200 OK):
```json
{
  "id": "ORDER_001",
  "status": "completed",
  "priority": "HIGH",
  "customer_id": "CUST_001",
  "items": 5,
  "robot_assigned": "R1",
  "timeline": {
    "created_at": 1000.0,
    "assigned_at": 1010.0,
    "pickup_at": 1050.0,
    "delivery_at": 1200.0,
    "completed_at": 1200.0,
    "deadline": 2000.0
  },
  "locations": {
    "pickup": {"x": 5, "y": 10, "name": "Shelf_A1"},
    "delivery": {"x": 30, "y": 40, "name": "Station_B"}
  },
  "metrics": {
    "distance": 45.6,
    "processing_time": 200.0,
    "wait_time": 10.0,
    "fulfillment_time": 190.0,
    "deadline_met": true,
    "efficiency_score": 0.95
  }
}
```

**参数**: 无

**错误**:
- `404`: 订单未找到
- `500`: 服务器错误

---

## 指标API

### GET /api/metrics

获取系统性能指标

**请求**:
```http
GET /api/metrics HTTP/1.1
Host: localhost:5001
```

**响应** (200 OK):
```json
{
  "timestamp": 1234.5,
  "system": {
    "running": true,
    "uptime": 1234.5,
    "total_time_simulated": 1234.5
  },
  "orders": {
    "total": 45,
    "completed": 38,
    "pending": 7,
    "average_wait_time": 12.3,
    "average_processing_time": 185.6,
    "average_fulfillment_time": 197.9,
    "on_time_delivery_rate": 0.95,
    "throughput_per_hour": 110.2
  },
  "robots": {
    "total_robots": 5,
    "average_utilization": 0.78,
    "average_battery_level": 72.5,
    "total_distance": 6245.6,
    "average_efficiency": 0.90,
    "active_orders": 3,
    "idle_robots": 2
  },
  "performance": {
    "makespan": 1234.5,
    "total_distance": 6245.6,
    "average_distance_per_order": 138.8,
    "energy_efficiency": 0.88,
    "fleet_utilization": 0.78
  }
}
```

**参数**: 无

**错误**:
- `500`: 服务器错误

---

### GET /api/metrics/timeline

获取时间序列指标数据

**请求**:
```http
GET /api/metrics/timeline?hours=1 HTTP/1.1
Host: localhost:5001
```

**响应** (200 OK):
```json
{
  "data": [
    {
      "timestamp": 1000.0,
      "orders_completed": 0,
      "avg_wait_time": 0,
      "robot_utilization": 0.2,
      "system_throughput": 0
    },
    {
      "timestamp": 1100.0,
      "orders_completed": 8,
      "avg_wait_time": 15.3,
      "robot_utilization": 0.75,
      "system_throughput": 28.8
    }
    // ... 更多数据点
  ],
  "interval": 100,
  "samples": 12
}
```

**参数**:
- `hours` (可选): 过去几小时的数据 (默认1)
- `interval` (可选): 采样间隔秒数 (默认60)

**错误**:
- `500`: 服务器错误

---

## 仿真控制API

### POST /api/simulation/start

启动仓库仿真

**请求**:
```bash
curl -X POST http://localhost:5001/api/simulation/start
```

**响应** (200 OK):
```json
{
  "status": "started",
  "message": "Simulation started successfully",
  "timestamp": 1234.5
}
```

**参数**: 无

**错误**:
- `400`: 仿真已在运行
- `500`: 服务器错误

---

### POST /api/simulation/pause

暂停仓库仿真

**请求**:
```bash
curl -X POST http://localhost:5001/api/simulation/pause
```

**响应** (200 OK):
```json
{
  "status": "paused",
  "message": "Simulation paused successfully",
  "timestamp": 1234.5,
  "current_time": 1234.5
}
```

**参数**: 无

**错误**:
- `400`: 仿真未运行
- `500`: 服务器错误

---

### POST /api/simulation/reset

重置仓库仿真到初始状态

**请求**:
```bash
curl -X POST http://localhost:5001/api/simulation/reset
```

**响应** (200 OK):
```json
{
  "status": "reset",
  "message": "Simulation reset to initial state",
  "timestamp": 0.0,
  "total_orders": 0,
  "robots_reset": 5
}
```

**参数**: 无

**错误**:
- `500`: 服务器错误

---

### POST /api/simulation/step

执行仿真的一个时间步

**请求**:
```bash
curl -X POST http://localhost:5001/api/simulation/step
```

**响应** (200 OK):
```json
{
  "status": "stepped",
  "message": "Simulation stepped by 1 second",
  "current_time": 1.0,
  "orders_generated": 0,
  "orders_assigned": 0
}
```

**参数**: 无

**前置条件**: 仿真必须处于暂停状态

**错误**:
- `400`: 仿真正在运行
- `500`: 服务器错误

---

## 数据格式

### 机器人状态枚举
```
"idle"      - 机器人空闲，等待任务
"moving"    - 机器人正在移动到位置
"busy"      - 机器人正在执行任务
"charging"  - 机器人正在充电
```

### 订单状态枚举
```
"pending"       - 订单已生成，待分配
"assigned"      - 订单已分配给机器人
"in_progress"   - 机器人正在处理订单
"completed"     - 订单已完成
"cancelled"     - 订单已取消
```

### 优先级枚举
```
"LOW"       - 低优先级 (权重: 1.0)
"MEDIUM"    - 中优先级 (权重: 2.0)
"HIGH"      - 高优先级 (权重: 3.0)
"URGENT"    - 紧急优先级 (权重: 5.0)
```

### 位置对象
```json
{
  "x": 10.5,      // 水平坐标 (0-50)
  "y": 25.3,      // 竖直坐标 (0-50)
  "name": "Shelf_A1"  // 可选名称
}
```

---

## 错误处理

### 标准错误响应

```json
{
  "error": "Invalid request",
  "message": "Parameter 'status' must be one of: idle, moving, busy, charging",
  "status_code": 400,
  "timestamp": 1234.5
}
```

### HTTP 状态码

| 代码 | 含义 | 示例 |
|------|------|------|
| 200 | 成功 | `GET /api/robots` |
| 400 | 客户端错误 | 无效参数、重复启动 |
| 404 | 未找到 | 机器人/订单不存在 |
| 500 | 服务器错误 | 数据库错误、异常 |

### 常见错误

**400 Bad Request**
```json
{
  "error": "Invalid parameter",
  "message": "Unknown status: 'invalid'. Must be one of: idle, moving, busy, charging"
}
```

**404 Not Found**
```json
{
  "error": "Not found",
  "message": "Robot 'R99' not found"
}
```

**500 Internal Server Error**
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred. Please try again later."
}
```

---

## 示例

### 示例1: 获取系统状态并启动仿真

```bash
# 1. 获取当前状态
curl http://localhost:5001/api/status | jq .

# 2. 启动仿真
curl -X POST http://localhost:5001/api/simulation/start

# 3. 等待5秒
sleep 5

# 4. 获取更新的状态
curl http://localhost:5001/api/status | jq '.robots[0]'
```

输出:
```json
{
  "id": "R1",
  "x": 10.5,
  "y": 15.3,
  "status": "moving",
  "battery": 85.0,
  ...
}
```

### 示例2: 获取特定机器人的详细信息

```bash
curl http://localhost:5001/api/robots/R1 | jq .

# 过滤响应
curl http://localhost:5001/api/robots/R1 | jq '.stats'
```

### 示例3: 查询已完成的高优先级订单

```bash
curl 'http://localhost:5001/api/orders?status=completed&priority=HIGH' | jq '.orders | length'
```

### 示例4: 获取系统性能指标

```bash
curl http://localhost:5001/api/metrics | jq '.performance'

# 输出对战性能数据
curl http://localhost:5001/api/metrics | jq '
  {
    makespan: .performance.makespan,
    throughput: .orders.throughput_per_hour,
    on_time_rate: .orders.on_time_delivery_rate
  }'
```

输出:
```json
{
  "makespan": 1234.5,
  "throughput": 110.2,
  "on_time_rate": 0.95
}
```

### 示例5: JavaScript中使用API

```javascript
// 获取系统状态
async function getSystemStatus() {
  const response = await fetch('http://localhost:5001/api/status');
  const data = await response.json();
  return data;
}

// 启动仿真
async function startSimulation() {
  const response = await fetch('http://localhost:5001/api/simulation/start', {
    method: 'POST'
  });
  return response.json();
}

// 使用
getSystemStatus().then(data => {
  console.log(`Running robots: ${data.robots.length}`);
  console.log(`Pending orders: ${data.pending_orders}`);
});
```

---

## 性能指南

### 推荐的轮询间隔
- **UI更新**: 500ms
- **实时监控**: 1000ms
- **性能分析**: 5000ms

### 批量操作
```javascript
// ❌ 不推荐: 单个获取每个机器人
robots.forEach(r => fetch(`/api/robots/${r.id}`));

// ✅ 推荐: 一次获取所有机器人
fetch('/api/robots');
```

### 缓存策略
```javascript
// 缓存未更改的数据
let robotCache = null;
let cacheTime = 0;

async function getRobotsCached() {
  if (Date.now() - cacheTime < 500) {
    return robotCache;  // 返回缓存
  }
  robotCache = await fetch('/api/robots').then(r => r.json());
  cacheTime = Date.now();
  return robotCache;
}
```

---

## 版本控制

**当前版本**: v2.1-stable

**向后兼容性**: ✅ 是

**废弃API**: 无

**计划功能** (v3.0):
- WebSocket实时更新
- 批量操作端点
- 认证/授权
- 速率限制

---

**最后更新**: 2026-04-17  
**维护者**: [项目团队]  
**反馈**: 提交Issue或PR
