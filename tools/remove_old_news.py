"""
Currently not in use.
"""

from datetime import datetime


def is_over_days(date_str: str, days: int = 14) -> bool:
    """判断当前运行日期距离目标日期字符串是否超过指定天数（包含前后双向）。

    参数:
        date_str: 格式为 'YYYYMMDD' 的日期字符串，例如 '20260820'
        days: 间隔天数，默认为 14

    返回:
        bool: 间隔达到或超过指定天数返回 True，否则返回 False
    """
    # 将字符串解析为 date 对象
    target_date = datetime.strptime(date_str, "%Y%m%d").date()

    # 获取代码运行当天的日期
    today = datetime.now().date()

    # 计算两个日期之间的天数差
    diff_days = (today - target_date).days

    # 判断是否达到或超过指定天数
    return diff_days > days


# --- 使用示例 ---
print(is_over_days("20261120"))
