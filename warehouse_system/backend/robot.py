"""
模块2：机器人系统
每个机器人有：位置、状态、任务队列、可用时间
"""
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
from enum import Enum
import time

class RobotState(Enum):
    IDLE = "idle"  # 空闲
    BUSY = "busy"  # 忙碌
    CHARGING = "charging"  # 充电
    MOVING = "moving"  # 移动中

class Robot:
    """机器人类"""
    
    instance_count = 0
    
    def __init__(self, 
                 x: int, 
                 y: int,
                 max_capacity: int = 100,
                 max_battery: float = 100.0,
                 speed: float = 1.0):
        """
        初始化机器人
        
        Args:
            x, y: 初始位置
            max_capacity: 最大容量
            max_battery: 最大电池容量
            speed: 移动速度（距离/秒）
        """
        Robot.instance_count += 1
        self.id = Robot.instance_count
        self.x = x
        self.y = y
        self.state = RobotState.IDLE
        self.current_load = 0
        self.max_capacity = max_capacity
        self.battery = max_battery
        self.max_battery = max_battery
        self.speed = speed
        self.task_queue: List[Dict] = []  # 任务队列
        self.total_distance = 0.0
        self.tasks_completed = 0
        self.available_time = 0.0  # 可用时间戳
        self.current_task = None
        self.path: List[Tuple[int, int]] = []  # 当前路径
        self.path_index = 0
    
    def assign_task(self, task: Dict, available_time: float = 0.0):
        """分配任务"""
        self.task_queue.append(task)
        if self.state == RobotState.IDLE:
            self.state = RobotState.BUSY
        self.available_time = max(self.available_time, available_time)
    
    def complete_task(self):
        """完成任务"""
        if self.current_task:
            self.tasks_completed += 1
            self.current_task = None
    
    def update_position(self, x: int, y: int, distance: float):
        """更新位置和电池"""
        self.x = x
        self.y = y
        self.total_distance += distance
        # 消耗电池 (阿假设每个距离单位消耗0.1电量)
        self.battery -= distance * 0.1
    
    def charge(self, amount: float):
        """充电"""
        self.battery = min(self.battery + amount, self.max_battery)
    
    def needs_charging(self, threshold: float = 20.0) -> bool:
        """检查是否需要充电"""
        return self.battery < threshold
    
    def get_workload(self) -> float:
        """获取机器人工作量（任务数+当前负载）"""
        return len(self.task_queue) + self.current_load / self.max_capacity
    
    def get_status(self) -> Dict:
        """获取机器人状态信息"""
        state_value = self.state.value if isinstance(self.state, RobotState) else str(self.state)
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'state': state_value,
            'battery': self.battery,
            'load': self.current_load,
            'workload_level': self.get_workload(),
            'tasks_in_queue': len(self.task_queue),
            'total_distance': self.total_distance,
            'tasks_completed': self.tasks_completed,
            'available_time': self.available_time,
        }

class RobotFleet:
    """机器人集群管理"""
    
    def __init__(self, num_robots: int = 5, start_position: Tuple[int, int] = (2, 2)):
        """
        初始化机器人集群
        
        Args:
            num_robots: 机器人数量
            start_position: 起始位置
        """
        self.robots: Dict[int, Robot] = {}
        for i in range(num_robots):
            robot = Robot(start_position[0], start_position[1])
            self.robots[robot.id] = robot
    
    def get_robot(self, robot_id: int) -> Optional[Robot]:
        """获取机器人"""
        return self.robots.get(robot_id)
    
    def get_all_robots(self) -> List[Robot]:
        """获取所有机器人"""
        return list(self.robots.values())
    
    def get_idle_robots(self) -> List[Robot]:
        """获取空闲机器人"""
        return [r for r in self.robots.values() if r.state == RobotState.IDLE]
    
    def get_fleet_status(self) -> Dict:
        """获取集群状态"""
        robots_status = [robot.get_status() for robot in self.robots.values()]
        total_load = sum(r.current_load for r in self.robots.values())
        total_distance = sum(r.total_distance for r in self.robots.values())
        
        return {
            'total_robots': len(self.robots),
            'idle_robots': len(self.get_idle_robots()),
            'total_load': total_load,
            'total_distance': total_distance,
            'robots': robots_status,
        }
