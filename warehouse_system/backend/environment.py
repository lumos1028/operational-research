"""
模块1：环境建模
包含网格地图、障碍物、通道、充电区
"""
import numpy as np
from dataclasses import dataclass
from typing import List, Set, Tuple

@dataclass
class Environment:
    """
    仓库环境建模
    """
    width: int = 50  # 地图宽度
    height: int = 50  # 地图高度
    
    def __init__(self, width=50, height=50):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.int32)
        # 0: 通道, 1: 障碍物, 2: 充电区, 3: 目标点
        self.obstacles = set()
        self.charging_areas = set()
        self.target_points = set()
        
    def add_obstacles(self, obstacles: List[Tuple[int, int]]):
        """添加障碍物（货架）"""
        for x, y in obstacles:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = 1
                self.obstacles.add((x, y))
    
    def add_charging_area(self, pos: Tuple[int, int]):
        """添加充电区"""
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = 2
            self.charging_areas.add((x, y))
    
    def add_target_point(self, pos: Tuple[int, int]):
        """添加目标点（拣货点）"""
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = 3
            self.target_points.add((x, y))
    
    def is_walkable(self, x: int, y: int) -> bool:
        """检查位置是否可通行"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        # 通道、充电区、目标点都是可通行的
        return self.grid[y, x] != 1
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """获取相邻可通行的位置（4向移动）"""
        neighbors = []
        # 上下左右四个方向
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if self.is_walkable(nx, ny):
                neighbors.append((nx, ny))
        return neighbors
    
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """曼哈顿距离"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def euclidean_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """欧氏距离"""
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
    
    def get_grid_state(self):
        """获取网格状态（为前端返回）"""
        return self.grid.tolist()
    
    def create_default_warehouse(self):
        """创建默认仓库配置"""
        # 添加障碍物（货架）- 形成通道
        for i in range(5, 45, 10):
            for j in range(5, 45):
                self.add_obstacles([(j, i), (j, i+2)])
        
        # 添加充电区（左上角）
        for x in range(2, 5):
            for y in range(2, 5):
                self.add_charging_area((x, y))
        
        # 添加目标点（右下角）
        for x in range(45, 48):
            for y in range(45, 48):
                self.add_target_point((x, y))
