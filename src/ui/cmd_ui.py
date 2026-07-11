"""
命令行交互界面模块

负责菜单显示、用户输入处理和界面控制。
使用异常机制实现"输入 0 返回上级菜单"，复用 _filter_list 方法减少代码重复。
"""
import os
import json
from src.services import PersonService
from src.services.csv_export import DataExporter
from src.services.csv_import import DataImporter
from src.ui.exceptions import ReturnBack
from src.ui.filter import PersonFilter
from src.ui.collector import PersonCollector


class CmdUI:
    """命令行用户界面主类"""

    CONFIG_FILE = 'data/config.json'

    def __init__(self):
        self.service = PersonService()
        self.collector = PersonCollector(self.service)
        self.auto_save_on = False
        self.load_config()
        # 菜单编号到方法的映射
        self.MENU = {
            "1": self.add_person,
            "2": self.find_person,
            "3": self.show_all_person,
            "4": self.update_person,
            "5": self.delete_person,
            "6": self.get_person_statistics,
            "7": self.auto_save,
            "8": self.manual_save,
            "9": self.manual_load,
            "10": self.export_csv,
            "11": self.import_csv,
        }

    def save(self):
        self.service.save()

    def load_data(self):
        self.service.load()

    def manual_save(self):
        """手动保存：执行保存后提示用户"""
        self.save()
        self.show_message('保存成功')

    def manual_load(self):
        """手动读取：执行读取后提示用户"""
        self.load_data()
        self.show_message('读取成功')

    def export_csv(self):
        """导出人员数据为 CSV 文件"""
        try:
            DataExporter.export_csv(self.service.person_list)
            self.show_message('导出成功，文件保存在 data/person.csv')
        except Exception as e:
            self.show_message(f'导出失败：{e}')

    def import_csv(self):
        """导入CSV数据"""
        while True:
            try:
                self.clear_screen()
                print('===== CSV数据导入 =====')
                print()
                print('请将CSV文件放入 data/import/ 目录')
                print('文件需包含表头：编号,姓名,性别,年龄,类型,特有字段')
                print('注意：请勿重复导入，表头逗号为英文逗号')
                print()
                filename = input('请输入文件名（如 test.csv）：')
                if filename == '0':
                    return
                filepath = f'data/import/{filename}'
                persons, skipped = DataImporter.import_csv(filepath)
                # 过滤编号重复的
                added = 0
                for p in persons:
                    if not self.service.person_id_check(p._person_id):
                        self.service.add_person(p)
                        added += 1
                    else:
                        skipped += 1
                self.data_change()
                msg = f'导入完成：成功 {added} 条'
                if skipped > 0:
                    msg += f'，跳过 {skipped} 条（重复或格式错误）'
                self.show_message(msg)
                return  # 成功后返回主菜单
            except FileNotFoundError:
                self.show_message(f'未找到文件：{filepath}')
            except Exception as e:
                self.show_message(f'导入失败：{e}')
            except KeyboardInterrupt:
                return

    def load_config(self):
        """从 config.json 加载自动保存开关状态"""
        try:
            with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.auto_save_on = config.get('autoSaveOn', False)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_config(self):
        """将自动保存开关状态持久化到 config.json"""
        with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({'autoSaveOn': self.auto_save_on}, f, ensure_ascii=False, indent=4)

    def save_if_auto(self):
        """自动保存：如果开启则保存，否则不操作"""
        if self.auto_save_on:
            self.save()

    def data_change(self):
        """数据变更后的统一操作入口"""
        self.save_if_auto()

    def run(self):
        """主循环：显示菜单 → 接收输入 → 分发到对应方法"""
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
        """人员查询：复用筛选逻辑"""
        self._filter_list('人员查询')

    def show_all_person(self):
        """显示所有人员记录"""
        try:
            self.clear_screen()
            print("=========所有人员列表如下=========")
            for p in self.service.person_list:
                print(p)
            self.input_with_back(input("按enter返回上级菜单"))
        except KeyboardInterrupt:
            return

    def update_person(self):
        """修改人员：筛选后输入序号修改"""
        person = self._filter_list('修改人员', '修改')
        if person:
            self.update_by_index(person)

    def delete_person(self):
        """删除人员：筛选后输入序号删除"""
        pf = PersonFilter(self.service)
        while True:
            person = self._filter_list('删除人员', '删除', pf)
            if not person:
                return
            self.delete_by_index(person)

    def get_person_statistics(self):
        """显示人员统计信息"""
        stat = self.service.get_person_statistics()
        self.clear_screen()
        # 表格格式显示统计信息
        print('╔══════════════════════════╗')
        print('║       人员统计           ║')
        print('╠══════════════════════════╣')
        print('║  【总览】                ║')
        print(f'║  总人数：{stat["总人数"]:<17}║')
        print(f'║  男员工：{stat["男员工"]:<17}║')
        print(f'║  女员工：{stat["女员工"]:<17}║')
        print('╠══════════════════════════╣')
        print('║  【按类型】              ║')
        print(f'║  教师：    {stat["教师"]:<17}║')
        print(f'║  实验员：  {stat["实验员"]:<17}║')
        print(f'║  行政人员：{stat["行政人员"]:<15}║')
        print(f'║  教师兼行政：{stat["教师兼行政人员"]:<13}║')
        print('╚══════════════════════════╝')
        self.input_with_back(input('\n按enter返回上级菜单'))

    def auto_save(self):
        """切换自动保存开关"""
        self.auto_save_on = not self.auto_save_on
        self.save_config()
        if self.auto_save_on:
            self.show_message('自动保存已开启')
        else:
            self.show_message('自动保存已关闭')

    def input_with_back(self, value: str):
        """输入包装：输入 0 时抛出 ReturnBack 异常实现返回"""
        if value == '0':
            raise ReturnBack()
        return value

    def is_empty(self, value: str):
        """判空：为空返回 True 并打印提示"""
        if not value.strip():
            print('输入不能为空')
            return True
        return False

    def show_message(self, msg):
        """清屏 → 显示消息 → 按 enter 继续"""
        self.clear_screen()
        print(msg)
        self.input_with_back(input('按enter继续'))

    def show_filter_menu(self, pf):
        """显示筛选菜单（当前筛选状态）"""
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
        """
        通用的筛选 + 选择人员流程
        
        查询、修改、删除三个功能共用此方法，减少代码重复。
        - 查询：action_name=None，只展示筛选结果
        - 修改/删除：action_name="修改"/"删除"，支持选择具体人员
        
        Returns:
            选中的人员对象，或 None（用户返回/只查询）
        """
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
                    self.show_message('无效的操作编号')
        except (KeyboardInterrupt, ReturnBack):
            return None

    def delete_by_index(self, person):
        """删除确认：y 确认删除，n 取消"""
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
        """执行修改操作"""
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
        """跨平台清屏"""
        if os.name == 'nt':
            os.system('cls')  # Windows
        else:
            os.system('clear')  # Linux/Mac

    def show_menu(self):
        """显示主菜单"""
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
        print('10. 导出CSV')
        print('11. 导入CSV')
        print('0. 退出系统')

    def add_person(self):
        """添加人员：支持连续添加"""
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
