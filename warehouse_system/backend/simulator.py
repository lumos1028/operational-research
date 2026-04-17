"""
系统模拟器 - 集成所有模块 (使用高级调度算法)
"""
import time
from environment import Environment
from robot import RobotFleet, RobotState
from order import OrderGenerator, OrderStatus
try:
    # 优先使用高级调度器（包含Hungarian和遗传算法）
    from scheduler_advanced import PathPlanner, AdvancedScheduler as Scheduler
except ImportError:
    # 备用：使用基础调度器
    from scheduler import PathPlanner, Scheduler

class WarehouseSimulator:
    """仓库系统模拟器"""
    
    def __init__(self, 
                 num_robots: int = 5,
                 warehouse_width: int = 50,
                 warehouse_height: int = 50):
        """初始化模拟器"""
        # 初始化环境
        self.environment = Environment(warehouse_width, warehouse_height)
        self.environment.create_default_warehouse()
        
        # 初始化机器人车队
        self.robot_fleet = RobotFleet(num_robots=num_robots, 
                                      start_position=(2, 2))
        
        # 初始化订单生成器
        self.order_generator = OrderGenerator(
            warehouse_width=warehouse_width,
            warehouse_height=warehouse_height,
            base_interval=1.0  # 每1秒生成一个订单
        )
        
        # 初始化路径规划和调度系统
        self.path_planner = PathPlanner(self.environment)
        self.scheduler = Scheduler(self.environment, self.robot_fleet, 
                                  self.path_planner)
        
        # 模拟状态
        self.current_time = 0.0
        self.simulation_running = False
        self.step_count = 0
        self.events_log = []
    
    def step(self, delta_time: float = 1.0):
        """模拟一步"""
        self.current_time += delta_time
        self.step_count += 1
        
        # 生成新订单
        new_orders = self.order_generator.update(self.current_time)
        for order in new_orders:
            self.events_log.append({
                'type': 'order_created',
                'order_id': order.id,
                'time': self.current_time,
                'priority': order.priority.name,
            })
        
        # 获取待分配订单
        pending_orders = self.order_generator.get_pending_orders()
        
        # 分配订单（延迟分配，让前端能看到待分配订单）
        # 每2步才分配一次，避免订单立即消失
        if self.step_count % 2 == 0 and pending_orders:
            assignments = self.scheduler.assign_orders(pending_orders, self.current_time)
            for assignment in assignments:
                self.events_log.append({
                    'type': 'order_assigned',
                    'order_id': assignment['order_id'],
                    'robot_id': assignment['robot_id'],
                    'time': self.current_time,
                })
        
        # 更新机器人状态（简化版本）
        for robot in self.robot_fleet.get_all_robots():
            # 如果有任务，模拟执行
            if robot.task_queue and not robot.current_task:
                robot.current_task = robot.task_queue.pop(0)
                robot.state = RobotState.MOVING
            
            # 模拟任务完成
            if robot.current_task:
                # 简化：假设每步完成一点任务
                progress = delta_time / robot.current_task.get('estimated_time', 15)
                
                # 获取路径并沿路径移动
                path = robot.current_task.get('path', [])
                if path and robot.path_index < len(path):
                    # 按路径移动
                    target_x, target_y = path[robot.path_index]
                    robot.x = target_x
                    robot.y = target_y
                    robot.path_index += 1
                
                # 累加距离
                distance = robot.current_task.get('distance', 0)
                robot.total_distance += distance * progress
                robot.battery -= distance * progress * 0.1  # 消耗电池
                
                # 任务完成（路径走完或超时）
                if robot.path_index >= len(path) or progress >= 1.0:
                    robot.tasks_completed += 1
                    robot.current_load = 0
                    robot.current_task = None
                    robot.path_index = 0
                    robot.state = RobotState.IDLE
                    self.events_log.append({
                        'type': 'task_completed',
                        'robot_id': robot.id,
                        'time': self.current_time,
                    })
            else:
                # 空闲状态
                if robot.state != RobotState.IDLE:
                    robot.state = RobotState.IDLE
            
            # 检查是否需要充电
            if robot.needs_charging():
                robot.state = RobotState.CHARGING
                robot.charge(0.5 * delta_time)  # 每步充电0.5
    
    def run_simulation(self, duration: float = 60.0, step_size: float = 1.0):
        """运行模拟"""
        self.simulation_running = True
        steps = int(duration / step_size)
        
        for _ in range(steps):
            if not self.simulation_running:
                break
            self.step(step_size)
    
    def get_state(self) -> dict:
        """获取当前系统状态"""
        return {
            'current_time': self.current_time,
            'step_count': self.step_count,
            'grid': self.environment.get_grid_state(),
            'robots': self.robot_fleet.get_fleet_status(),
            'pending_orders': len(self.order_generator.get_pending_orders()),
            'all_orders': [o.to_dict() for o in self.order_generator.get_all_orders()],
            'metrics': self.scheduler.get_system_metrics(),
            'events_log': self.events_log[-20:],  # 最近20条事件
        }
    
    def pause(self):
        """暂停模拟"""
        self.simulation_running = False
    
    def resume(self):
        """恢复模拟"""
        self.simulation_running = True

# 全局模拟器实例
_simulator = None

def get_simulator(num_robots: int = 5) -> WarehouseSimulator:
    """获取或创建模拟器"""
    global _simulator
    if _simulator is None:
        _simulator = WarehouseSimulator(num_robots=num_robots)
    return _simulator

def reset_simulator():
    """重置模拟器"""
    global _simulator
    _simulator = None
