#数据类

#基类
class baseClass:
    def __init__(self,personID:str,personName:str,personGender:str,personAge:str):
        '''
        基类：编号，姓名，性别，年龄
        '''
        self._personID=personID
        self._personName=personName
        self._personGender=personGender
        self._personAge=personAge

#教师
class teacher(baseClass):
    def __init__(self,personID:str,personName:str,personGender:str,personAge:str,
                 major:str,professionalTitle:str):
        '''
        教师类：编号，姓名，性别，年龄,所在系部，专业，职称
        '''
        super().__init__(personID,personName,personGender,personAge)
        self._major=major
        self._professionalTitle=professionalTitle




#实验员
class experimenter(baseClass):
    def __init__(self,personID:str,personName:str,personGender:str,personAge:str,
                 laboratory:str,duties:str):
        '''
        实验员类：编号，姓名，性别，年龄，所在实验室，职务
        '''
        super().__init__(personID,personName,personGender,personAge)
        self._laboratory=laboratory
        self._duties=duties
        
#行政人员
class admin(classmethod):
    def __init__(self,personID:str,personName:str,personGender:str,personAge:str,
                 politicalAppearance:str,professionalTitle:str,):
        '''
        行政人员类：编号，姓名，性别，年龄，政治面貌，职称
        '''
        super().__init__(personID,personName,personGender,personAge)
        self._politicalAppearance=politicalAppearance
        self._professionalTitle=professionalTitle