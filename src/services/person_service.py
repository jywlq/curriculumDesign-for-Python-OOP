"""
人员服务模块 - 核心业务逻辑层

负责人员的增删改查操作和 JSON 数据持久化。
所有 UI 层的人员操作都通过此类完成，实现了业务逻辑与界面的分离。
"""
from typing import List, Optional, Dict
from src.models import Teacher, Experimenter, Admin, TeacherAdmin
import json


class PersonService:
    """人员服务类，封装增删改查和文件读写"""

    def __init__(self):
        self.person_list = []  # 人员列表，存储所有人员对象

    def person_id_check(self, person_id: str) -> bool:
        """检查编号是否已存在"""
        for p in self.person_list:
            if p._person_id == person_id:
                return True
        return False

    def add_person(self, person) -> bool:
        """添加人员（编号校验在 UI 层完成）"""
        self.person_list.append(person)
        return True

    def find_person(self, person_id: str = '', person_name: str = '') -> List:
        """
        前缀匹配查询
        
        无参数时返回全部人员的副本，有参数时按编号/姓名前缀筛选。
        返回副本避免外部修改影响内部数据。
        """
        if not person_id and not person_name:
            return self.person_list.copy()
        result = []
        for p in self.person_list:
            if p._person_id.startswith(person_id) and p._person_name.startswith(person_name):
                result.append(p)
        return result.copy()

    def update_person(self, person_id: str, person) -> bool:
        """
        修改人员（双重检查）
        
        检查1：新编号不能与其他人员冲突
        检查2：旧编号必须存在
        """
        if self.person_id_check(person._person_id) and person_id != person._person_id:
            return False
        for i, p in enumerate(self.person_list):
            if p._person_id == person_id:
                self.person_list[i] = person
                return True
        return False

    def delete_person(self, person_id: str) -> bool:
        """按编号删除人员"""
        for p in self.person_list:
            if p._person_id == person_id:
                self.person_list.remove(p)
                return True
        return False

    def get_person_statistics(self) -> Dict[str, int]:
        """统计各类人员数量（先检查子类再检查父类，避免重复计数）"""
        res = {"教师": 0, "实验员": 0, "行政人员": 0, "教师兼行政人员": 0}
        for p in self.person_list:
            if isinstance(p, TeacherAdmin):
                res["教师兼行政人员"] += 1
            elif isinstance(p, Teacher):
                res["教师"] += 1
            elif isinstance(p, Experimenter):
                res["实验员"] += 1
            elif isinstance(p, Admin):
                res["行政人员"] += 1
        return res

    def save(self, filename: str = 'data/person.json'):
        """将人员列表序列化为 JSON 文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in self.person_list],
                      f, ensure_ascii=False, indent=4)

    def load(self, filename: str = 'data/person.json'):
        """
        从 JSON 文件加载人员数据
        
        通过 __class__ 字段和 class_map 映射还原为对应的类型对象。
        """
        # 类名到类对象的映射
        class_map = {c.__name__: c for c in [Teacher, Experimenter, Admin, TeacherAdmin]}
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
            self.person_list.clear()
            for d in data_list:
                cls = class_map.get(d.get('__class__'), Teacher)
                self.person_list.append(cls.from_dict(d))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def __str__(self):
        return ''.join([str(p) + '\n' for p in self.person_list])
