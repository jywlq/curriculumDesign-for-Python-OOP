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
        self._deleted=False  #deleted表示是否删除
        
    def to_dict(self):
        return {
            'personID': self._personID,
            'personName': self._personName,
            'personGender': self._personGender,
            'personAge': self._personAge
        }
    
    def __repr__(self):
        return f"baseClass(personID={self._personID}, personName={self._personName}, personGender={self._personGender}, personAge={self._personAge})"
    

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
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'major': self._major,
            'professionalTitle': self._professionalTitle
        })
        return data
    
    def __repr__(self):
        super_repr = super().__repr__()
        return f"teacher({super_repr}, major={self._major}, professionalTitle={self._professionalTitle})"
    
    



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
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'laboratory': self._laboratory,
            'duties': self._duties
        })
        return data
    
    def __repr__(self):
        super_repr = super().__repr__()
        return f"experimenter({super_repr}, laboratory={self._laboratory}, duties={self._duties})"
        
#行政人员
class admin(baseClass):
    def __init__(self,personID:str,personName:str,personGender:str,personAge:str,
                 politicalAppearance:str,professionalTitle:str,):
        '''
        行政人员类：编号，姓名，性别，年龄，政治面貌，职称
        '''
        super().__init__(personID,personName,personGender,personAge)
        self._politicalAppearance=politicalAppearance
        self._professionalTitle=professionalTitle
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'politicalAppearance': self._politicalAppearance,
            'professionalTitle': self._professionalTitle
        })
        return data
    
    def __repr__(self):
        super_repr = super().__repr__()
        return f"admin({super_repr}, politicalAppearance={self._politicalAppearance}, professionalTitle={self._professionalTitle})"
        
#教师兼行政人员
class teacher_admin(teacher,admin):
    def __init__(self,personID:str,personName:str,personGender:str,personAge:str,
                 major:str,professionalTitle:str,
                 politicalAppearance:str):
        '''
        教师兼行政人员类：编号，姓名，性别，年龄，所在系部，专业，职称，政治面貌
        '''
        teacher.__init__(self,personID,personName,personGender,personAge,
                         major,professionalTitle)
        admin.__init__(self,personID,personName,personGender,personAge,
                       politicalAppearance,professionalTitle)
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'major': self._major,
            'professionalTitle': self._professionalTitle,
            'politicalAppearance': self._politicalAppearance
        })
        return data
    
    def __repr__(self):
        super_repr = super().__repr__()
        return f"teacher_admin({super_repr}, major={self._major}, professionalTitle={self._professionalTitle}, politicalAppearance={self._politicalAppearance})"
    