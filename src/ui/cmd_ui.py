# 命令行交互界面（菜单、输入输出）
import os
import json
from src.services import PersonService
from src.ui.exceptions import ReturnBack
from src.ui.filter import PersonFilter
from src.ui.collector import PersonCollector


class CmdUI:
    CONFIG_FILE = 'data/config.json'

    def __init__(self):
        self.service = PersonService()
        self.collector = PersonCollector(self.service)
        self.auto_save_on = False
        self.load_config()
        '''
        菜单映射方法
        '''
        self.MENU = {
            "1": self.add_person,
            "2": self.find_person,
            "3": self.show_all_person,
            "4": self.update_person,
            "5": self.delete_person,
            "6": self.get_person_statistics,
            "7": self.auto_save,
            "8": self.save,
            "9": self.load_data,
        }

    def save(self):
        self.service.save()

    def load_data(self):
        self.service.load()

    def load_config(self):
        '''加载配置文件'''
        try:
            with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.auto_save_on = config.get('autoSaveOn', False)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_config(self):
        '''保存配置文件'''
        with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({'autoSaveOn': self.auto_save_on}, f, ensure_ascii=False, indent=4)

    def save_if_auto(self):  # 识别自动存储开关
        if self.auto_save_on:
            self.save()

    def data_change(self):  # 统一调用数据变更后操作
        self.save_if_auto()

    def run(self):
        '''
        主循环
        '''
        self.load_data()
        try:
            while True:
                self.clear_screen()
                self.show_menu()
                choice = self.input_with_back(input('请输入操作编号：'))
                func = self.MENU.get(choice)
                if func:
                    func()
                else:
                    self.show_message('无效的操作编号')
        except (KeyboardInterrupt, ReturnBack):
            self.save()
            print('\n已保存，退出系统')

    def find_person(self):
        '''
        列表筛选：初始显示全部，支持累积筛选
        '''
        self._filter_list('人员查询')

    def show_all_person(self):
        try:
            self.clear_screen()
            print("=========所有人员列表如下=========")
            for p in self.service.person_list:
                print(p)
            self.input_with_back(input("按enter返回上级菜单"))
        except KeyboardInterrupt:
            return

    def update_person(self):
        '''
        修改人员：复用筛选逻辑，用户筛选后输入序号修改
        '''
        person = self._filter_list('修改人员', '修改')
        if person:
            self.update_by_index(person)

    def delete_person(self):
        '''
        删除人员：复用筛选逻辑，用户筛选后输入序号删除
        '''
        pf = PersonFilter(self.service)
        while True:
            person = self._filter_list('删除人员', '删除', pf)
            if not person:
                return
            self.delete_by_index(person)

    def get_person_statistics(self):
        stat = self.service.get_person_statistics()
        self.clear_screen()
        print('=========人员统计=========')
        for k, v in stat.items():
            print(f'{k}：{v}')
        self.input_with_back(input('按enter返回上级菜单'))

    def auto_save(self):
        self.auto_save_on = not self.auto_save_on
        self.save_config()
        if self.auto_save_on:
            self.show_message('自动保存已开启')
        else:
            self.show_message('自动保存已关闭')

    def input_with_back(self, value: str):
        '''
        带返回功能的输入，0返回ReturnBack异常
        '''
        if value == '0':
            raise ReturnBack()
        return value

    def is_empty(self, value: str):
        '''
        判空，为空返回True打印提示
        '''
        if not value.strip():
            print('输入不能为空')
            return True
        return False

    def show_message(self, msg):
        '''清屏 → 显示提示 → 按enter继续'''
        self.clear_screen()
        print(msg)
        self.input_with_back(input('按enter继续'))

    def show_filter_menu(self, pf):
        '''显示筛选菜单'''
        print()
        if pf.filter_id:
            print(f'1. 按编号筛选 --> {pf.filter_id}')
        else:
            print('1. 按编号筛选')
        if pf.filter_name:
            print(f'2. 按姓名筛选 --> {pf.filter_name}')
        else:
            print('2. 按姓名筛选')
        print('3. 重置（清除所有筛选）')

    def _filter_list(self, title, action_name=None, pf=None):
        '''
        通用的筛选+选择人员流程
        title: 页面标题
        action_name: 操作名称，如"删除"/"修改"，None表示只查询
        pf: PersonFilter对象，为None时创建新的
        返回: 选中的人员对象，或 None（用户返回或只查询）
        '''
        try:
            if pf is None:
                pf = PersonFilter(self.service)
            while True:
                self.clear_screen()
                print(f'========={title}=========')
                current_list = pf.get_result()
                print(f'共 {len(current_list)} 条记录\n')
                for i, p in enumerate(current_list, 1):
                    print(f'{i}. {p}')
                if not current_list:
                    print('暂无符合条件的人员记录')
                self.show_filter_menu(pf)
                if action_name:
                    print(f"4. 输入序号{action_name}对应人员")
                print("输入0返回上级菜单")
                choice = self.input_with_back(input('\n请选择操作：'))
                if choice == '1':
                    keyword = self.input_with_back(input('请输入编号前缀：'))
                    pf.update_id(keyword)
                elif choice == '2':
                    keyword = self.input_with_back(input('请输入姓名前缀：'))
                    pf.update_name(keyword)
                elif choice == '3':
                    pf.reset()
                elif choice == '4' and action_name:
                    idx = self.input_with_back(input(f'请输入要{action_name}的序号：'))
                    try:
                        index = int(idx) - 1
                        if index < 0 or index >= len(current_list):
                            raise ValueError
                        return current_list[index]
                    except ValueError:
                        self.show_message('序号无效')
                else:
                    if action_name:
                        self.show_message('无效的操作编号')
        except (KeyboardInterrupt, ReturnBack):
            return None

    def delete_by_index(self, person):
        '''删除人员，返回是否成功'''
        while True:
            confirm = self.input_with_back(input(f'确认删除 {person._person_name}({person._person_id})？(y/n)：'))
            if confirm.lower() == 'y':
                if self.service.delete_person(person._person_id):
                    self.data_change()
                    self.show_message('删除成功')
                    return True
                else:
                    self.show_message('删除失败')
                    return False
            elif confirm.lower() == 'n':
                return False
            else:
                print('请输入y或n')

    def update_by_index(self, person):
        '''修改人员'''
        try:
            person_class, data = self.collector.collect(person._person_id)
        except (ReturnBack, KeyboardInterrupt):
            return
        if self.service.update_person(person._person_id, person_class(**data)):
            self.data_change()
            self.show_message('修改成功')
        else:
            self.show_message('修改失败')

    def clear_screen(self):
        '''
        清屏
        '''
        if os.name == 'nt':
            os.system('cls')  # Windows
        else:
            os.system('clear')  # Linux/Mac

    def show_menu(self):
        print('欢迎使用人员信息管理系统')
        print('1. 添加人员')
        print('2. 查询人员')
        print('3. 显示人员')
        print('4. 修改人员')
        print('5. 删除人员')
        print('6. 统计人员')
        print('7. 自动保存', "(已开启)" if self.auto_save_on else "(已关闭)")
        print('8. 手动保存')
        print('9. 读取数据')
        print('0. 退出系统')

    def add_person(self):
        try:
            print('添加人员')
            print('输入0返回上级菜单')
            while True:
                person_class, data = self.collector.collect()
                self.service.add_person(person_class(**data))
                self.data_change()
                self.clear_screen()
                print('添加成功\n')
                self.input_with_back(input('按enter继续添加人员，输入0返回：'))
        except ReturnBack:
            return
        except KeyboardInterrupt:
            return
