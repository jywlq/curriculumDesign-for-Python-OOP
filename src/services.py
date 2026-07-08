# 业务逻辑类（增删改查、文件读写）
from src.models import baseClass,teacher,experimenter,admin,teacher_admin
import json


class personService:
    def __init__(self):
        self.personList=[]


    def personIDcheck(self,personID:str):
        '''
        检查编号是否存在
        '''
        for p in self.personList:
            if p._personID==personID:
                return True
        return False

    def addPerson(self,person:baseClass):
        '''
        按类添加
        '''
        if self.personIDcheck(person._personID):
            return False
        self.personList.append(person)
        return True

    def findPerson(self,personID:str='',personName:str=''):
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
    
    def deletePerson(self,personID:str):
        for p in self.personList:
            if p._personID==personID:
                self.personList.remove(p)
                return True
        return False
    
    def updatePerson(self,personID:str,person:baseClass):
        if self.personIDcheck(person._personID) and personID!=person._personID:
            '''
            双重检查，防止编号冲突并允许修改自身
            '''
            return False
        for i,p in enumerate(self.personList):
            if p._personID==personID:
                self.personList[i]=person
                return True
        return False
    
    
    def save(self,filename:str='data/person.json'):
        '''
        由调用方决定何时保存，main层调用
        '''
        with open(filename,'w',encoding='utf-8') as f:
            json.dump([p.to_dict() for p in self.personList],
                      f,ensure_ascii=False,indent=4)
            
            
    '''
    核心save和load方法，供外部调用  
    '''
    def load(self,filename:str='data/person.json'):
        '''
        由调用方决定何时加载，main层调用
        '''
        classMap={c.__name__:c for c in [baseClass,teacher,experimenter,admin,teacher_admin]}
        #classmap方法：将类名映射到类对象，便于从字典中恢复对象
        try:
            with open(filename,'r',encoding='utf-8') as f:
                data_list=json.load(f)
            self.personList.clear()
            for d in data_list:
                cls=classMap.get(d.get('__class__','baseClass'),baseClass)
                self.personList.append(cls.from_dict(d))
        except FileNotFoundError:
            pass
    
    '''
    test
    '''
    def __str__(self):
        return ''.join([str(p)+'\n' for p in self.personList])
    
    '''
    testEnd
    '''
