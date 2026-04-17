"""
模块3：订单系统 - 企业真实场景版本
包含订单类型、截止时间、客户等级等真实属性
"""
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from enum import Enum
import random
import time

class OrderType(Enum):
    """订单类型"""
    SKU_PICKING = "sku_picking"          # SKU拣选
    CASE_SHIPMENT = "case_shipment"      # 整箱出库
    RETURN_INTAKE = "return_intake"      # 退货入库
    URGENT_REPLENISH = "urgent_replenish"  # 紧急补货

class OrderPriority(Enum):
    """订单优先级"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class CustomerType(Enum):
    """客户等级"""
    REGULAR = 1
    STANDARD = 2
    VIP = 3

class OrderStatus(Enum):
    PENDING = "pending"  # 待分配
    ASSIGNED = "assigned"  # 已分配
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消
    OVERDUE = "overdue"  # 逾期

@dataclass
class Order:
    """企业级订单类"""
    id: int
    order_type: OrderType                  # 订单类型
    customer_id: str                       # 客户ID
    customer_type: CustomerType            # 客户等级
    
    # 取货点相关
    pickup_location: Tuple[int, int]      # 取货点
    pickup_region: str                     # 取货区域名称
    
    # 送货点相关
    delivery_location: Tuple[int, int]    # 送货点（固定）
    delivery_station: str                  # 送货站点名称
    
    # 货物相关
    priority: OrderPriority = OrderPriority.MEDIUM
    weight_kg: float = 5.0                # 重量（单位：kg）
    volume_m3: float = 0.1               # 体积（单位：m³）
    quantity: int = 1
    
    # 时间相关
    created_time: float = field(default_factory=time.time)
    deadline: float = field(default_factory=lambda: time.time() + 3600)  # 1小时内完成
    operation_time: float = 3.0           # 机械臂操作时间（秒）
    
    # 状态相关
    status: OrderStatus = OrderStatus.PENDING
    assigned_robot_id: int = None
    start_time: float = None
    completion_time: float = None
    
    def get_urgency_score(self, current_time: float) -> float:
        """
        企业级紧迫性评分
        考虑：优先级、截止时间、客户等级
        """
        # 优先级基础分
        priority_base = self.priority.value * 15
        
        # 截止时间紧急度（越接近越高）
        time_to_deadline = self.deadline - current_time
        if time_to_deadline < 0:
            deadline_score = 100  # 已逾期
        else:
            deadline_score = max(0, (3600 - time_to_deadline) * 0.5)  # 0-1800分
        
        # 客户等级加成
        customer_bonus = (self.customer_type.value - 1) * 10
        
        # 订单年龄加成（等待越久优先级越高）
        age = current_time - self.created_time
        age_score = age * 0.1
        
        total_score = priority_base + deadline_score + customer_bonus + age_score
        return total_score
    
    def to_dict(self) -> Dict:
        """转换为字典（前端展示）"""
        time_to_deadline = max(0, self.deadline - time.time())
        return {
            'id': self.id,
            'order_type': self.order_type.name,
            'customer_id': self.customer_id,
            'customer_type': self.customer_type.name,
            'pickup_location': self.pickup_location,
            'pickup_region': self.pickup_region,
            'delivery_location': self.delivery_location,
            'delivery_station': self.delivery_station,
            'priority': self.priority.name,
            'weight_kg': self.weight_kg,
            'volume_m3': self.volume_m3,
            'quantity': self.quantity,
            'created_time': self.created_time,
            'deadline': self.deadline,
            'time_to_deadline': time_to_deadline,
            'operation_time': self.operation_time,
            'status': self.status.value,
            'assigned_robot_id': self.assigned_robot_id,
            'urgency_score': self.get_urgency_score(time.time()),
        }

class OrderGenerator:
    """企业级订单生成器"""
    
    # 预定义的仓库区域
    WAREHOUSE_REGIONS = {
        'SHELF_A': [(5, 10), (15, 10), (25, 10), (35, 10)],      # A区货架
        'SHELF_B': [(5, 25), (15, 25), (25, 25), (35, 25)],      # B区货架
        'SHELF_C': [(5, 40), (15, 40), (25, 40), (35, 40)],      # C区货架
        'INTAKE': [(10, 5), (30, 5)],                             # 入库暂存区
    }
    
    # 固定的送货站点
    DELIVERY_STATIONS = {
        'PACKING_A': (45, 15),   # 拣货打包区A
        'PACKING_B': (45, 35),   # 拣货打包区B
        'SHIP_DOCK': (48, 25),   # 出库装车区
    }
    
    # 客户ID列表（模拟）
    CUSTOMER_IDS = [f'CUST_{i:04d}' for i in range(100, 200)]
    
    def __init__(self, 
                 warehouse_width: int = 50,
                 warehouse_height: int = 50,
                 base_interval: float = 2.0):
        """初始化企业级订单生成器"""
        self.warehouse_width = warehouse_width
        self.warehouse_height = warehouse_height
        self.base_interval = base_interval
        self.next_order_id = 1
        self.orders: Dict[int, Order] = {}
        self.last_generation_time = 0
    
    def generate_order(self, current_time: float = None) -> Order:
        """生成符合企业场景的订单"""
        if current_time is None:
            current_time = time.time()
        
        order_id = self.next_order_id
        self.next_order_id += 1
        
        # 订单类型分布
        rand_type = random.random()
        if rand_type < 0.65:
            order_type = OrderType.SKU_PICKING
        elif rand_type < 0.85:
            order_type = OrderType.CASE_SHIPMENT
        elif rand_type < 0.95:
            order_type = OrderType.RETURN_INTAKE
        else:
            order_type = OrderType.URGENT_REPLENISH
        
        # 客户等级分布（VIP:15%, 标准:35%, 普通:50%）
        rand_cust = random.random()
        if rand_cust < 0.15:
            customer_type = CustomerType.VIP
            deadline_offset = 1800  # VIP：30分钟
        elif rand_cust < 0.50:
            customer_type = CustomerType.STANDARD
            deadline_offset = 3600  # 标准：1小时
        else:
            customer_type = CustomerType.REGULAR
            deadline_offset = 7200  # 普通：2小时
        
        # 取货点选择（80%来自货架，20%来自暂存区）
        if random.random() < 0.8:
            region_name = random.choice(['SHELF_A', 'SHELF_B', 'SHELF_C'])
            pickup_location = random.choice(self.WAREHOUSE_REGIONS[region_name])
        else:
            region_name = 'INTAKE'
            pickup_location = random.choice(self.WAREHOUSE_REGIONS['INTAKE'])
        
        # 送货点固定选择
        station_name = random.choice(list(self.DELIVERY_STATIONS.keys()))
        delivery_location = self.DELIVERY_STATIONS[station_name]
        
        # 货物属性
        weight_kg = random.uniform(0.5, 20.0)
        volume_m3 = weight_kg * 0.005 + random.uniform(0, 0.05)
        quantity = random.randint(1, 10)
        
        # 优先级（高优先级20%，中30%，低50%）
        rand_priority = random.random()
        if rand_priority < 0.2:
            priority = OrderPriority.HIGH
        elif rand_priority < 0.5:
            priority = OrderPriority.MEDIUM
        else:
            priority = OrderPriority.LOW
        
        order = Order(
            id=order_id,
            order_type=order_type,
            customer_id=random.choice(self.CUSTOMER_IDS),
            customer_type=customer_type,
            pickup_location=pickup_location,
            pickup_region=region_name,
            delivery_location=delivery_location,
            delivery_station=station_name,
            priority=priority,
            weight_kg=weight_kg,
            volume_m3=volume_m3,
            quantity=quantity,
            created_time=current_time,
            deadline=current_time + deadline_offset,
            operation_time=3.0 + random.uniform(0, 2),  # 3-5秒
        )
        
        self.orders[order_id] = order
        return order
    
    def generate_orders_batch(self, current_time: float = None, num_orders: int = 3) -> List[Order]:
        """批量生成订单"""
        if current_time is None:
            current_time = time.time()
        
        # 双11场景：峰值时订单生成数量增加
        is_peak = (current_time % 100) < 30  # 模拟峰值时段
        num_orders = num_orders * 2 if is_peak else num_orders
        
        return [self.generate_order(current_time) for _ in range(num_orders)]
    
    def should_generate(self, current_time: float = None) -> bool:
        """检查是否应该生成新订单"""
        if current_time is None:
            current_time = 0
        
        time_elapsed = current_time - self.last_generation_time
        # 变量间隔：在base_interval的50%-150%之间
        interval = self.base_interval * random.uniform(0.5, 1.5)
        
        return time_elapsed >= interval
    
    def update(self, current_time: float = None) -> List[Order]:
        """更新订单生成状态，返回新生成的订单"""
        if current_time is None:
            current_time = time.time()
        
        new_orders = []
        if self.should_generate(current_time):
            new_orders = self.generate_orders_batch(current_time)
            self.last_generation_time = current_time if current_time is not None else 0
        
        return new_orders
    
    def get_pending_orders(self) -> List[Order]:
        """获取所有待分配的订单"""
        return [o for o in self.orders.values() if o.status == OrderStatus.PENDING]
    
    def get_all_orders(self) -> List[Order]:
        """获取所有订单"""
        return list(self.orders.values())
    
    def get_orders_by_region(self, region: str) -> List[Order]:
        """按地区获取订单"""
        return [o for o in self.orders.values() if o.pickup_region == region]
    
    def get_overdue_orders(self, current_time: float) -> List[Order]:
        """获取已逾期的订单"""
        return [o for o in self.orders.values() 
                if o.status in [OrderStatus.PENDING, OrderStatus.ASSIGNED, OrderStatus.IN_PROGRESS]
                and o.deadline < current_time]
