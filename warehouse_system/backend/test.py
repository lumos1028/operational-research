"""
测试脚本 - 验证各个模块功能
"""
import sys
sys.path.insert(0, '/Users/fanyue/operational research/warehouse_system/backend')

from environment import Environment
from robot import RobotFleet, Robot
from order import OrderGenerator, Order, OrderPriority
from scheduler import PathPlanner, Scheduler
import time

def test_environment():
    """测试环境模块"""
    print("=" * 50)
    print("测试1: 环境模块")
    print("=" * 50)
    
    env = Environment(50, 50)
    env.create_default_warehouse()
    
    print(f"✅ 地图大小: {env.width}x{env.height}")
    print(f"✅ 障碍物数量: {len(env.obstacles)}")
    print(f"✅ 充电区数量: {len(env.charging_areas)}")
    print(f"✅ 目标点数量: {len(env.target_points)}")
    
    # 测试距离计算
    dist = env.manhattan_distance((0, 0), (5, 5))
    print(f"✅ 曼哈顿距离 (0,0)→(5,5): {dist}")
    
    # 测试可通行性
    walkable = env.is_walkable(10, 10)
    print(f"✅ 位置(10,10)可通行: {walkable}")
    
    print()

def test_robot():
    """测试机器人模块"""
    print("=" * 50)
    print("测试2: 机器人模块")
    print("=" * 50)
    
    robot = Robot(10, 10, max_capacity=100, max_battery=100.0)
    print(f"✅ 机器人ID: {robot.id}")
    print(f"✅ 初始位置: ({robot.x}, {robot.y})")
    print(f"✅ 初始电量: {robot.battery}%")
    print(f"✅ 初始状态: {robot.state.value}")
    
    # 测试任务分配
    task = {
        'order_id': 1,
        'pickup_location': (20, 20),
        'delivery_location': (30, 30),
    }
    robot.assign_task(task)
    print(f"✅ 分配任务后队列长度: {len(robot.task_queue)}")
    
    # 测试工作负载
    workload = robot.get_workload()
    print(f"✅ 机器人工作负载: {workload:.2f}")
    
    # 测试机器人集群
    fleet = RobotFleet(num_robots=5)
    print(f"✅ 机器人集群大小: {len(fleet.get_all_robots())}")
    print(f"✅ 空闲机器人数: {len(fleet.get_idle_robots())}")
    
    print()

def test_order():
    """测试订单系统"""
    print("=" * 50)
    print("测试3: 订单系统")
    print("=" * 50)
    
    generator = OrderGenerator(50, 50, base_interval=2.0)
    
    # 生成单个订单
    order = generator.generate_order()
    print(f"✅ 生成订单ID: {order.id}")
    print(f"✅ 订单优先级: {order.priority.name}")
    print(f"✅ 取货点: {order.pickup_location}")
    print(f"✅ 送货点: {order.delivery_location}")
    print(f"✅ 订单状态: {order.status.name}")
    
    # 生成批量订单
    orders = generator.generate_orders_batch(num_orders=3)
    print(f"✅ 批量生成订单数: {len(orders)}")
    
    # 测试紧迫性评分
    current_time = time.time()
    urgency = order.get_urgency_score(current_time)
    print(f"✅ 订单紧迫性评分: {urgency:.2f}")
    
    # 测试待分配订单
    pending = generator.get_pending_orders()
    print(f"✅ 待分配订单数: {len(pending)}")
    
    print()

def test_scheduler():
    """测试调度系统"""
    print("=" * 50)
    print("测试4: 调度系统（路径规划和任务分配）")
    print("=" * 50)
    
    env = Environment(50, 50)
    env.create_default_warehouse()
    
    fleet = RobotFleet(num_robots=3)
    path_planner = PathPlanner(env)
    scheduler = Scheduler(env, fleet, path_planner)
    
    # 测试路径规划
    start = (5, 5)
    goal = (40, 40)
    path = path_planner.plan_path(start, goal)
    print(f"✅ 路径规划: {start} → {goal}")
    print(f"✅ 路径长度: {len(path)} 步")
    if len(path) > 0:
        print(f"✅ 路径: {path[:5]}...（显示前5步）")
    
    # 测试任务分配成本计算
    robot = fleet.get_all_robots()[0]
    order = Order(
        id=1,
        pickup_location=(20, 20),
        delivery_location=(30, 30),
        priority=OrderPriority.HIGH,
    )
    current_time = time.time()
    cost_info = scheduler.calculate_assignment_cost(robot, order, current_time)
    print(f"\n✅ 任务分配成本计算:")
    print(f"   - 路径距离: {cost_info['distance']} 步")
    print(f"   - 估计完成时间: {cost_info['estimated_time']:.1f} 秒")
    print(f"   - 综合成本: {cost_info['composite_cost']:.2f}")
    
    # 测试最佳机器人选择
    best_robot = scheduler.select_best_robot(order, current_time)
    print(f"\n✅ 最佳机器人选择:")
    print(f"   - 机器人ID: {best_robot['robot_id']}")
    print(f"   - 综合成本: {best_robot['composite_cost']:.2f}")
    
    print()

def test_integration():
    """集成测试"""
    print("=" * 50)
    print("测试5: 集成测试")
    print("=" * 50)
    
    from simulator import WarehouseSimulator
    
    simulator = WarehouseSimulator(num_robots=3)
    print("✅ 模拟器初始化完成")
    
    # 运行几步模拟
    print("✅ 运行10步模拟...")
    for i in range(10):
        simulator.step(delta_time=1.0)
    
    # 获取系统状态
    state = simulator.get_state()
    print(f"✅ 当前时间: {state['current_time']:.1f}秒")
    print(f"✅ 完成步数: {state['step_count']}")
    print(f"✅ 待分配订单: {state['pending_orders']}")
    print(f"✅ 已完成任务: {state['metrics']['total_tasks_completed']}")
    print(f"✅ 总行驶距离: {state['metrics']['total_distance']:.1f}米")
    print(f"✅ 平均电量: {state['metrics']['average_battery']:.1f}%")
    
    print()

def run_all_tests():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " " * 10 + "多机器人仓储系统 - 功能测试" + " " * 10 + "║")
    print("╚" + "=" * 48 + "╝")
    print()
    
    try:
        test_environment()
        test_robot()
        test_order()
        test_scheduler()
        test_integration()
        
        print("=" * 50)
        print("✅ 所有测试通过！")
        print("=" * 50)
        print("\n现在可以启动应用了!")
        print("运行: python app.py")
        print("然后打开: frontend/index.html")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_all_tests()
