# 命令行交互界面（菜单、输入输出）
import os
import json
from src.models import teacher,experimenter,admin,teacher_admin
from src.services import personService

class ReturnBack(Exception):pass


class PersonFilter:
    '''
    人员筛选器类：管理筛选状态，返回筛选结果列表
    '''
    def __init__(self, service):
        self.service=service
        self.filterID=''        # 编号筛选条件
        self.filterName=''      # 姓名筛选条件

    def updateID(self, value:str):
        '''更新编号筛选条件'''
        self.filterID=value

    def updateName(self, value:str):
        '''更新姓名筛选条件'''
        self.filterName=value

    def reset(self):
        '''重置所有筛选条件'''
        self.filterID=''
        self.filterName=''

    def getResult(self):
        '''获取筛选结果列表'''
        return self.service.findPerson(self.filterID, self.filterName)


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


class CmdUI:
    CONFIG_FILE='data/config.json'

    def __init__(self):
        self.service=personService()
        self.collector=PersonCollector(self.service)
        self.autoSaveOn=False
        self.loadConfig()
        '''
        菜单映射方法
        '''
        self.MENU={
            "1":self.addPerson,
            "2":self.findPerson,
            "3":self.showAllPerson,
            "4":self.updatePerson,
            "5":self.deletePerson,
            "6":self.getPersonStatistics,
            "7":self.autoSave,
            "8":self.save,
            "9":self.loadData,
        }
    
    def save(self):
        self.service.save()

    def loadData(self):
        self.service.load()

    def loadConfig(self):
        '''加载配置文件'''
        try:
            with open(self.CONFIG_FILE,'r',encoding='utf-8') as f:
                config=json.load(f)
            self.autoSaveOn=config.get('autoSaveOn',False)
        except (FileNotFoundError,json.JSONDecodeError):
            pass

    def saveConfig(self):
        '''保存配置文件'''
        with open(self.CONFIG_FILE,'w',encoding='utf-8') as f:
            json.dump({'autoSaveOn':self.autoSaveOn},f,ensure_ascii=False,indent=4)

    def saveIfAuto(self):       #识别自动存储开关
        if self.autoSaveOn:
            self.save()

    def dataChange(self):       #统一调用数据变更后操作
        self.saveIfAuto()
    
        
    def run(self):
        '''
        主循环
        '''
        self.loadData()
        try:
            while True:
                self.clearScreen()
                self.showMenu()
                choice=self.inputWithBack(input('请输入操作编号：'))
                func=self.MENU.get(choice)
                if func:
                    func()
                else:
                    self.showMessage('无效的操作编号')
        except (KeyboardInterrupt,ReturnBack):
            if self.autoSaveOn:
                self.save()
                print('\n已保存，退出系统')
            else:
                print('\n退出系统')
            
    def findPerson(self):
        '''
        列表筛选：初始显示全部，支持累积筛选（可组合编号和姓名条件）
        '''
        try:
            pf=PersonFilter(self.service)
            while True:
                self.clearScreen()
                print('========= 人员查询 =========')
                currentList=pf.getResult()
                print(f'共 {len(currentList)} 条记录\n')
                for i,p in enumerate(currentList,1):
                    print(f'{i}. {p}')
                if not currentList:
                    print('暂无符合条件的人员记录')
                self.showFilterMenu(pf)
                print('输入0返回上级菜单')
                choice=self.inputWithBack(input('\n请选择操作：'))
                if choice=='1':
                    keyword=self.inputWithBack(input('请输入编号前缀：'))
                    pf.updateID(keyword)
                elif choice=='2':
                    keyword=self.inputWithBack(input('请输入姓名前缀：'))
                    pf.updateName(keyword)
                elif choice=='3':
                    pf.reset()
                else:
                    self.showMessage('无效的操作编号')
        except KeyboardInterrupt:
            return
        except ReturnBack:
            return
        
    def showAllPerson(self):
        try:
            self.clearScreen()
            print("=========所有人员列表如下=========")
            for p in self.service.personList:
                print(p)
            self.inputWithBack(input("按enter返回上级菜单"))
        except KeyboardInterrupt:
            return
            
        
    def updatePerson(self):
        try:
            self.clearScreen()
            print('=========修改人员=========')
            print('输入0返回上级菜单')
            while True:
                personID=self.inputWithBack(input('请输入要修改的编号：'))
                if not personID.strip():
                    print('输入不能为空')
                    continue
                break
            personList=self.service.findPerson(personID)
            if not personList:
                print('未找到该编号对应的人员')
                return
            oldPerson=personList[0]
            personClass, data=self.collector.collect(oldPerson._personID)
            if self.service.updatePerson(personID,personClass(**data)):
                self.dataChange()
                print('修改成功')
            else:
                print('修改失败')
        except ReturnBack:
            return
        except KeyboardInterrupt:
            return

    def deletePerson(self):
        '''
        删除人员：复用筛选逻辑，用户筛选后输入序号删除
        '''
        try:
            pf=PersonFilter(self.service)
            while True:
                self.clearScreen()
                print('=========删除人员=========')
                currentList=pf.getResult()
                print(f'共 {len(currentList)} 条记录\n')
                for i,p in enumerate(currentList,1):
                    print(f'{i}. {p}')
                if not currentList:
                    print('暂无符合条件的人员记录')
                self.showFilterMenu(pf)
                print("4. 输入序号删除对应人员")
                print("输入0返回上级菜单")
                choice=self.inputWithBack(input('\n请选择操作'))
                if choice=='1':
                    keyword=self.inputWithBack(input('请输入编号前缀：'))
                    pf.updateID(keyword)
                elif choice=='2':
                    keyword=self.inputWithBack(input('请输入姓名前缀：'))
                    pf.updateName(keyword)
                elif choice=='3':
                    pf.reset()
                elif choice=='4':
                    idx=self.inputWithBack(input('请输入要删除的序号：'))
                    try:
                        self.deleteByIndex(int(idx)-1, currentList)
                    except ValueError:
                        self.showMessage('序号无效')
                else:
                    self.showMessage('无效的操作编号')
        except (KeyboardInterrupt, ReturnBack):
            return

    def getPersonStatistics(self):
        stat=self.service.getPersonStatistics()
        self.clearScreen()
        print('=========人员统计=========')
        for k,v in stat.items():
            print(f'{k}：{v}')
        self.inputWithBack(input('按enter返回上级菜单'))

    def autoSave(self):
        self.autoSaveOn=not self.autoSaveOn
        self.saveConfig()
        if self.autoSaveOn:
            self.showMessage('自动保存已开启')
        else:
            self.showMessage('自动保存已关闭')

    def inputWithBack(self, value:str):
        '''
        带返回功能的输入，0返回ReturnBack异常
        '''
        if value=='0':
            raise ReturnBack()
        return value

    def isEmpty(self, value:str):
        '''
        判空，为空返回True打印提示
        '''
        if not value.strip():
            print('输入不能为空')
            return True
        return False

    def showMessage(self, msg):
        '''清屏 → 显示提示 → 按enter继续'''
        self.clearScreen()
        print(msg)
        self.inputWithBack(input('按enter继续'))

    def showFilterMenu(self, pf):
        '''显示筛选菜单'''
        print()
        if pf.filterID:
            print(f'1. 按编号筛选 --> {pf.filterID}')
        else:
            print('1. 按编号筛选')
        if pf.filterName:
            print(f'2. 按姓名筛选 --> {pf.filterName}')
        else:
            print('2. 按姓名筛选')
        print('3. 重置（清除所有筛选）')

    def deleteByIndex(self, index, currentList):
        '''根据序号删除人员'''
        if index<0 or index>=len(currentList):
            raise ValueError
        personID=currentList[index]._personID
        self.clearScreen()
        if self.service.deletePerson(personID):
            self.dataChange()
            self.showMessage('删除成功')
        else:
            self.showMessage('序号无效')



    def clearScreen(self):
        '''
        清屏
        '''
        if os.name=='nt':
            os.system('cls')#Windows
        else:
            os.system('clear')#Linux/Mac

    def showMenu(self):
        print('欢迎使用人员信息管理系统')
        print('1. 添加人员')
        print('2. 查询人员')
        print('3. 显示人员')
        print('4. 修改人员')
        print('5. 删除人员')
        print('6. 统计人员')
        print('7. 自动保存',"(已开启)" if self.autoSaveOn else "(已关闭)")
        print('8. 手动保存')
        print('9. 读取数据')
        print('0. 退出系统')

    def addPerson(self):
        try:
            print('添加人员')
            print('输入0返回上级菜单')
            while True:
                personClass, data=self.collector.collect()
                self.service.addPerson(personClass(**data))
                self.dataChange()
                self.clearScreen()
                print('添加成功\n')
                self.inputWithBack(input('按enter继续添加人员，输入0返回：'))
        except ReturnBack:
            return
        except KeyboardInterrupt:
            return
