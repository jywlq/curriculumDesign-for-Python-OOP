# 业务逻辑类（增删改查、文件读写）
from src.models import baseClass,teacher,experimenter,admin,teacher_admin
import json


class personService:
    def __init__(self):
        self.personList=[]

    def addPerson(self,person:baseClass):
        for p in self.personList:
            if p._personID==person._personID:
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
    
    def deletePerson(self,person:baseClass):
        for p in self.personList:
            if p is person:
                p._deleted=True
                '''
                标记删除，避免移动列表后续元素，提高效率
                '''
                self.save()
                return
    def save(self,filename:str='data/person.json'):#存储
        with open(filename,'w',encoding='utf-8') as f:
            json.dump([p.to_dict() for p in self.personList if not p._deleted],
                      f,ensure_ascii=False,indent=4)
            
    def load(self,filename:str='data/person.json'):#加载
        try:
            with open(filename,'r',encoding='utf-8') as f:
                data_list=json.load(f)
            self.personList.clear()
            for d in data_list:
                pid=d['personID']
                pname=d['personName']
                pgender=d['personGender']
                page=d['personAge']
                if 'major' in d and 'politicalAppearance' in d:
                    obj=teacher_admin(pid,pname,pgender,page,
                                      d['major'],d['professionalTitle'],d['politicalAppearance'])
                elif 'major' in d:
                    obj=teacher(pid,pname,pgender,page,
                                d['major'],d['professionalTitle'])
                elif 'laboratory' in d:
                    obj=experimenter(pid,pname,pgender,page,
                                     d['laboratory'],d['duties'])
                elif 'politicalAppearance' in d:
                    obj=admin(pid,pname,pgender,page,
                              d['politicalAppearance'],d['professionalTitle'])
                else:
                    obj=baseClass(pid,pname,pgender,page)
                self.personList.append(obj)
        except FileNotFoundError:
            pass
        return self.personList
