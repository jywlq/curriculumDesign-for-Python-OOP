# 人员信息收集器类
from src.models import teacher,experimenter,admin,teacher_admin
from src.ui.exceptions import ReturnBack

class PersonCollector:
    '''
    人员信息收集器类：封装人员信息的输入收集逻辑
    '''
    PERSON_TYPE={
        "1":teacher,
        "2":experimenter,
        "3":admin,
        "4":teacher_admin,
        "老师":teacher,
        "实验员":experimenter,
        "行政人员":admin,
        "老师兼行政人员":teacher_admin
    }

    def __init__(self, service):
        self.service=service

    def selectType(self):
        '''
        选择人员类型，返回类对象
        '''
        while True:
            personType=input("请输入人员类型或序号(1.老师/2.实验员/3.行政人员/4.老师兼行政人员)：")
            if personType=='0':
                raise ReturnBack()
            if not personType.strip():
                print('输入不能为空')
                continue
            personClass=self.PERSON_TYPE.get(personType)
            if not personClass:
                print('无效的人员类型，请重新输入')
                continue
            return personClass

    def collectBaseInfo(self, oldID:str=''):
        '''
        收集baseClass的四个字段，返回字典
        '''
        while True:
            id=input("请输入编号：")
            if id=='0':
                raise ReturnBack()
            if not id.strip():
                print('输入不能为空')
                continue
            if not id.isascii() or not id.isalnum():
                print('编号只能包含字母和数字，请重新输入')
                continue
            if id!=oldID and self.service.personIDCheck(id):
                print('编号已存在，请重新输入')
                continue
            break
        while True:
            name=input("请输入姓名：")
            if name=='0':
                raise ReturnBack()
            if not name.strip():
                print('输入不能为空')
                continue
            break
        while True:
            gender=input("请输入性别：")
            if gender=='0':
                raise ReturnBack()
            if not gender.strip():
                print('输入不能为空')
                continue
            if gender not in ('男','女'):
                print('性别只能是男或女，请重新输入')
                continue
            break
        while True:
            ageStr=input("请输入年龄：")
            if ageStr=='0':
                raise ReturnBack()
            if not ageStr.strip():
                print('输入不能为空')
                continue
            try:
                age = int(ageStr)
                if 1 <= age <= 150:
                    break
                else:
                    print("年龄必须在1到150之间")
            except ValueError:
                print("年龄必须是一个整数")
        return {"personID":id,"personName":name,"personGender":gender,"personAge":age}

    def collectExtraFields(self, personClass):
        '''
        收集类特有字段，调用getFields()获取字段列表，返回字典
        '''
        data={}
        for field,prompt in personClass.getFields():
            while True:
                value=input(f"请输入{prompt}：")
                if value=='0':
                    raise ReturnBack()
                if not value.strip():
                    print('输入不能为空')
                    continue
                data[field]=value
                break
        return data

    def collect(self, oldID:str=''):
        '''
        收集完整人员信息，返回(类型类, 数据字典)
        '''
        personClass=self.selectType()
        data=self.collectBaseInfo(oldID)
        data.update(self.collectExtraFields(personClass))
        return personClass, data
