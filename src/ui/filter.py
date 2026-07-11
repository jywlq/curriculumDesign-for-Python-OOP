"""
人员筛选器模块
"""
from typing import List


class PersonFilter:
    """人员筛选器：管理编号/姓名的筛选状态，返回筛选结果"""

    def __init__(self, service):
        self.service = service
        self.filter_id = ''    # 编号前缀筛选条件
        self.filter_name = ''  # 姓名前缀筛选条件

    def update_id(self, value: str):
        self.filter_id = value

    def update_name(self, value: str):
        self.filter_name = value

    def reset(self):
        """重置所有筛选条件"""
        self.filter_id = ''
        self.filter_name = ''

    def get_result(self) -> List:
        """调用 service 的 find_person 获取筛选结果"""
        return self.service.find_person(self.filter_id, self.filter_name)
