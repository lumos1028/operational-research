"""
Phase 3: 高级调度算法
- Hungarian算法（匈牙利算法）：最优1-to-N任务分配
- 遗传算法：全局最优解搜索
- 批量任务分配
- 负载均衡优化
"""
import heapq
from typing import List, Dict, Tuple, Set, Optional
from math import sqrt, exp
import random
import numpy as np
from scipy.optimize import linear_sum_assignment
from dataclasses import dataclass
import time
from order import OrderStatus
from abc import ABC, abstractmethod

@dataclass
class PathNode:
    """路径节点用于A*算法"""
    x: int
    y: int
    g: float
    h: float
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
        self.collision_map = {}
    
    def manhattan_heuristic(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def plan_path(self, 
                  start: Tuple[int, int], 
                  goal: Tuple[int, int],
                  max_iterations: int = 1000) -> List[Tuple[int, int]]:
        """A*路径规划"""
        if not self.environment.is_walkable(goal[0], goal[1]):
            goal = self._find_nearest_walkable(goal)
        
        start_node = PathNode(start[0], start[1], 0, 
                             self.manhattan_heuristic(start, goal))
        goal_pos = goal
        
        open_list = [start_node]
        closed_set = set()
        iterations = 0
        
        while open_list and iterations < max_iterations:
            iterations += 1
            current = heapq.heappop(open_list)
            
            if (current.x, current.y) == goal_pos:
                path = []
                node = current
                while node:
                    path.append((node.x, node.y))
                    node = node.parent
                return path[::-1]
            
            closed_set.add((current.x, current.y))
            neighbors = self.environment.get_neighbors(current.x, current.y)
            
            for nx, ny in neighbors:
                neighbor_pos = (nx, ny)
                
                if neighbor_pos in closed_set:
                    continue
                
                g = current.g + 1
                h = self.manhattan_heuristic(neighbor_pos, goal_pos)
                neighbor_node = PathNode(nx, ny, g, h, current)
                
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

class HungarianScheduler:
    """Hungarian算法调度器 - 最优任务分配"""
    
    def __init__(self, environment, robot_fleet, path_planner):
        self.environment = environment
        self.robot_fleet = robot_fleet
        self.path_planner = path_planner
    
    def calculate_cost_matrix(self, 
                             robots: List,
                             orders: List,
                             current_time: float) -> np.ndarray:
        """
        计算成本矩阵
        rows: 机器人, cols: 订单
        """
        n_robots = len(robots)
        n_orders = len(orders)
        
        # 创建成本矩阵
        cost_matrix = np.zeros((n_robots, n_orders))
        
        for i, robot in enumerate(robots):
            for j, order in enumerate(orders):
                # 跳过电池不足的机器人
                if robot.battery < 15:
                    cost_matrix[i, j] = 1e10  # 大成本值
                    continue
                
                # 计算距离成本
                distance = self.environment.manhattan_distance(
                    (robot.x, robot.y), order.pickup_location)
                distance += self.environment.manhattan_distance(
                    order.pickup_location, order.delivery_location)
                
                # 计算时间成本（队列时间）
                queue_cost = len(robot.task_queue) * 10
                
                # 计算电池成本
                battery_cost = (distance * 0.1) / max(robot.battery, 1)
                
                # 计算紧迫性奖励（负成本 = 优先分配）
                urgency = order.get_urgency_score(current_time)
                urgency_reward = -urgency * 0.001  # 转换为成本空间
                
                # 综合成本
                cost_matrix[i, j] = (
                    distance * 0.5 +
                    queue_cost * 0.3 +
                    battery_cost * 0.2 +
                    urgency_reward
                )
        
        return cost_matrix
    
    def assign_orders_hungarian(self, 
                               orders: List,
                               current_time: float) -> List[Dict]:
        """
        使用Hungarian算法进行最优任务分配
        """
        available_robots = [r for r in self.robot_fleet.get_all_robots() 
                           if r.battery > 15 and r.state.value != 'CHARGING']
        
        if not available_robots or not orders:
            return []
        
        # 按紧迫性排序订单（优先处理紧迫订单）
        sorted_orders = sorted(orders,
                              key=lambda o: o.get_urgency_score(current_time),
                              reverse=True)
        
        # 计算成本矩阵
        cost_matrix = self.calculate_cost_matrix(available_robots, sorted_orders, current_time)
        
        # 调用Hungarian算法
        robot_indices, order_indices = linear_sum_assignment(cost_matrix)
        
        assignments = []
        
        for r_idx, o_idx in zip(robot_indices, order_indices):
            # 检查成本是否合理（不超过阈值）
            if cost_matrix[r_idx, o_idx] > 1e9:
                continue
            
            robot = available_robots[r_idx]
            order = sorted_orders[o_idx]
            
            # 规划路径
            path = self.path_planner.plan_path(
                (robot.x, robot.y),
                order.pickup_location
            )
            
            if not path:
                continue
            
            # 创建任务
            task = {
                'order_id': order.id,
                'pickup_location': order.pickup_location,
                'delivery_location': order.delivery_location,
                'path': path,
                'created_time': current_time,
                'priority': order.priority.value,
            }
            
            # 分配任务
            robot.assign_task(task, current_time)
            order.status = OrderStatus.ASSIGNED
            order.assigned_robot_id = robot.id
            
            assignments.append({
                'order_id': order.id,
                'robot_id': robot.id,
                'algorithm': 'Hungarian',
                'cost': float(cost_matrix[r_idx, o_idx]),
                'timestamp': current_time,
            })
        
        return assignments

class GeneticScheduler:
    """遗传算法调度器 - 全局最优解搜索"""
    
    def __init__(self, environment, robot_fleet, path_planner):
        self.environment = environment
        self.robot_fleet = robot_fleet
        self.path_planner = path_planner
        
        # 遗传算法参数
        self.population_size = 20
        self.generations = 50
        self.mutation_rate = 0.1
        self.crossover_rate = 0.8
    
    def generate_solution(self, 
                         robots: List, 
                         orders: List) -> np.ndarray:
        """
        生成一个随机解（assignment vector）
        solution[i] = robot_id for order i（-1表示未分配）
        """
        solution = np.full(len(orders), -1, dtype=int)
        
        for i, order in enumerate(orders):
            if random.random() < 0.8:  # 80%概率分配
                available_robot_ids = [r.id for r in robots if r.battery > 15]
                if available_robot_ids:
                    solution[i] = random.choice(available_robot_ids)
        
        return solution
    
    def evaluate_solution(self,
                         solution: np.ndarray,
                         robots: List,
                         orders: List,
                         current_time: float) -> float:
        """
        评估解的质量（fitness score）
        目标：最小化总完成时间、总距离、最大负载
        """
        if solution is None or len(solution) == 0:
            return 1e10
        
        total_cost = 0
        robot_loads = {}  # 每个机器人的总距离
        robot_tasks = {}  # 每个机器人的任务数
        
        for robot in robots:
            robot_loads[robot.id] = 0
            robot_tasks[robot.id] = 0
        
        unassigned_orders = 0
        
        for i, order_idx in enumerate(solution):
            if order_idx == -1 or order_idx >= len(orders):
                unassigned_orders += 1
                continue
            
            order = orders[i]
            robot_id = int(order_idx)
            
            # 找到机器人
            robot = self.robot_fleet.get_robot(robot_id)
            if not robot:
                unassigned_orders += 1
                continue
            
            # 计算距离
            distance = self.environment.manhattan_distance(
                (robot.x, robot.y), order.pickup_location)
            distance += self.environment.manhattan_distance(
                order.pickup_location, order.delivery_location)
            
            robot_loads[robot_id] += distance
            robot_tasks[robot_id] += 1
        
        # 计算目标函数
        # 1. 最小化最大负载（负载均衡）
        max_load = max(robot_loads.values()) if robot_loads else 0
        load_balance_cost = max_load
        
        # 2. 最小化未分配订单
        unassigned_cost = unassigned_orders * 100
        
        # 3. 最小化负载不均衡度（方差）
        if robot_loads:
            loads = list(robot_loads.values())
            mean_load = np.mean(loads)
            variance = np.var(loads)
            variance_cost = variance * 0.5
        else:
            variance_cost = 0
        
        total_cost = load_balance_cost + unassigned_cost + variance_cost
        
        return total_cost
    
    def mutate(self, solution: np.ndarray, robots: List, orders: List) -> np.ndarray:
        """
        变异操作：随机修改分配
        """
        mutated = solution.copy()
        
        if len(orders) == 0:
            return mutated
        
        for _ in range(max(1, len(orders) // 5)):
            if random.random() < self.mutation_rate:
                idx = random.randint(0, len(mutated) - 1)
                
                if random.random() < 0.5:
                    # 随机分配给一个机器人
                    available_robot_ids = [r.id for r in robots if r.battery > 15]
                    if available_robot_ids:
                        mutated[idx] = random.choice(available_robot_ids)
                else:
                    # 设置为未分配
                    mutated[idx] = -1
        
        return mutated
    
    def crossover(self, parent1: np.ndarray, parent2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        交叉操作：结合两个父解
        """
        if len(parent1) == 0:
            return parent1.copy(), parent2.copy()
        
        crossover_point = random.randint(1, len(parent1) - 1)
        
        child1 = np.concatenate([parent1[:crossover_point], parent2[crossover_point:]])
        child2 = np.concatenate([parent2[:crossover_point], parent1[crossover_point:]])
        
        return child1, child2
    
    def solve(self,
             orders: List,
             current_time: float) -> List[Dict]:
        """
        使用遗传算法求解任务分配问题
        """
        available_robots = [r for r in self.robot_fleet.get_all_robots() 
                           if r.battery > 15]
        
        if not available_robots or not orders:
            return []
        
        # 按紧迫性排序订单
        sorted_orders = sorted(orders,
                              key=lambda o: o.get_urgency_score(current_time),
                              reverse=True)[:10]  # 限制规模以加快计算
        
        # 初始化种群
        population = [self.generate_solution(available_robots, sorted_orders) 
                     for _ in range(self.population_size)]
        
        # 进化过程
        for generation in range(self.generations):
            # 评估
            fitness_scores = [self.evaluate_solution(sol, available_robots, sorted_orders, current_time)
                            for sol in population]
            
            # 选择（竞赛选择）
            new_population = []
            for _ in range(self.population_size):
                # 随机选择2个候选者，选择更好的
                idx1, idx2 = random.sample(range(self.population_size), 2)
                if fitness_scores[idx1] < fitness_scores[idx2]:
                    new_population.append(population[idx1].copy())
                else:
                    new_population.append(population[idx2].copy())
            
            population = new_population
            
            # 交叉和变异
            for i in range(0, len(population) - 1, 2):
                if random.random() < self.crossover_rate:
                    population[i], population[i + 1] = self.crossover(
                        population[i], population[i + 1])
                
                population[i] = self.mutate(population[i], available_robots, sorted_orders)
                population[i + 1] = self.mutate(population[i + 1], available_robots, sorted_orders)
        
        # 找到最优解
        fitness_scores = [self.evaluate_solution(sol, available_robots, sorted_orders, current_time)
                         for sol in population]
        best_solution = population[np.argmin(fitness_scores)]
        
        # 转换为分配结果
        assignments = []
        
        for i, robot_id in enumerate(best_solution):
            if robot_id == -1 or robot_id >= len(available_robots):
                continue
            
            order = sorted_orders[i]
            robot = self.robot_fleet.get_robot(int(robot_id))
            
            if not robot:
                continue
            
            # 规划路径
            path = self.path_planner.plan_path(
                (robot.x, robot.y),
                order.pickup_location
            )
            
            if not path:
                continue
            
            # 创建任务
            task = {
                'order_id': order.id,
                'pickup_location': order.pickup_location,
                'delivery_location': order.delivery_location,
                'path': path,
                'created_time': current_time,
                'priority': order.priority.value,
            }
            
            # 分配任务
            robot.assign_task(task, current_time)
            order.status = OrderStatus.ASSIGNED
            order.assigned_robot_id = robot.id
            
            # 记录分配
            best_fitness = fitness_scores[np.argmin(fitness_scores)]
            assignments.append({
                'order_id': order.id,
                'robot_id': robot.id,
                'algorithm': 'Genetic',
                'fitness': float(best_fitness),
                'timestamp': current_time,
            })
        
        return assignments

class AdvancedScheduler:
    """
    高级调度器 - 整合Hungarian和遗传算法
    自动选择最适合的算法
    """
    
    def __init__(self, environment, robot_fleet, path_planner):
        self.environment = environment
        self.robot_fleet = robot_fleet
        self.path_planner = path_planner
        
        # 初始化两种算法
        self.hungarian_scheduler = HungarianScheduler(environment, robot_fleet, path_planner)
        self.genetic_scheduler = GeneticScheduler(environment, robot_fleet, path_planner)
        
        self.assignment_history = []
        self.algorithm_stats = {'Hungarian': 0, 'Genetic': 0}
    
    def should_use_genetic(self, n_robots: int, n_orders: int) -> bool:
        """
        决定是否使用遗传算法
        规则：订单数多且涉及多个机器人时使用遗传算法
        """
        # 如果订单和机器人都较多且时间充裕，使用遗传算法获得更优解
        return (n_orders > 8 and n_robots > 3)
    
    def assign_orders(self, 
                     orders: List,
                     current_time: float) -> List[Dict]:
        """
        分配订单 - 自动选择算法
        """
        available_robots = [r for r in self.robot_fleet.get_all_robots() 
                           if r.battery > 15]
        
        pending_orders = [o for o in orders if o.status.value == 'pending']
        
        if not pending_orders or not available_robots:
            return []
        
        # 决定使用哪个算法
        if self.should_use_genetic(len(available_robots), len(pending_orders)):
            # 使用遗传算法
            assignments = self.genetic_scheduler.solve(pending_orders, current_time)
            self.algorithm_stats['Genetic'] += len(assignments)
        else:
            # 使用Hungarian算法
            assignments = self.hungarian_scheduler.assign_orders_hungarian(
                pending_orders, current_time)
            self.algorithm_stats['Hungarian'] += len(assignments)
        
        # 记录历史
        self.assignment_history.extend(assignments)
        
        return assignments
    
    def get_system_metrics(self) -> Dict:
        """获取系统性能指标"""
        all_robots = self.robot_fleet.get_all_robots()
        total_distance = sum(r.total_distance for r in all_robots)
        total_tasks = sum(r.tasks_completed for r in all_robots)
        avg_battery = sum(r.battery for r in all_robots) / len(all_robots) if all_robots else 0
        
        # 计算负载均衡度
        if all_robots:
            loads = [r.total_distance for r in all_robots]
            load_variance = np.var(loads) if len(loads) > 1 else 0
            load_balance_score = 1.0 / (1.0 + load_variance)  # 正规化到0-1
        else:
            load_balance_score = 0
        
        return {
            'total_distance': total_distance,
            'total_tasks_completed': total_tasks,
            'average_battery': avg_battery,
            'total_assignments': len(self.assignment_history),
            'load_balance_score': load_balance_score,
            'algorithm_usage': self.algorithm_stats,
        }

# 为了向后兼容，别名Scheduler到AdvancedScheduler
Scheduler = AdvancedScheduler
