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
    def getFields(cls):
        return []

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

    def __str__(self):
        return f"{self._personName}({self._personID})，{self._personGender}，{self._personAge}岁"


#教师
class teacher(baseClass):
    def __init__(self,personID:str,personName:str,personGender:str,personAge:str,
                 department:str,major:str,professionalTitle:str):
        '''
        教师类：编号，姓名，性别，年龄,所在系部，专业，职称
        '''
        super().__init__(personID,personName,personGender,personAge)
        self._department=department
        self._major=major
        self._professionalTitle=professionalTitle

    @classmethod
    def getFields(cls):
        return [("department","所在系部"),("major","专业"),("professionalTitle","职称")]

    @classmethod
    def from_dict(cls,d:dict):
        return cls(d['personID'],d['personName'],d['personGender'],d['personAge'],
                   d.get('department',''),d['major'],d['professionalTitle'])

    def to_dict(self):
        data = super().to_dict()
        data.update({
            '__class__': 'teacher',
            'department': self._department,
            'major': self._major,
            'professionalTitle': self._professionalTitle
        })
        return data

    def __repr__(self):
        return f"teacher(personID={self._personID}, personName={self._personName}, personGender={self._personGender}, personAge={self._personAge}, department={self._department}, major={self._major}, professionalTitle={self._professionalTitle})"

    def __str__(self):
        return f"{self._personName}({self._personID})，{self._personGender}，{self._personAge}岁，{self._department}，{self._major}，{self._professionalTitle}"


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
    def getFields(cls):
        return [("laboratory","所在实验室"),("duties","职务")]

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
        return f"experimenter(personID={self._personID}, personName={self._personName}, personGender={self._personGender}, personAge={self._personAge}, laboratory={self._laboratory}, duties={self._duties})"

    def __str__(self):
        return f"{self._personName}({self._personID})，{self._personGender}，{self._personAge}岁，{self._laboratory}，{self._duties}"

#行政人员
class admin(baseClass):
    def __init__(self,personID:str,personName:str,personGender:str,personAge:str,
                 politicalAffiliation:str,professionalTitle:str):
        '''
        行政人员类：编号，姓名，性别，年龄，政治面貌，职称
        '''
        super().__init__(personID,personName,personGender,personAge)
        self._politicalAffiliation=politicalAffiliation
        self._professionalTitle=professionalTitle

    @classmethod
    def getFields(cls):
        return [("politicalAffiliation","政治面貌"),("professionalTitle","职称")]

    @classmethod
    def from_dict(cls,d:dict):
        return cls(d['personID'],d['personName'],d['personGender'],d['personAge'],
                   d['politicalAffiliation'],d['professionalTitle'])

    def to_dict(self):
        data = super().to_dict()
        data.update({
            '__class__': 'admin',
            'politicalAffiliation': self._politicalAffiliation,
            'professionalTitle': self._professionalTitle
        })
        return data

    def __repr__(self):
        return f"admin(personID={self._personID}, personName={self._personName}, personGender={self._personGender}, personAge={self._personAge}, politicalAffiliation={self._politicalAffiliation}, professionalTitle={self._professionalTitle})"

    def __str__(self):
        return f"{self._personName}({self._personID})，{self._personGender}，{self._personAge}岁，{self._politicalAffiliation}，{self._professionalTitle}"

#教师兼行政人员
class teacher_admin(teacher,admin):
    def __init__(self,personID:str,personName:str,personGender:str,personAge:str,
                 department:str,major:str,professionalTitle:str,
                 politicalAffiliation:str):
        '''
        教师兼行政人员类：编号，姓名，性别，年龄，所在系部，专业，职称，政治面貌
        '''
        baseClass.__init__(self,personID,personName,personGender,personAge)
        self._department=department
        self._major=major
        self._professionalTitle=professionalTitle
        self._politicalAffiliation=politicalAffiliation

    @classmethod
    def getFields(cls):
        return [("department","所在系部"),("major","专业"),("professionalTitle","职称"),("politicalAffiliation","政治面貌")]

    @classmethod
    def from_dict(cls,d:dict):
        return cls(d['personID'],d['personName'],d['personGender'],d['personAge'],
                   d.get('department',''),d['major'],d['professionalTitle'],d['politicalAffiliation'])

    def to_dict(self):
        data = teacher.to_dict(self)
        data.update({
            '__class__': 'teacher_admin',
            'politicalAffiliation': self._politicalAffiliation
        })
        return data

    def __repr__(self):
        return f"teacher_admin(personID={self._personID}, personName={self._personName}, personGender={self._personGender}, personAge={self._personAge}, department={self._department}, major={self._major}, professionalTitle={self._professionalTitle}, politicalAffiliation={self._politicalAffiliation})"

    def __str__(self):
        return f"{self._personName}({self._personID})，{self._personGender}，{self._personAge}岁，{self._department}，{self._major}，{self._professionalTitle}，{self._politicalAffiliation}"
