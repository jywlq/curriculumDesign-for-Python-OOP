# 命令行交互界面（菜单、输入输出）
import os
import json
from src.services import personService
from src.ui.exceptions import ReturnBack
from src.ui.filter import PersonFilter
from src.ui.collector import PersonCollector


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
            self.save()
            print('\n已保存，退出系统')
            
            
    def findPerson(self):
        '''
        列表筛选：初始显示全部，支持累积筛选
        '''
        self._filterList('人员查询')
        
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
        '''
        修改人员：复用筛选逻辑，用户筛选后输入序号修改
        '''
        person=self._filterList('修改人员', '修改')
        if person:
            self.updateByIndex(person)

    def deletePerson(self):
        '''
        删除人员：复用筛选逻辑，用户筛选后输入序号删除
        '''
        pf=PersonFilter(self.service)
        while True:
            person=self._filterList('删除人员', '删除', pf)
            if not person:
                return
            self.deleteByIndex(person)

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

    def _filterList(self, title, actionName=None, pf=None):
        '''
        通用的筛选+选择人员流程
        title: 页面标题
        actionName: 操作名称，如"删除"/"修改"，None表示只查询
        pf: PersonFilter对象，为None时创建新的
        返回: 选中的人员对象，或 None（用户返回或只查询）
        '''
        try:
            if pf is None:
                pf=PersonFilter(self.service)
            while True:
                self.clearScreen()
                print(f'========={title}=========')
                currentList=pf.getResult()
                print(f'共 {len(currentList)} 条记录\n')
                for i,p in enumerate(currentList,1):
                    print(f'{i}. {p}')
                if not currentList:
                    print('暂无符合条件的人员记录')
                self.showFilterMenu(pf)
                if actionName:
                    print(f"4. 输入序号{actionName}对应人员")
                print("输入0返回上级菜单")
                choice=self.inputWithBack(input('\n请选择操作：'))
                if choice=='1':
                    keyword=self.inputWithBack(input('请输入编号前缀：'))
                    pf.updateID(keyword)
                elif choice=='2':
                    keyword=self.inputWithBack(input('请输入姓名前缀：'))
                    pf.updateName(keyword)
                elif choice=='3':
                    pf.reset()
                elif choice=='4' and actionName:
                    idx=self.inputWithBack(input(f'请输入要{actionName}的序号：'))
                    try:
                        index=int(idx)-1
                        if index<0 or index>=len(currentList):
                            raise ValueError
                        return currentList[index]
                    except ValueError:
                        self.showMessage('序号无效')
                else:
                    if actionName:
                        self.showMessage('无效的操作编号')
        except (KeyboardInterrupt, ReturnBack):
            return None

    def deleteByIndex(self, person):
        '''删除人员，返回是否成功'''
        while True:
            confirm=self.inputWithBack(input(f'确认删除 {person._personName}({person._personID})？(y/n)：'))
            if confirm.lower()=='y':
                if self.service.deletePerson(person._personID):
                    self.dataChange()
                    self.showMessage('删除成功')
                    return True
                else:
                    self.showMessage('删除失败')
                    return False
            elif confirm.lower()=='n':
                return False
            else:
                print('请输入y或n')

    def updateByIndex(self, person):
        '''修改人员'''
        try:
            personClass, data=self.collector.collect(person._personID)
        except (ReturnBack, KeyboardInterrupt):
            return
        if self.service.updatePerson(person._personID, personClass(**data)):
            self.dataChange()
            self.showMessage('修改成功')
        else:
            self.showMessage('修改失败')



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
