# 🚀 使用指南 - 多机器人仓储系统

## 快速概览

您已获得一个**完整可用的多机器人仓储系统**，包含：
- ✅ **4个核心模块**（环境、机器人、订单、调度）
- ✅ **高级算法**（A*路径规划、多目标优化）
- ✅ **完整前端**（实时可视化、交互控制）
- ✅ **REST API**（10个端点）
- ✅ **充分测试**（所有模块已验证）

---

## ⚡ 立即启动（3种方式）

### 🖥️ 方式1：最快（推荐）

```bash
cd /Users/fanyue/operational\ research/warehouse_system
./run.sh                    # macOS/Linux
# 或 run.bat               # Windows
```

然后打开浏览器：`frontend/index.html`

### 🔧 方式2：手动安装

```bash
# 1. 进入后端目录
cd backend

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动后端
python app.py
# 看到这个说明成功: * Running on http://0.0.0.0:5000

# 4. 在另一个终端窗口打开前端
# 在浏览器打开: frontend/index.html
```

### ✅ 方式3：验证安装

```bash
cd backend
python test.py
# 看到所有测试通过 ✅
```

---

## 📂 文件说明

| 文件 | 说明 | 优先级 |
|------|------|--------|
| **backend/app.py** | Flask REST API服务器 | 🔴必须 |
| **frontend/index.html** | 网页可视化界面 | 🔴必须 |
| **backend/scheduler.py** | 核心调度算法 | 🔴必须 |
| **backend/environment.py** | 环境建模 | 🟡重要 |
| **backend/robot.py** | 机器人系统 | 🟡重要 |
| **backend/order.py** | 订单系统 | 🟡重要 |
| **backend/simulator.py** | 系统模拟器 | 🟡重要 |
| **backend/config.py** | 配置参数 | 🟢可选 |
| **backend/test.py** | 单元测试 | 🟢可选 |

---

## 🎮 使用步骤

### 1️⃣ 启动系统

```bash
# 终端1：启动后端
cd backend && python app.py

# 输出: * Running on http://0.0.0.0:5000
```

### 2️⃣ 打开前端

在浏览器中打开：
```
/Users/fanyue/operational research/warehouse_system/frontend/index.html
```

或者用Python临时服务器：
```bash
cd frontend
python -m http.server 8000
# 然后访问 http://localhost:8000
```

### 3️⃣ 操作界面

```
┌─────────────────────────────────────────────┐
│  🤖 多机器人仓储系统可视化                    │
├─────────────────┬─────────────────────────┤
│                 │                         │
│   🏭 仓库地图    │   ⏱ ▶ ⏸ ⏭ 🔄 控制按钮  │
│  (Canvas绘制)   │                         │
│  机器人实时位置  │   📊 系统指标           │
│                 │   🤖 机器人列表         │
│                 │   🎨 图例               │
│                 │                         │
└─────────────────┴─────────────────────────┘
```

### 4️⃣ 主要操作

| 按钮 | 功能 | 说明 |
|------|------|------|
| **▶ 启动** | 开始实时模拟 | 后台自动运行，机器人开始执行任务 |
| **⏸ 暂停** | 暂停模拟 | 暂停所有动作 |
| **⏭ 单步** | 执行一步 | 手动推进模拟1秒 |
| **🔄 重置** | 重置系统 | 回到初始状态 |

---

## 📊 监控信息

### 左上：时间显示
```
⏱ 时间: 25.3s
```

### 左中：系统指标
```
📊 系统指标
├─ 总机器人数: 5
├─ 空闲机器人: 2
├─ 待分配订单: 3
├─ 总行驶距离: 145.8 m
├─ 已完成任务: 12
└─ 平均电量: 87%
```

### 左下：机器人列表
```
🤖 机器人状态
├─ 机器人 #1 [空闲]
│  位置: (15, 22)
│  负载: 0/100
│  任务队列: 1
│  已完成: 3
│  电量: ▰▰▰▰▱ 95%
│
├─ 机器人 #2 [移动]
│  ...
```

### 中间：地图
```
地图元素说明：
- 黄色区域  = 通道（可通行）
- 黑色区域  = 货架（障碍物）
- 绿色区域  = 充电站
- 粉色区域  = 拣货区
- 蓝色圆点  = 机器人

机器人颜色指示：
- 绿色光圈  = 空闲
- 黄色光圈  = 忙碌
- 蓝色光圈  = 移动
- 红色光圈  = 充电
```

---

## 🔧 自定义配置

编辑 `backend/config.py` 调整参数：

### 修改机器人数量
```python
ROBOT_CONFIG = {
    'num_robots': 10,  # 改为10个机器人
}
```

### 修改订单生成频率
```python
ORDER_CONFIG = {
    'base_generation_interval': 0.5,  # 改为每0.5秒生成一个订单
}
```

### 修改任务分配权重
```python
SCHEDULER_CONFIG = {
    'cost_weights': {
        'distance': 0.3,      # 降低距离权重
        'queue_time': 0.4,    # 提高队列权重
        'workload': 0.3,      # 提高负载权重
    }
}
```

修改后重启后端即可生效。

---

## 🌐 API 调用示例

### 获取系统状态
```bash
curl http://localhost:5000/api/status
```

### 获取所有机器人
```bash
curl http://localhost:5000/api/robots
```

### 启动模拟
```bash
curl -X POST http://localhost:5000/api/simulation/start
```

### 执行一步
```bash
curl -X POST http://localhost:5000/api/simulation/step \
  -H "Content-Type: application/json" \
  -d '{"delta_time": 1.0}'
```

---

## 🐛 常见问题

### ❌ 后端无法启动

**症状**: `Address already in use`

**解决**:
```bash
# 查找占用5000端口的进程
lsof -i :5000

# 杀死该进程
kill -9 <PID>

# 重新启动
python app.py
```

### ❌ 前端显示空白

**症状**: Canvas区域无内容

**解决**:
1. 硬刷新浏览器：`Cmd+Shift+R` (Mac) 或 `Ctrl+Shift+R` (Win)
2. 检查后端是否正常运行
3. 打开浏览器控制台 (F12) 查看错误信息

### ❌ 无法连接到后端

**症状**: 前端报Connection错误

**解决**:
1. 确保后端已启动: `python app.py`
2. 确认端口是5000
3. 查看防火墙设置
4. 试试 `http://127.0.0.1:5000` 而不是 `localhost`

### ❌ 模块导入失败

**症状**: `ModuleNotFoundError: No module named 'numpy'`

**解决**:
```bash
pip install -r requirements.txt
```

---

## 📚 深入学习

### 理解核心算法

**A*路径规划** - 查看 `scheduler.py` 中的 `PathPlanner.plan_path()`
- 用于找到在障碍物中的最短路径
- 合并实际距离(g) + 估计距离(h)
- 时间复杂度 O(log n)

**任务分配** - 查看 `scheduler.py` 中的 `Scheduler.select_best_robot()`
- 多目标加权优化
- 权重：距离(40%) + 队列(35%) + 负载(25%)
- 选择成本最低的机器人

**订单优先级** - 查看 `order.py` 中的 `Order.get_urgency_score()`
- 考虑优先级和等待时间
- 老的订单优先级提高
- 高优先级订单优先分配

### 修改代码示例

#### 添加新的优化目标

在 `scheduler.py` 中修改成本计算：
```python
def calculate_assignment_cost(self, robot, order, current_time):
    # ... 现有代码 ...
    
    # 新增：添加距离充电站的距离
    charge_dist = self.environment.manhattan_distance(
        (robot.x, robot.y), 
        nearest_charging_station
    )
    
    composite_cost = (
        distance * 0.3 +      # 降低距离权重
        queue_time * 0.3 +    # 保持队列权重
        workload * 0.2 +      # 降低负载权重
        charge_dist * 0.2     # 新增充电距离权重
    )
    
    return composite_cost
```

#### 修改邻接移动方式

在 `environment.py` 中改为8向移动：
```python
def get_neighbors(self, x: int, y: int):
    neighbors = []
    # 4向 + 4对角线 = 8向移动
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if self.is_walkable(nx, ny):
                neighbors.append((nx, ny))
    return neighbors
```

---

## 📈 性能优化建议

### 对于大规模系统（>100机器人）

1. **算法优化**
   - 使用启发式剪枝加速A*
   - 实现路径缓存减少重复计算

2. **系统架构**
   - 使用缓存（Redis）存储频繁查询
   - 分离重型计算到后台任务队列

3. **数据库**
   - 部署PostgreSQL存储历史数据
   - 建立索引加速查询

---

## 💡 实验建议

### 实验1：测试不同机器人数量的影响

```python
# config.py
for num_robots in [1, 3, 5, 10, 20]:
    ROBOT_CONFIG['num_robots'] = num_robots
    # 运行并观察完成时间和行驶距离
```

### 实验2：调整权重比例

```python
# 测试不同的权重组合
weights_combinations = [
    {'distance': 0.5, 'queue_time': 0.3, 'workload': 0.2},
    {'distance': 0.3, 'queue_time': 0.5, 'workload': 0.2},
    {'distance': 0.2, 'queue_time': 0.3, 'workload': 0.5},
]
```

### 实验3：观察电池和充电影响

```python
# config.py - 修改电池参数
ROBOT_CONFIG = {
    'max_battery': 50.0,              # 降低最大电量
    'battery_consumption_rate': 0.2,  # 增加消耗率
    'charging_rate': 1.0,             # 加快充电
}
```

---

## 📞 获取帮助

### 查看文档
- `README.md` - 完整技术文档
- `QUICKSTART.md` - 快速指南和故障排除
- `PROJECT_SUMMARY.md` - 项目总结和学习资源

### 阅读代码注释
所有Python文件都有详细的文档字符串和注释。

### 运行测试
```bash
cd backend && python test.py
```

---

## 🎯 预期使用场景

✅ **适合场景**:
- 学习多机器人系统设计
- 理解路径规划和调度算法
- 研究运筹学优化问题
- 原型开发和演示
- 教学和培训

⚠️ **限制因素**:
- 仅限于单个50×50网格
- 最多几十个机器人（更多需要优化）
- 模拟而非真实物理

---

## 🏁 完成清单

- [x] 后端API运行
- [x] 前端界面显示
- [x] 模拟启动和工作
- [x] 机器人在移动
- [x] 订单在分配
- [x] 指标在更新
- [x] 所有功能正常

**祝贺！** 您的系统已完全可用！ 🎉

---

**最后提示**: 先用默认配置运行几分钟，感受系统的工作方式，然后再尝试修改参数进行实验。

祝您使用愉快！ 🚀
