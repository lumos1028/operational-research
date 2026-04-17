"""
模块4：调度系统 & 路径规划
- A*路径规划
- 任务分配算法
- 冲突避免
"""
from typing import List, Dict, Tuple, Set, Optional
import heapq
from math import sqrt
from dataclasses import dataclass
import time
from order import OrderStatus

@dataclass
class PathNode:
    """路径节点用于A*算法"""
    x: int
    y: int
    g: float  # 从起点到当前节点的代价
    h: float  # 从当前节点到目标的启发式估计
    parent: Optional['PathNode'] = None
    
    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

class PathPlanner:
    """路径规划器 - 使用A*算法"""
    
    def __init__(self, environment):
        self.environment = environment
        self.collision_map = {}  # 用于冲突检测的时间-空间映射
    
    def manhattan_heuristic(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """曼哈顿距离启发式函数"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def euclidean_heuristic(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """欧氏距离启发式函数"""
        return sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def plan_path(self, 
                  start: Tuple[int, int], 
                  goal: Tuple[int, int],
                  max_iterations: int = 1000) -> List[Tuple[int, int]]:
        """
        A*路径规划
        
        Args:
            start: 起始位置
            goal: 目标位置
            max_iterations: 最大迭代次数
        
        Returns:
            路径列表
        """
        if not self.environment.is_walkable(goal[0], goal[1]):
            # 如果目标不可通行，寻找最近的可通行位置
            goal = self._find_nearest_walkable(goal)
        
        start_node = PathNode(start[0], start[1], 0, 
                             self.manhattan_heuristic(start, goal))
        goal_pos = goal
        
        open_list = [start_node]
        closed_set = set()
        iterations = 0
        
        while open_list and iterations < max_iterations:
            iterations += 1
            
            # 获取f值最小的节点
            current = heapq.heappop(open_list)
            
            if (current.x, current.y) == goal_pos:
                # 重建路径
                path = []
                node = current
                while node:
                    path.append((node.x, node.y))
                    node = node.parent
                return path[::-1]  # 反转路径
            
            closed_set.add((current.x, current.y))
            
            # 探索邻居
            neighbors = self.environment.get_neighbors(current.x, current.y)
            
            for nx, ny in neighbors:
                neighbor_pos = (nx, ny)
                
                if neighbor_pos in closed_set:
                    continue
                
                g = current.g + 1  # 每步距离为1
                h = self.manhattan_heuristic(neighbor_pos, goal_pos)
                
                neighbor_node = PathNode(nx, ny, g, h, current)
                
                # 检查是否已在open_list中
                existing = None
                for node in open_list:
                    if node == neighbor_node:
                        existing = node
                        break
                
                if existing is None:
                    heapq.heappush(open_list, neighbor_node)
                elif neighbor_node.g < existing.g:
                    existing.g = neighbor_node.g
                    existing.parent = current
        
        # 如果没有找到路径，返回空列表
        return []
    
    def _find_nearest_walkable(self, pos: Tuple[int, int], radius: int = 5) -> Tuple[int, int]:
        """查找最近的可通行位置"""
        x, y = pos
        for r in range(1, radius + 1):
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    nx, ny = x + dx, y + dy
                    if self.environment.is_walkable(nx, ny):
                        return (nx, ny)
        return pos
    
    def register_path(self, robot_id: int, path: List[Tuple[int, int]], start_time: float):
        """注册路径以进行冲突检测"""
        for idx, (x, y) in enumerate(path):
            time_key = (start_time + idx, x, y)
            if time_key not in self.collision_map:
                self.collision_map[time_key] = []
            self.collision_map[time_key].append(robot_id)
    
    def check_collision(self, path: List[Tuple[int, int]], start_time: float) -> bool:
        """检查路径是否会产生碰撞"""
        for idx, (x, y) in enumerate(path):
            time_key = (start_time + idx, x, y)
            if time_key in self.collision_map:
                # 检查是否有其他机器人在该时间空间位置
                return len(self.collision_map[time_key]) > 0
        return False
    
    def cleanup_old_collisions(self, current_time: float, history_window: float = 100):
        """清理过期的碰撞记录"""
        keys_to_remove = []
        for time_pos_key in self.collision_map.keys():
            if time_pos_key[0] < current_time - history_window:
                keys_to_remove.append(time_pos_key)
        
        for key in keys_to_remove:
            del self.collision_map[key]

class Scheduler:
    """调度系统"""
    
    def __init__(self, environment, robot_fleet, path_planner):
        self.environment = environment
        self.robot_fleet = robot_fleet
        self.path_planner = path_planner
        self.task_history: List[Dict] = []
        self.assignment_history: List[Dict] = []
    
    def calculate_assignment_cost(self, 
                                 robot, 
                                 order,
                                 current_time: float) -> Dict:
        """
        计算任务分配成本
        
        返回字典包含：
        - distance: 总距离
        - time: 估计完成时间
        - battery_cost: 电池消耗
        - urgency: 订单紧迫性评分
        """
        # 计算机器人到取货点的距离
        pickup_distance = self.environment.manhattan_distance(
            (robot.x, robot.y), order.pickup_location)
        
        # 计算取货点到送货点的距离
        delivery_distance = self.environment.manhattan_distance(
            order.pickup_location, order.delivery_location)
        
        total_distance = pickup_distance + delivery_distance
        
        # 估计完成时间 = 距离 / 速度 + 处理时间(10秒)
        estimated_time = total_distance / robot.speed + 10
        
        # 考虑机器人当前任务队列的时间
        queue_time = len(robot.task_queue) * 15  # 每个任务15秒
        
        # 电池消耗估计
        battery_cost = total_distance * 0.1
        
        # 获取订单紧迫性
        urgency = order.get_urgency_score(current_time)
        
        # 综合成本：距离 + 队列时间 - 紧迫性（紧迫性高的订单优先）
        # 负权重给紧迫性，因为我们想优先分配紧迫的订单
        composite_cost = (total_distance * 0.5 + 
                         queue_time * 0.3 - 
                         urgency * 0.2 +
                         battery_cost * 0.2)
        
        return {
            'robot_id': robot.id,
            'distance': total_distance,
            'estimated_time': estimated_time,
            'queue_time': queue_time,
            'battery_cost': battery_cost,
            'urgency': urgency,
            'composite_cost': composite_cost,
            'workload_level': robot.get_workload(),
        }
    
    def select_best_robot(self, 
                          order,
                          current_time: float) -> Optional[Dict]:
        """
        选择最佳机器人
        
        优化目标：
        1. 最小化总完成时间（Makespan）
        2. 最小化总行驶距离
        3. 机器人负载均衡
        4. 避免冲突
        """
        available_robots = self.robot_fleet.get_all_robots()
        
        if not available_robots:
            return None
        
        # 计算所有可用机器人的成本
        robot_costs = []
        for robot in available_robots:
            # 过滤掉电池过低的机器人
            if robot.battery < 15:
                continue
            
            cost_info = self.calculate_assignment_cost(robot, order, current_time)
            robot_costs.append(cost_info)
        
        if not robot_costs:
            # 如果没有可用机器人，选择电池最好的
            return min([self.calculate_assignment_cost(r, order, current_time) 
                       for r in available_robots],
                      key=lambda x: x['composite_cost'])
        
        # 使用加权综合指标选择最佳机器人
        # 权重：距离(40%) + 队列时间(35%) + 工作负载(25%)
        best_option = min(robot_costs,
                         key=lambda x: (x['distance'] * 0.4 + 
                                       x['queue_time'] * 0.35 +
                                       x['workload_level'] * 0.25))
        
        return best_option
    
    def assign_orders(self, orders: List, current_time: float) -> List[Dict]:
        """
        分配订单到机器人
        
        Args:
            orders: 待分配订单列表
            current_time: 当前时间
        
        Returns:
            分配结果列表
        """
        assignments = []
        
        # 按紧迫性排序订单
        sorted_orders = sorted(orders, 
                              key=lambda o: o.get_urgency_score(current_time),
                              reverse=True)
        
        for order in sorted_orders:
            best_robot_info = self.select_best_robot(order, current_time)
            
            if best_robot_info:
                robot_id = best_robot_info['robot_id']
                robot = self.robot_fleet.get_robot(robot_id)
                
                # 规划路径
                path = self.path_planner.plan_path(
                    (robot.x, robot.y),
                    order.pickup_location
                )
                
                # 创建任务
                task = {
                    'order_id': order.id,
                    'pickup_location': order.pickup_location,
                    'delivery_location': order.delivery_location,
                    'path': path,
                    'created_time': current_time,
                    'estimated_time': best_robot_info['estimated_time'],
                    'priority': order.priority.value,
                }
                
                # 分配任务给机器人
                robot.assign_task(task, current_time)
                order.status = OrderStatus.ASSIGNED
                order.assigned_robot_id = robot_id
                
                # 记录分配信息
                assignments.append({
                    'order_id': order.id,
                    'robot_id': robot_id,
                    'cost': best_robot_info['composite_cost'],
                    'distance': best_robot_info['distance'],
                    'estimated_time': best_robot_info['estimated_time'],
                    'timestamp': current_time,
                })
                
                self.assignment_history.append(assignments[-1])
        
        return assignments
    
    def get_system_metrics(self) -> Dict:
        """获取系统性能指标"""
        all_robots = self.robot_fleet.get_all_robots()
        total_distance = sum(r.total_distance for r in all_robots)
        total_tasks = sum(r.tasks_completed for r in all_robots)
        avg_battery = sum(r.battery for r in all_robots) / len(all_robots) if all_robots else 0
        
        return {
            'total_distance': total_distance,
            'total_tasks_completed': total_tasks,
            'average_battery': avg_battery,
            'total_assignments': len(self.assignment_history),
        }
