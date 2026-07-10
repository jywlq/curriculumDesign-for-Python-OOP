# 人员筛选器类
class PersonFilter:
    '''
    人员筛选器类：管理筛选状态，返回筛选结果列表
    '''
    def __init__(self, service):
        self.service=service
        self.filterID=''        # 编号筛选条件
        self.filterName=''      # 姓名筛选条件

    def updateID(self, value:str):
        '''更新编号筛选条件'''
        self.filterID=value

    def updateName(self, value:str):
        '''更新姓名筛选条件'''
        self.filterName=value

    def reset(self):
        '''重置所有筛选条件'''
        self.filterID=''
        self.filterName=''

    def getResult(self):
        '''获取筛选结果列表'''
        return self.service.findPerson(self.filterID, self.filterName)
