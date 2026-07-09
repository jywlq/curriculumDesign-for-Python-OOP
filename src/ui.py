# 命令行交互界面（菜单、输入输出）
import os
from src.models import teacher,experimenter,admin,teacher_admin
from src.services import personService

class BackToMenu(Exception):pass


class CmdUI:
    PERSON_TYPE={                               #字典映射类
        "1":teacher,
        "2":experimenter,
        "3":admin,
        "4":teacher_admin,
        "老师":teacher,
        "实验员":experimenter,
        "行政人员":admin,
        "老师兼行政人员":teacher_admin
    }

    def __init__(self):
        self.service=personService()
        '''
        菜单映射方法
        '''
        self.MENU={
            "1":self.addPerson,
            "2":self.deletePerson,
            "3":self.updatePerson,
            "4":self.findPerson,
            "5":self.getStatisticPerson,
        }
    def deletePerson(self):pass
    def updatePerson(self):pass
    def findPerson(self):pass
    def getStatisticPerson(self):pass

    def inputWithBack(self, value:str):
        '''
        带返回功能的输入，输入0抛BackToMenu异常
        '''
        if value=='0':
            raise BackToMenu()
        return value

    def isEmpty(self, value:str):
        '''
        判空，为空返回True并打印提示
        '''
        if not value.strip():
            print('输入不能为空')
            return True
        return False

    def clearScreen(self):
        '''
        清屏
        '''
        if os.name=='nt':
            os.system('cls')
        else:
            os.system('clear')

    def showMenu(self):
        print('欢迎使用人员信息管理系统')
        print('1. 添加人员')
        print('2. 删除人员')
        print('3. 修改人员信息')
        print('4. 查询人员信息')
        print('5. 统计人员信息')
        print('0. 退出系统')

    def run(self):
        self.service.load()
        try:
            while True:
                self.clearScreen()
                self.showMenu()
                choice=input('请输入操作编号：')
                if choice=='0':
                    self.service.save()
                    print('已保存，退出系统')
                    break
                func=self.MENU.get(choice)
                if func:
                    func()
                else:
                    print('无效的操作编号，请重新输入')
        except KeyboardInterrupt:
            self.service.save()
            print('\n已保存，退出系统')

    def selectType(self):
        '''
        选择人员类型，返回类对象
        '''
        while True:
            personType=self.inputWithBack(input("请输入人员类型或序号(1.老师/2.实验员/3.行政人员/4.老师兼行政人员)："))
            if self.isEmpty(personType):
                continue
            personClass=self.PERSON_TYPE.get(personType)
            if not personClass:
                print('无效的人员类型，请重新输入')
                continue
            return personClass

    def collectBaseInfo(self):
        '''
        收集baseClass的四个字段，返回字典
        '''
        while True:
            id=self.inputWithBack(input("请输入编号："))
            if self.isEmpty(id):
                continue
            if not id.isascii() or not id.isalnum():
                print('编号只能包含字母和数字，请重新输入')
                continue
            if self.service.personIDCheck(id):
                print('编号已存在，请重新输入')
                continue
            break
        while True:
            name=self.inputWithBack(input("请输入姓名："))
            if self.isEmpty(name):
                continue
            break
        while True:
            gender=self.inputWithBack(input("请输入性别："))
            if self.isEmpty(gender):
                continue
            if gender not in ('男','女'):
                print('性别只能是男或女，请重新输入')
                continue
            break
        while True:
            ageStr = self.inputWithBack(input("请输入年龄："))
            if self.isEmpty(ageStr):
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
                value=self.inputWithBack(input(f"请输入{prompt}："))
                if self.isEmpty(value):
                    continue
                data[field]=value
                break
        return data

    def addPerson(self):
        try:
            print('添加人员')
            print('输入0返回上级菜单')
            while True:
                personClass=self.selectType()
                data=self.collectBaseInfo()
                data.update(self.collectExtraFields(personClass))
                self.service.addPerson(personClass(**data))
                self.service.save()
                self.clearScreen()
                print('添加成功\n')
                print('0.返回上级菜单')
                choice=input('按enter继续添加人员：')
                if choice=='0':
                    return
        except BackToMenu:
            return
        except KeyboardInterrupt:
            self.service.save()
            return
