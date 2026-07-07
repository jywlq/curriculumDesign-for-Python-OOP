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
        ID,Name=[],[]#暂存列表
        if personID!=' ':
            for p in self.personList:
                if p._personID.startswith(personID):
                    ID.append(p)
        if personName!=' ':
            for p in self.personList:
                if p._personName.startswith(personName):
                    Name.append(p)
        if not ID and not Name:
            return self.personList
        elif not ID:
            return Name
        elif not Name:
            return ID
        else:
            return list(set(ID).intersection(set(Name)))
    
    