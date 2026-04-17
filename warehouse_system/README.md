# Multi-Robot Warehouse System | 多机器人仓储系统

A simulation platform for multi-robot warehouse management, featuring real-time 3D visualization, intelligent scheduling algorithms, and a complete REST API.

企业级多机器人仓库管理仿真平台，支持实时3D可视化、智能调度算法与完整REST API。

---

## Features | 功能特性

- **3D Visualization** — WebGL-based 60 FPS real-time rendering with free camera control
- **2D Dashboard** — Order monitoring, robot status tracking, and performance metrics
- **Scheduling Algorithms** — A\* path planning + multi-objective task assignment (distance, workload, queue time)
- **REST API** — 10 endpoints for simulation control and data retrieval
- **Dynamic Orders** — Priority-based order generation with urgency scoring

---

## Quick Start | 快速开始

**Requirements:** Python 3.7+, pip

```bash
# 1. Install dependencies
cd backend && pip install -r requirements.txt

# 2. Start backend (Terminal 1)
cd backend && python app.py

# 3. Start frontend server (Terminal 2)
cd frontend && python -m http.server 8000
```

Open in browser: `http://localhost:8000`

---

## Project Structure | 项目结构

```
warehouse_system/
├── backend/
│   ├── app.py           # Flask REST API server
│   ├── simulator.py     # Core simulation engine
│   ├── scheduler.py     # A* path planning & task assignment
│   ├── robot.py         # Robot fleet management
│   ├── order.py         # Order generation & tracking
│   └── requirements.txt
└── frontend/
    ├── home.html        # Navigation hub
    ├── 3d-dashboard.html  # 3D visualization
    └── dashboard.html   # 2D data dashboard
```

---

## API Reference | API 文档

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | Full system state |
| `/api/robots` | GET | Robot fleet status |
| `/api/orders` | GET | All orders |
| `/api/metrics` | GET | Performance metrics |
| `/api/grid` | GET | Map grid + robot positions |
| `/api/simulation/start` | POST | Start simulation |
| `/api/simulation/pause` | POST | Pause simulation |
| `/api/simulation/step` | POST | Step simulation by 1s |
| `/api/simulation/reset` | POST | Reset to initial state |

---

## Algorithm Overview | 算法说明

**Task Assignment** uses a weighted cost function:

```
cost = distance × 0.40 + queue_time × 0.35 + workload × 0.25
```

**Path Planning** uses A\* with Manhattan distance heuristic and space-time collision avoidance.

**Order Priority** scoring combines priority level, waiting time, and deadline proximity.

---

## Roadmap | 开发计划

| Phase | Content | Status |
|-------|---------|--------|
| 1 | Core simulation & 2D visualization | Complete |
| 2 | 3D visualization | Complete |
| 3 | Algorithm visualization & WebSocket | In progress |
| 4 | VR/AR integration | Planned |

---

## License

MIT
