"""
Flask后端服务器
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time
from simulator import get_simulator, reset_simulator

app = Flask(__name__)
CORS(app)  # 启用CORS

# 模拟器线程
simulator_thread = None
running = False

def simulation_loop():
    """后台模拟循环"""
    global running
    simulator = get_simulator()
    
    while running:
        simulator.step(delta_time=0.5)
        time.sleep(0.1)  # 控制模拟速度

@app.route('/api/status', methods=['GET'])
def get_status():
    """获取系统状态"""
    try:
        simulator = get_simulator()
        state = simulator.get_state()
        return jsonify({
            'success': True,
            'data': state
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/robots', methods=['GET'])
def get_robots():
    """获取所有机器人信息"""
    try:
        simulator = get_simulator()
        robots = simulator.robot_fleet.get_fleet_status()
        return jsonify({
            'success': True,
            'data': robots
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """获取所有订单"""
    try:
        simulator = get_simulator()
        orders = [o.to_dict() for o in simulator.order_generator.get_all_orders()]
        return jsonify({
            'success': True,
            'data': orders
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """获取系统性能指标"""
    try:
        simulator = get_simulator()
        metrics = simulator.scheduler.get_system_metrics()
        return jsonify({
            'success': True,
            'data': metrics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/grid', methods=['GET'])
def get_grid():
    """获取地图网格"""
    try:
        simulator = get_simulator()
        grid = simulator.environment.get_grid_state()
        
        # 添加机器人位置信息
        robot_positions = []
        for robot in simulator.robot_fleet.get_all_robots():
            robot_positions.append({
                'id': robot.id,
                'x': robot.x,
                'y': robot.y,
                'state': robot.state.value if hasattr(robot.state, 'value') else str(robot.state),
                'battery': robot.battery,
            })
        
        return jsonify({
            'success': True,
            'data': {
                'grid': grid,
                'width': simulator.environment.width,
                'height': simulator.environment.height,
                'robots': robot_positions,
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/simulation/start', methods=['POST'])
def start_simulation():
    """启动模拟"""
    global running, simulator_thread
    
    try:
        if not running:
            running = True
            simulator_thread = threading.Thread(target=simulation_loop, daemon=True)
            simulator_thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Simulation started',
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/simulation/pause', methods=['POST'])
def pause_simulation():
    """暂停模拟"""
    global running
    running = False
    return jsonify({
        'success': True,
        'message': 'Simulation paused',
    })

@app.route('/api/simulation/reset', methods=['POST'])
def reset_simulation_api():
    """重置模拟"""
    global running
    running = False
    reset_simulator()
    return jsonify({
        'success': True,
        'message': 'Simulation reset',
    })

@app.route('/api/simulation/step', methods=['POST'])
def step_simulation():
    """执行一步模拟"""
    try:
        data = request.get_json() or {}
        delta_time = data.get('delta_time', 1.0)
        
        simulator = get_simulator()
        simulator.step(delta_time)
        
        return jsonify({
            'success': True,
            'data': simulator.get_state()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """获取事件日志"""
    try:
        simulator = get_simulator()
        limit = request.args.get('limit', 50, type=int)
        events = simulator.events_log[-limit:]
        return jsonify({
            'success': True,
            'data': events
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/robot/<int:robot_id>', methods=['GET'])
def get_robot_detail(robot_id):
    """获取特定机器人详情"""
    try:
        simulator = get_simulator()
        robot = simulator.robot_fleet.get_robot(robot_id)
        
        if not robot:
            return jsonify({
                'success': False,
                'error': 'Robot not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': robot.get_status()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
