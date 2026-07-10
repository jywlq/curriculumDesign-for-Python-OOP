# 业务逻辑类（增删改查、文件读写）
from src.models import Teacher, Experimenter, Admin, TeacherAdmin
import json


class PersonService:
    def __init__(self):
        self.person_list = []

    def person_id_check(self, person_id: str):
        '''
        检查编号是否存在
        '''
        for p in self.person_list:
            if p._person_id == person_id:
                return True
        return False

    def add_person(self, person):
        '''
        按类添加
        '''
        # 此处ID check在ui层实现
        self.person_list.append(person)
        return True

    def find_person(self, person_id: str = '', person_name: str = ''):
        '''
        前缀查询
        '''
        if not person_id and not person_name:
            return self.person_list.copy()
        result = []
        for p in self.person_list:
            if p._person_id.startswith(person_id) and p._person_name.startswith(person_name):
                result.append(p)
        return result.copy()

    def update_person(self, person_id: str, person):
        '''
        双重检查，防止编号冲突并允许修改自身
        '''
        if self.person_id_check(person._person_id) and person_id != person._person_id:
            return False
        for i, p in enumerate(self.person_list):
            if p._person_id == person_id:
                self.person_list[i] = person
                return True
        return False

    def delete_person(self, person_id: str):
        '''
        删除人员
        '''
        for p in self.person_list:
            if p._person_id == person_id:
                self.person_list.remove(p)
                return True
        return False

    def get_person_statistics(self):
        '''
        统计各类人数，先检查子类再检查父类避免重复计数
        '''
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
        '''
        由调用方决定何时保存，main层调用
        '''
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in self.person_list],
                      f, ensure_ascii=False, indent=4)

    def load(self, filename: str = 'data/person.json'):
        '''
        调用方决定何时加载，main层调用
        '''
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
