# 多机器人仓储系统 - 快速开始指南

**版本**: v2.1-stable  
**更新**: 2026-04-17  
**阅读时间**: 5分钟

---

## ⚡ 30秒快速启动

### 最小启动流程

```bash
# 终端1: 启动后端
cd backend && python3 app.py

# 终端2: 启动前端 (可选)
cd frontend && python3 -m http.server 8000

# 浏览器访问
http://localhost:8000
```

**完成**: 仓库系统已启动、3D可视化就绪 ✅

---

## 📋 前置要求

### 必需
- ✅ Python 3.7+
- ✅ 现代浏览器 (Chrome/Safari/Firefox)
- ✅ 网络连接 (CDN资源加载)

### 可选
- Node.js 12+ (如用npm代替python启动前端)
- Git (版本控制)

### 系统资源
- 内存: 最少 4GB, 推荐 8GB
- CPU: 任意现代处理器
- 磁盘: 50MB

---

## 🚀 完整安装步骤

### 1️⃣ 克隆或下载项目

```bash
# 如已有项目目录，跳过此步
git clone <repo-url> warehouse_system
cd warehouse_system
```

### 2️⃣ 检查目录结构

```bash
warehouse_system/
├── backend/
│   ├── app.py           ← Flask主应用
│   ├── simulator.py      ← 仓库模拟器
│   ├── robot.py          ← 机器人类
│   └── order.py          ← 订单类
├── frontend/
│   ├── home.html         ← 首页
│   ├── dashboard.html    ← 2D仪表板
│   ├── 3d-dashboard.html ← 3D可视化 ⭐
│   └── assets/           ← CSS/JS资源
└── README.md             ← 项目说明
```

### 3️⃣ 安装后端依赖

```bash
cd backend

# 创建虚拟环境 (推荐)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install flask flask-cors
```

**验证**:
```bash
python3 -c "import flask; print(flask.__version__)"
# 输出: 2.3.x
```

### 4️⃣ 启动后端服务

```bash
python3 app.py

# 预期输出:
# WARNING: This is a development server. Do not use it in production.
# Running on http://127.0.0.1:5001
```

✅ 后端就绪 - 保持此终端运行

### 5️⃣ 打开前端 (选择一种方式)

#### 方式A: 使用Python简易服务器 (推荐)
```bash
# 新建终端，不关闭后端
cd frontend
python3 -m http.server 8000

# 访问: http://localhost:8000
```

#### 方式B: 直接打开文件
```bash
# 在浏览器中打开文件
file:///Users/fanyue/operational\ research/warehouse_system/frontend/home.html
```

#### 方式C: 使用Node.js (如已安装)
```bash
cd frontend
npx http-server -p 8000
```

---

## 🎮 使用说明

### 首页导航
访问 `http://localhost:8000` 后，看到首页菜单：

| 链接 | 功能 | 说明 |
|------|------|------|
| **2D仪表板** | dashboard.html | 实时数据监控 (订单/机器人/指标) |
| **3D可视化** | 3d-dashboard.html | 虚拟仓库环境 (⭐推荐) |

### 3D仪表板详解

#### UI布局
```
┌─────────────────────────────────────┐
│  系统状态 Panel                │ 机器人列表 Panel │
├─────────────────────────────────────┤
│                                     │
│        3D 仓库场景 (中心)          │
│        • 50m×50m虚拟空间          │
│        • 12个货架                  │
│        • 3个充电站                 │
│        • 5个机器人                 │
│                                     │
├─────────────────────────────────────┤
│  图例 Panel                  │ 帮助信息 Panel     │
└─────────────────────────────────────┘
```

#### 控制按钮
```
控制区按钮:
┌──────────────────────────────┐
│ ▶ 启动  │ ⏸ 暂停  │ 🔄 重置 │ ⏭ 步进 │
└──────────────────────────────┘

功能:
• ▶ 启动: 开始仓库模拟
• ⏸ 暂停: 暂停仓库运行
• 🔄 重置: 恢复初始状态
• ⏭ 步进: 单步执行 (暂停时可用)
```

#### 相机操作
```
🖱️ 鼠标控制:
• 左键拖拽: 旋转视角
• 滚轮: 缩放距离 (20-150m)

⌨️ 键盘快捷键:
• Space: 重置视角到默认位置
```

#### 颜色代码
```
🟦 蓝色: 机器人空闲 (IDLE)
🟥 红色: 机器人移动中或繁忙
🟨 黄色: 机器人充电中 (CHARGING)
⬜ 灰色: 货架/充电站 (静态)
```

#### 信息面板说明

**系统状态 (左上)**
```
运行时间: 显示模拟已运行秒数
模拟速度: 实际/虚拟时间比 (1x, 10x等)
总订单数: 已处理/待处理
平均效率: 订单完成效率百分比
```

**机器人列表 (右上)**
```
显示5个机器人:
R1-R5

每个显示:
• 名称
• 状态 (IDLE/MOVING/CHARGING)
• 电量 (百分比)
• 坐标 (x, y位置)
```

**图例 (左下)**
```
颜色含义速查表
• 蓝=待命
• 红=工作
• 黄=充电
```

**帮助 (右下)**
```
一句话操作提示
鼠标+键盘快捷方式速查
```

---

## 📊 2D仪表板说明

访问 `http://localhost:8000/dashboard.html`

### 数据分类
```
订单数据区:
├─ 总订单数
├─ 处理中订单
├─ 已完成订单
└─ 平均响应时间

机器人数据区:
├─ 在线机器人
├─ 电池充电中
├─ 平均电量
└─ 工作效率

系统指标区:
├─ 吞吐量 (订单/小时)
├─ 可用性 (%)
├─ 响应时间 (秒)
└─ 成本效益
```

### 更新频率
- 自动刷新: **500ms**
- 计算延迟: **<100ms**
- 显示延迟: **<150ms**

---

## ⚙️ 配置调整

### 后端配置

编辑 `backend/app.py`:

#### 改变监听端口
```python
# 第47行左右
app.run(host='0.0.0.0', port=5001)  # ← 改5001为需要的端口
```

#### 改变仓库大小
编辑 `backend/simulator.py`:
```python
# 第XX行
self.width = 50    # 改为需要的宽度
self.height = 50   # 改为需要的高度
```

#### 改变机器人数量
编辑 `backend/simulator.py`:
```python
# 第YY行
robots = [Robot(...) for _ in range(5)]  # 改5为需要的数量
```

### 前端配置

编辑 `frontend/3d-dashboard.html`:

#### 改变API服务器地址
```javascript
// 约第50行
const API_URL = 'http://localhost:5001';  // ← 改为实际地址
```

#### 改变更新频率
```javascript
// 约第60行
const UPDATE_INTERVAL = 500;  // 改为毫秒数 (建议200-1000)
```

#### 改变视角默认位置
```javascript
// SimpleCamera类定义处
this.theta = Math.PI / 4;   // 水平角
this.phi = Math.PI / 3;     // 垂直角  
this.radius = 60;           // 距离
```

---

## 🐛 常见问题解决

### Q1: 浏览器显示"无法连接到服务器"

**症状**: 3D页面全黑，控制台错误 `Cannot GET /`

**原因**: 前端服务器未启动或地址不对

**解决**:
```bash
# 确保在frontend目录
cd frontend
python3 -m http.server 8000

# 然后访问 http://localhost:8000
```

### Q2: 3D场景不渲染，只显示UI面板

**症状**: 中央是黑色，只能看到4个角落的UI

**原因**: Canvas被遮挡或Three.js库加载失败

**解决**:
```bash
# 1. 打开浏览器控制台 (F12)
# 2. 查看Network标签
# 检查是否有红色标记 (加载失败)
# 3. 检查Console标签是否有错误信息
```

如果看到 `THREE is not defined`:
```bash
# 原因: Three.js库加载失败
# 解决: 检查网络连接，CDN是否可用
# 备选: 在 header 中改用本地Three.js库
```

### Q3: 后端启动失败 `Address already in use`

**症状**: `ERROR: Address already in use`

**原因**: 端口5001被占用

**解决**:
```bash
# macOS/Linux: 查找并杀死占用进程
lsof -i :5001
kill -9 <PID>

# Windows: 
netstat -ano | findstr :5001
taskkill /PID <PID> /F

# 或改用其他端口
python3 app.py --port 5002
```

### Q4: 机器人不动

**症状**: 各项数据显示但机器人不移动

**原因**: 系统未启动仿真

**解决**:
```
1. 检查系统状态面板
2. 点击 ▶ 启动按钮
3. 观察"运行时间"是否增加
4. 查看机器人状态是否变化
```

### Q5: 页面卡顿/FPS低

**症状**: 移动鼠标或旋转视角时明显延迟

**原因**:  
- 浏览器性能问题
- 机器人数量过多
- 分辨率过高

**解决**:
```
1. 关闭其他浏览器标签页
2. 关闭浏览器插件
3. 清除缓存并刷新
4. 尝试不同浏览器
5. 减少机器人数量进行测试
```

---

## 📱 不同设备适配

### 高级显示器 (2K+)
- ✅ 完全支持
- 建议分辨率: 2560×1440+
- 预期FPS: 60

### 标准显示器 (1080p)
- ✅ 良好支持
- 推荐分辨率: 1920×1080
- 预期FPS: 55-60

### 笔记本屏幕 (13-15")
- ✅ 可用支持
- 分辨率: 1366×768+
- 预期FPS: 45-55

### 移动设备 (平板)
- ⚠️ 部分支持
- 建议: iPad Air 2+ 或安卓旗舰
- 注意: 触摸控制需要改进

---

## 🎯 下一步

### 立即尝试
- [ ] 在3D环境中旋转视角
- [ ] 点击启动模拟观察机器人移动
- [ ] 切换到2D仪表板对比数据

### 深入学习
- 阅读 [PHASE2_FINAL.md](PHASE2_FINAL.md) 了解技术细节
- 阅读 [API文档](API_DOCS.md) 学习REST接口
- 查看源代码 - 300行注释清晰的JavaScript

### 定制扩展
- 修改仓库大小
- 增加机器人数量
- 改变颜色主题
- 添加自定义对象

---

## 📞 获取帮助

### 资源列表
| 文档 | 内容 | 链接 |
|------|------|------|
| README | 项目总览 | [→](../README.md) |
| PHASE2_IMPLEMENTATION_REPORT | 实现报告 | [→](PHASE2_IMPLEMENTATION_REPORT.md) |
| PHASE2_FINAL | 技术细节 | [→](PHASE2_FINAL.md) |

### 反馈渠道
- 📧 Email: [项目邮箱]
- 🐛 Issues: GitHub Issues
- 💬 Discussion: GitHub Discussions

---

**祝您使用愉快！** 🚀

**最后更新**: 2026-04-17  
**版本**: v2.1-stable

### 系统状态指示

**机器人状态颜色**:
- 🟢 **绿色光圈** = 空闲中
- 🟡 **黄色光圈** = 忙碌中
- 🔵 **蓝色光圈** = 移动中
- 🔴 **红色光圈** = 充电中

**地图元素**:
- 黄色区域 = 通道（可通行）
- 黑色区域 = 货架（障碍物）
- 绿色区域 = 充电站
- 粉色区域 = 拣货区

### 控制按钮

| 按钮 | 功能 |
|------|------|
| ▶ 启动 | 开始实时模拟 |
| ⏸ 暂停 | 暂停模拟 |
| ⏭ 单步 | 执行一步模拟（+1秒） |
| 🔄 重置 | 重置整个系统 |

### 实时监控

**左下方显示**:
- ⏱ 当前模拟时间
- 📊 系统性能指标
- 🤖 机器人详细状态（位置、负载、电量等）

**中间显示**:
- 🏭 仓库地图和机器人位置
- 📍 实时位置更新

## 🔧 自定义配置

编辑 `backend/config.py` 文件修改系统参数：

```python
# 修改机器人数量
ROBOT_CONFIG = {
    'num_robots': 10,  # 改为10个机器人
}

# 修改订单生成频率
ORDER_CONFIG = {
    'base_generation_interval': 0.5,  # 改为每0.5秒生成一个订单
}

# 修改任务分配权重
SCHEDULER_CONFIG = {
    'cost_weights': {
        'distance': 0.3,      # 降低距离权重
        'queue_time': 0.4,    # 提高队列时间权重
        'workload': 0.3,      # 提高负载权重
    }
}
```

## 📊 API 文档

### 查看完整API文档
所有API端点都支持跨域（CORS），可以从任何前端调用。

**基础URL**: `http://localhost:5000/api`

常用端点：
- `GET /status` - 获取完整系统状态
- `GET /robots` - 获取机器人列表
- `GET /orders` - 获取订单列表
- `GET /metrics` - 获取性能指标
- `POST /simulation/start` - 启动模拟
- `POST /simulation/pause` - 暂停模拟
- `POST /simulation/step` - 执行一步

## 🐛 故障排除

### 问题1: 无法连接到后端服务
**症状**: 前端显示连接错误  
**解决方案**:
- 确保后端已启动: `python app.py`
- 检查是否运行在正确的端口: `http://localhost:5000`
- 检查防火墙设置

### 问题2: 模块导入错误
**症状**: `ModuleNotFoundError: No module named 'numpy'`  
**解决方案**:
```bash
pip install -r requirements.txt
```

### 问题3: 前端canvas不显示
**症状**: 仓库地图区域为空  
**解决方案**:
- 硬刷新浏览器: `Ctrl+Shift+R` (Win/Linux) 或 `Cmd+Shift+R` (Mac)
- 检查浏览器控制台错误: F12 → Console
- 确保后端API可以访问

### 问题4: 性能缓慢
**症状**: 机器人移动卡顿，界面反应慢  
**解决方案**:
- 减少机器人数量（修改 `config.py`）
- 降低模拟更新频率
- 关闭其他浏览器标签页

## 📈 性能优化建议

### 对于大规模部署
1. **增加服务器资源**
   - 运行在更强大的硬件上
   - 使用多进程/多线程处理

2. **优化算法**
   - 使用缓存优化A*算法
   - 批量处理订单

3. **扩展后端**
   - 部署多个后端实例
   - 使用消息队列（RabbitMQ）
   - 数据库持久化

## 🎓 学习资源

### 核心算法
- **A*路径规划**: 查看 `scheduler.py` 中的 `PathPlanner` 类
- **任务分配**: 查看 `scheduler.py` 中的 `Scheduler.select_best_robot()` 方法
- **订单系统**: 查看 `order.py` 中的优先级和紧迫性计算

### 进阶主题
- 修改启发式函数（曼哈顿 → 欧氏距离）
- 实现多目标优化（Pareto前沿）
- 添加动态障碍物避免
- 实现分布式调度

## 📞 获取帮助

如有问题：
1. 查看 `README.md` 了解完整文档
2. 运行 `python test.py` 验证安装
3. 检查 `backend/config.py` 了解可配置参数
4. 查看浏览器控制台（F12）的错误信息

## 🌟 下一步

现在系统已经设置完成！您可以：

1. ✅ **启动模拟** 观察系统运行
2. 📊 **调整参数** 进行实验
3. 🔧 **扩展功能** 添加新的调度算法
4. 📈 **分析性能** 优化系统效率

祝你使用愉快！🎉
