import time
import random


def generate_drag_trajectory(distance, start_x=100, start_y=200, raw_step=5, delay=0.01, max_points_amount=50):
    """
    生成拖动轨迹，返回格式为 [x, y, dt] 的数组，最多 max_points_amount 个点
    """
    raw_x = start_x
    raw_timestamp = time.time()
    trajectory = []

    # 原始轨迹（细粒度）
    for dx in range(0, distance + 1, raw_step):
        current_x = start_x + dx
        current_y = start_y + random.randint(-2, 2)  # 上下抖动
        dt = int((time.time() - raw_timestamp) * 1000)  # 毫秒
        trajectory.append([current_x, current_y, dt])
        time.sleep(delay)

    # 降采样为最多 max_points_amount 个点
    if len(trajectory) > max_points_amount:
        total = len(trajectory)
        step = (total - 1) / (max_points_amount - 1)
        indices = [round(i * step) for i in range(max_points_amount)]
        trajectory = [trajectory[i] for i in indices]

    return trajectory


print(generate_drag_trajectory(210, start_x=1018, start_y=1962))
