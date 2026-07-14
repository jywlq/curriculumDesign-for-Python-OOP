"""
人员信息收集器模块

封装用户输入收集逻辑，根据人员类型动态收集对应字段。
使用多态：调用 person_class.get_fields() 获取不同类型人员的特有字段。
"""
from src.models import Teacher, Experimenter, Admin, TeacherAdmin
from src.ui.exceptions import ReturnBack
from src.ui.constants import ID_PATTERN


class PersonCollector:
    """人员信息收集器：处理类型选择和字段输入"""

    # 类型选择映射：支持序号和中文名称两种输入方式
    PERSON_TYPE = {
        "1": Teacher,
        "2": Experimenter,
        "3": Admin,
        "4": TeacherAdmin,
        "老师": Teacher,
        "实验员": Experimenter,
        "行政人员": Admin,
        "老师兼行政人员": TeacherAdmin
    }

    def __init__(self, service):
        self.service = service

    def select_type(self):
        """选择人员类型，返回对应的类对象"""
        while True:
            person_type = input("请输入人员类型或序号(1.老师/2.实验员/3.行政人员/4.老师兼行政人员)：")
            if person_type == '0':
                raise ReturnBack()
            if not person_type.strip():
                print('输入不能为空')
                continue
            person_class = self.PERSON_TYPE.get(person_type)
            if not person_class:
                print('无效的人员类型，请重新输入')
                continue
            return person_class

    def collect_base_info(self, old_id: str = ''):
        """收集 BaseClass 的四个公共字段（编号/姓名/性别/年龄）"""
        # 编号验证：格式为 类型前缀 + 三位数字，如 T001、E001、A001、TA001
        while True:
            id = input("请输入编号（格式：T/E/A/TA + 三位数字，如 T001）：")
            if id == '0':
                raise ReturnBack()
            if not id.strip():
                print('输入不能为空')
                continue
            if not id.isascii() or not id.isalnum():
                print('编号只能包含字母和数字，请重新输入')
                continue
            if not ID_PATTERN.match(id):
                print('编号格式错误，应为 T/E/A/TA + 三位数字（如 T001）')
                continue
            if id != old_id and self.service.person_id_check(id):
                print('编号已存在，请重新输入')
                continue
            break
        # 姓名验证：长度 2-20 字符
        while True:
            name = input("请输入姓名（2-20个字符）：")
            if name == '0':
                raise ReturnBack()
            if not name.strip():
                print('输入不能为空')
                continue
            if len(name.strip()) < 2 or len(name.strip()) > 20:
                print('姓名长度必须在 2-20 个字符之间')
                continue
            break
        while True:
            gender = input("请输入性别：")
            if gender == '0':
                raise ReturnBack()
            if not gender.strip():
                print('输入不能为空')
                continue
            if gender not in ('男', '女'):
                print('性别只能是男或女，请重新输入')
                continue
            break
        # 年龄验证：整数，范围 1-150
        while True:
            age_str = input("请输入年龄（1-150之间的整数）：")
            if age_str == '0':
                raise ReturnBack()
            if not age_str.strip():
                print('输入不能为空')
                continue
            try:
                age = int(age_str)
                if 1 <= age <= 150:
                    break
                else:
                    print("年龄必须在 1-150 之间")
            except ValueError:
                print("年龄必须是一个整数")
        return {"personID": id, "personName": name, "personGender": gender, "personAge": age}

    def collect_extra_fields(self, person_class):
        """
        收集子类特有字段
        
        通过 get_fields() 动态获取字段定义，实现多态。
        不同类型人员调用各自的 get_fields() 返回不同的字段列表。
        """
        data = {}
        for field, prompt in person_class.get_fields():
            while True:
                value = input(f"请输入{prompt}：")
                if value == '0':
                    raise ReturnBack()
                if not value.strip():
                    print('输入不能为空')
                    continue
                data[field] = value
                break
        return data

    def collect(self, old_id: str = ''):
        """收集完整人员信息，返回 (类型类, 数据字典) 元组"""
        person_class = self.select_type()
        data = self.collect_base_info(old_id)
        data.update(self.collect_extra_fields(person_class))
        return person_class, data
