# 行政人员类
from src.models.base import baseClass

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
