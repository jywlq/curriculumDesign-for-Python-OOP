"""
人员服务模块 - 核心业务逻辑层

负责人员的增删改查操作和 JSON 数据持久化。
所有 UI 层的人员操作都通过此类完成，实现了业务逻辑与界面的分离。
"""
from typing import List, Dict
from src.models import Teacher, Experimenter, Admin, TeacherAdmin
import json
import logging

logger = logging.getLogger(__name__)

# 统计字典 key 常量
STAT_TOTAL = "总人数"
STAT_MALE = "男员工"
STAT_FEMALE = "女员工"
STAT_TEACHER = "教师"
STAT_EXPERIMENTER = "实验员"
STAT_ADMIN = "行政人员"
STAT_TEACHER_ADMIN = "教师兼行政人员"


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

    def import_persons(self, persons: List) -> tuple:
        """
        批量导入人员（自动去重）
        
        将传入的人员列表逐个检查编号，已存在的跳过。
        Returns:
            (added, skipped): 成功添加数和跳过数
        """
        added = 0
        skipped = 0
        for p in persons:
            if not self.person_id_check(p._person_id):
                self.person_list.append(p)
                added += 1
            else:
                skipped += 1
        return added, skipped

    def find_person(self, person_id: str = '', person_name: str = '') -> List:
        """
        前缀匹配查询（交集筛选）
        
        按编号/姓名前缀取交集筛选，空字符串表示该条件不过滤（匹配所有）。
        返回副本避免外部修改影响内部数据。
        按 _person_id 去重，防止数据源有重复时返回重复条目。
        """
        result = []
        seen = set()
        for p in self.person_list:
            if (p._person_id.startswith(person_id)
                    and p._person_name.startswith(person_name)
                    and p._person_id not in seen):
                seen.add(p._person_id)
                result.append(p)
        return result

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
        person = next((p for p in self.person_list if p._person_id == person_id), None)
        if person:
            self.person_list.remove(person)
            return True
        return False

    def get_person_statistics(self) -> Dict[str, int]:
        """统计总人数、性别分布和各类人员数量"""
        # type_name 到统计 key 的映射
        type_stat_map = {
            '教师': STAT_TEACHER,
            '实验员': STAT_EXPERIMENTER,
            '行政人员': STAT_ADMIN,
            '教师兼行政人员': STAT_TEACHER_ADMIN,
        }
        res = {
            STAT_TOTAL: len(self.person_list),
            STAT_MALE: 0,
            STAT_FEMALE: 0,
            STAT_TEACHER: 0,
            STAT_EXPERIMENTER: 0,
            STAT_ADMIN: 0,
            STAT_TEACHER_ADMIN: 0
        }
        for p in self.person_list:
            # 统计性别
            if p._person_gender == "男":
                res[STAT_MALE] += 1
            else:
                res[STAT_FEMALE] += 1
            # 统计类型（通过多态 type_name 属性）
            stat_key = type_stat_map.get(p.type_name)
            if stat_key:
                res[stat_key] += 1
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
        按 person_id 去重，保留首次出现的记录，去除重复数据。
        """
        # 类名到类对象的映射
        class_map = {c.__name__: c for c in [Teacher, Experimenter, Admin, TeacherAdmin]}
        self.person_list.clear()  # 先清空，确保无论文件状态如何都从空白开始
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
            seen = set()
            for d in data_list:
                class_name = d.get('__class__', '')
                if class_name not in class_map:
                    logger.warning('未知人员类型: %s，跳过该记录', class_name)
                    continue
                cls = class_map[class_name]
                person = cls.from_dict(d)
                if person._person_id not in seen:
                    seen.add(person._person_id)
                    self.person_list.append(person)
        except FileNotFoundError:
            pass  # 文件不存在（首次运行），列表保持空
        except json.JSONDecodeError:
            logger.warning('数据文件 %s 格式错误，已清空人员列表', filename)

    def __str__(self):
        return ''.join([str(p) + '\n' for p in self.person_list])
