# 命令行交互界面（菜单、输入输出）
import os
from src.models import teacher,experimenter,admin,teacher_admin
from src.services import personService

class BackToMenu(Exception):pass


class CmdUI:
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

    def addPerson(self):
        PERSON_TYPE={                           #局部字典映射类
            "1":teacher,
            "2":experimenter,
            "3":admin,
            "4":teacher_admin,
            "老师":teacher,
            "实验员":experimenter,
            "行政人员":admin,
            "老师兼行政人员":teacher_admin
        }
        PERSON_FIELDS={                         #局部字典映射类对应的字段和提示
            teacher:[("major","专业"),("professionalTitle","职称")],
            experimenter:[("laboratory","实验室"),("duties","职务")],
            admin:[("politicalAppearance","政治面貌"),("professionalTitle","职称")],
            teacher_admin:[("major","专业"),("professionalTitle","职称"),("politicalAppearance","政治面貌")]
        }
        try:
            print('添加人员')
            print('输入0返回上级菜单')
            while True:
                personType=self.inputWithBack(input("请输入人员类型或序号(1.老师/2.实验员/3.行政人员/4.老师兼行政人员)："))
                if self.isEmpty(personType):          #判空
                    continue
                personClass=PERSON_TYPE.get(personType)
                if not personClass:
                    print('无效的人员类型，请重新输入')
                    continue
                while True:
                    id=self.inputWithBack(input("请输入编号："))
                    if self.isEmpty(id):              #判空
                        continue
                    if not id.isascii() or not id.isalnum():  #编号只能英文和数字
                        print('编号只能包含字母和数字，请重新输入')
                        continue
                    if self.service.personIDCheck(id):  #编号不能重复
                        print('编号已存在，请重新输入')
                        continue
                    break
                while True:
                    name=self.inputWithBack(input("请输入姓名："))
                    if self.isEmpty(name):            #判空
                        continue
                    break
                while True:
                    gender=self.inputWithBack(input("请输入性别："))
                    if self.isEmpty(gender):          #判空
                        continue
                    if gender not in ('男','女'):       #性别只能男或女
                        print('性别只能是男或女，请重新输入')
                        continue
                    break
                while True:
                    age=self.inputWithBack(input("请输入年龄："))
                    if self.isEmpty(age):             #判空
                        continue
                    if not age.isdigit():               #年龄只能数字
                        print('年龄只能是数字，请重新输入')
                        continue
                    break
                data={"personID":id,"personName":name,"personGender":gender,"personAge":age}
                for field,prompt in PERSON_FIELDS[personClass]:
                    while True:
                        value=self.inputWithBack(input(f"请输入{prompt}："))
                        if self.isEmpty(value):       #判空
                            continue
                        data[field]=value
                        break
                self.service.addPerson(personClass(**data))
                self.service.save()
                self.clearScreen()
                print('添加成功\n')
                print('0.返回上级菜单')
                choice=input('按enter继续添加人员：')
                if choice=='0':
                    return
        except BackToMenu:                  #0异常返回上级菜单
            return
        except KeyboardInterrupt:
            self.service.save()
            return
