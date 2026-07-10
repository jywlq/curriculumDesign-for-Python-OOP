# 人员筛选器类
class PersonFilter:
    '''
    人员筛选器类：管理筛选状态，返回筛选结果列表
    '''
    def __init__(self, service):
        self.service = service
        self.filter_id = ''  # 编号筛选条件
        self.filter_name = ''  # 姓名筛选条件

    def update_id(self, value: str):
        '''更新编号筛选条件'''
        self.filter_id = value

    def update_name(self, value: str):
        '''更新姓名筛选条件'''
        self.filter_name = value

    def reset(self):
        '''重置所有筛选条件'''
        self.filter_id = ''
        self.filter_name = ''

    def get_result(self):
        '''获取筛选结果列表'''
        return self.service.find_person(self.filter_id, self.filter_name)
