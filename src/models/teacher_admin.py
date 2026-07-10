# 教师兼行政人员类
from src.models.base import baseClass
from src.models.teacher import teacher
from src.models.admin import admin

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
