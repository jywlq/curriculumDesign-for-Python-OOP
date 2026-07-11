"""
异常类模块

定义 ReturnBack 异常，用于实现"输入 0 返回上级菜单"的控制流。
"""


class ReturnBack(Exception):
    """用户输入 0 时抛出，由上层捕获后返回上级菜单"""
    pass
