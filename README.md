<div align="center">

# 🤖 Multi-Robot Warehouse System
### 多机器人仓储系统

*A simulation platform for multi-robot warehouse management*
*企业级多机器人仓库管理仿真平台*

![Python](https://img.shields.io/badge/Python-3.7+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey)
![Three.js](https://img.shields.io/badge/Three.js-r128-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

</div>

---

## What is this? | 这是什么？

A full-stack warehouse simulation system where multiple robots autonomously pick up and deliver orders — with real-time 3D visualization, intelligent scheduling, and a complete REST API.

多机器人仓库仿真系统，机器人自主接单、规划路径、执行配送，支持实时3D可视化与智能调度。

---

## Features | 核心功能

**3D Visualization** — WebGL-based 60 FPS rendering, free camera control, live robot status

**2D Dashboard** — Order monitoring, robot tracking, performance metrics

**Scheduling Algorithms** — A\* path planning + multi-objective task assignment

**REST API** — 10 endpoints for full simulation control

**Dynamic Orders** — Priority-based generation with urgency scoring

---

## Quick Start | 快速开始

```bash
# 1. Install dependencies | 安装依赖
cd backend && pip install -r requirements.txt

# 2. Start backend | 启动后端 (Terminal 1)
cd backend && python app.py

# 3. Start frontend | 启动前端 (Terminal 2)
cd frontend && python -m http.server 8000
```

Open in browser | 浏览器打开: `http://localhost:8000`

---

## Project Structure | 项目结构

```
warehouse_system/
├── backend/
│   ├── app.py              # Flask REST API server
│   ├── simulator.py        # Core simulation engine
│   ├── scheduler.py        # A* path planning & task assignment
│   ├── robot.py            # Robot fleet management
│   ├── order.py            # Order generation & tracking
│   └── requirements.txt
└── frontend/
    ├── home.html           # Navigation hub
    ├── 3d-dashboard.html   # 3D visualization
    └── dashboard.html      # 2D data dashboard
```

---

## Algorithm Overview | 算法说明

**Task Assignment | 任务分配**
```
cost = distance × 0.40 + queue_time × 0.35 + workload × 0.25
```

**Path Planning | 路径规划** — A\* with Manhattan distance heuristic + space-time collision avoidance

**Order Priority | 订单优先级** — Combines priority level, waiting time, and deadline proximity

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
| `/api/simulation/step` | POST | Step by 1s |
| `/api/simulation/reset` | POST | Reset to initial state |

---

## Roadmap | 开发计划

| Phase | Content | Status |
|-------|---------|--------|
| 1 | Core simulation & 2D visualization | ✅ Complete |
| 2 | 3D visualization | ✅ Complete |
| 3 | Algorithm visualization & WebSocket | 🔄 In progress |
| 4 | VR/AR integration | 📆 Planned |

---

<div align="center">

MIT License · Made by lumos1028

</div>
