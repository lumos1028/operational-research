"""
配置文件 - 系统参数配置
"""

# ==================== 环境配置 ====================
ENVIRONMENT_CONFIG = {
    'width': 50,
    'height': 50,
    'grid_cell_size': 1,  # 每个网格单元大小
}

# ==================== 机器人配置 ====================
ROBOT_CONFIG = {
    'num_robots': 5,
    'max_capacity': 100,  # 最大容量
    'max_battery': 100.0,  # 最大电池容量
    'speed': 1.0,  # 移动速度（格子/秒）
    'battery_consumption_rate': 0.1,  # 电池消耗率（每格消耗）
    'charging_rate': 0.5,  # 充电速率（电量/秒）
    'low_battery_threshold': 20.0,  # 低电量阈值
    'critical_battery_threshold': 10.0,  # 临界电量阈值
}

# ==================== 订单配置 ====================
ORDER_CONFIG = {
    'base_generation_interval': 1.0,  # 基础订单生成间隔（秒）
    'generation_randomness': 0.5,  # 生成间隔随机偏差（±50%）
    'priority_distribution': {
        'LOW': 0.1,      # 10% 低优先级
        'MEDIUM': 0.5,   # 50% 中优先级
        'HIGH': 0.3,     # 30% 高优先级
    },
    'min_quantity': 1,
    'max_quantity': 10,
}

# ==================== 调度配置 ====================
SCHEDULER_CONFIG = {
    # 任务分配成本权重
    'cost_weights': {
        'distance': 0.4,        # 距离权重
        'queue_time': 0.35,     # 队列时间权重
        'workload': 0.25,       # 工作负载权重
    },
    
    # 任务完成时间估计
    'task_time_estimate': {
        'base_time': 10.0,      # 基础处理时间（秒）
        'per_task_time': 15.0,  # 每个任务预估时间（秒）
    },
    
    # A*算法配置
    'pathfinding': {
        'max_iterations': 1000,  # A*最大迭代次数
        'heuristic': 'manhattan',  # 启发式函数类型
    },
    
    # 冲突检测
    'collision_detection': {
        'enabled': True,
        'history_window': 100,  # 历史记录窗口（秒）
    },
    
    # 紧迫性计算
    'urgency': {
        'priority_multiplier': 10,  # 优先级权重倍数
        'age_multiplier': 0.1,      # 年龄权重倍数
    },
}

# ==================== 模拟配置 ====================
SIMULATION_CONFIG = {
    'default_step_size': 1.0,  # 默认时间步长（秒）
    'max_simulation_time': 3600.0,  # 最大模拟时间（秒）
    'update_frequency': 0.1,  # 更新频率（秒）
}

# ==================== 前端配置 ====================
FRONTEND_CONFIG = {
    'canvas_grid_color': '#e0e0e0',
    'canvas_line_width': 0.5,
    'robot_radius': 8,  # 机器人绘制半径
    'animation_fps': 30,  # 动画帧率
}

# ==================== API配置 ====================
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True,
    'cors_enabled': True,
}

# ==================== 日志配置 ====================
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'warehouse_system.log',
}

# ==================== 性能指标配置 ====================
METRICS_CONFIG = {
    'track_metrics': True,
    'metrics_update_interval': 1.0,  # 指标更新间隔（秒）
    'export_metrics': True,  # 导出指标到文件
    'metrics_file': 'metrics.json',
}
