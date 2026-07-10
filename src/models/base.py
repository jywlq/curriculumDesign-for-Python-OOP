# 基类
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
