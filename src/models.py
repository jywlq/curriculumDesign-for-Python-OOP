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

    @classmethod
    def from_dict(cls,d:dict):
        return cls(d['personID'],d['personName'],d['personGender'],d['personAge'])

    def to_dict(self):
        return {
            '__class__': 'baseClass',
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

    @classmethod
    def from_dict(cls,d:dict):
        return cls(d['personID'],d['personName'],d['personGender'],d['personAge'],
                   d['major'],d['professionalTitle'])

    def to_dict(self):
        data = super().to_dict()
        data.update({
            '__class__': 'teacher',
            'major': self._major,
            'professionalTitle': self._professionalTitle
        })
        return data

    def __repr__(self):
        return f"teacher(personID={self._personID}, personName={self._personName}, major={self._major}, professionalTitle={self._professionalTitle})"


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

    @classmethod
    def from_dict(cls,d:dict):
        return cls(d['personID'],d['personName'],d['personGender'],d['personAge'],
                   d['laboratory'],d['duties'])

    def to_dict(self):
        data = super().to_dict()
        data.update({
            '__class__': 'experimenter',
            'laboratory': self._laboratory,
            'duties': self._duties
        })
        return data

    def __repr__(self):
        return f"experimenter(personID={self._personID}, personName={self._personName}, laboratory={self._laboratory}, duties={self._duties})"

#行政人员
class admin(baseClass):
    def __init__(self,personID:str,personName:str,personGender:str,personAge:str,
                 politicalAppearance:str,professionalTitle:str):
        '''
        行政人员类：编号，姓名，性别，年龄，政治面貌，职称
        '''
        super().__init__(personID,personName,personGender,personAge)
        self._politicalAppearance=politicalAppearance
        self._professionalTitle=professionalTitle

    @classmethod
    def from_dict(cls,d:dict):
        return cls(d['personID'],d['personName'],d['personGender'],d['personAge'],
                   d['politicalAppearance'],d['professionalTitle'])

    def to_dict(self):
        data = super().to_dict()
        data.update({
            '__class__': 'admin',
            'politicalAppearance': self._politicalAppearance,
            'professionalTitle': self._professionalTitle
        })
        return data

    def __repr__(self):
        return f"admin(personID={self._personID}, personName={self._personName}, politicalAppearance={self._politicalAppearance}, professionalTitle={self._professionalTitle})"

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
        self._politicalAppearance=politicalAppearance

    @classmethod
    def from_dict(cls,d:dict):
        return cls(d['personID'],d['personName'],d['personGender'],d['personAge'],
                   d['major'],d['professionalTitle'],d['politicalAppearance'])

    def to_dict(self):
        data = teacher.to_dict(self)
        data.update({
            '__class__': 'teacher_admin',
            'politicalAppearance': self._politicalAppearance
        })
        return data

    def __repr__(self):
        return f"teacher_admin(personID={self._personID}, personName={self._personName}, major={self._major}, professionalTitle={self._professionalTitle}, politicalAppearance={self._politicalAppearance})"
