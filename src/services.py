# 业务逻辑类（增删改查、文件读写）
from src.models import teacher,experimenter,admin,teacher_admin
import json


class personService:
    def __init__(self):
        self.personList=[]

    def personIDCheck(self,personID:str):
        '''
        检查编号是否存在
        '''
        for p in self.personList:
            if p._personID==personID:
                return True
        return False

    def addPerson(self,person):
        '''
        按类添加
        '''
        #此处ID check在ui层实现
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

    def updatePerson(self,personID:str,person):
        '''
        双重检查，防止编号冲突并允许修改自身
        '''
        if self.personIDCheck(person._personID) and personID!=person._personID:
            return False
        for i,p in enumerate(self.personList):
            if p._personID==personID:
                self.personList[i]=person
                return True
        return False

    def deletePerson(self,personID:str):
        '''
        删除人员
        '''
        for p in self.personList:
            if p._personID==personID:
                self.personList.remove(p)
                return True
        return False

    def getPersonStatistics(self):
        '''
        统计各类人数，先检查子类再检查父类避免重复计数
        '''
        res={"教师":0,"实验员":0,"行政人员":0,"教师兼行政人员":0}
        for p in self.personList:
            if isinstance(p,teacher_admin):
                res["教师兼行政人员"]+=1
            elif isinstance(p,teacher):
                res["教师"]+=1
            elif isinstance(p,experimenter):
                res["实验员"]+=1
            elif isinstance(p,admin):
                res["行政人员"]+=1
        return res

    def save(self,filename:str='data/person.json'):
        '''
        由调用方决定何时保存，main层调用
        '''
        with open(filename,'w',encoding='utf-8') as f:
            json.dump([p.to_dict() for p in self.personList],
                      f,ensure_ascii=False,indent=4)

    def load(self,filename:str='data/person.json'):
        '''
        由调用方决定何时加载，main层调用
        '''
        classMap={c.__name__:c for c in [teacher,experimenter,admin,teacher_admin]}
        try:
            with open(filename,'r',encoding='utf-8') as f:
                dataList=json.load(f)
            self.personList.clear()
            for d in dataList:
                cls=classMap.get(d.get('__class__'),teacher)
                self.personList.append(cls.from_dict(d))
        except (FileNotFoundError,json.JSONDecodeError):
            pass

    def __str__(self):
        return ''.join([str(p)+'\n' for p in self.personList])
