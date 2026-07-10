# 实验员类
from src.models.base import baseClass

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
