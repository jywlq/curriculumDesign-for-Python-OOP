# 业务逻辑类（增删改查、文件读写）
from src.models import baseClass,teacher,admin,teacher_admin

class personService:
    def __init__(self):
        self.personList=[]

    def addPerson(self,person:baseClass):
        for p in self.personList:
            if p._personID==person._personID:
                return False
        self.personList.append(person)
        return True

    def findPerson(self,personID:str,personName:str):
        '''
        前缀查询
        '''
        if not personID and not personName:
            return self.personList
        result=[]
        for p in self.personList:
            if p._personID.startswith(personID) and p._personName.startswith(personName):
                result.append(p)
        return result
    
    