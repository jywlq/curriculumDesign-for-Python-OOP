# 教师类
from src.models.base import baseClass

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
