"""
教师兼行政人员类模块

演示多重继承：同时继承 Teacher 和 Admin，合并两者特有字段。
"""
from src.models.base import BaseClass
from src.models.teacher import Teacher
from src.models.admin import Admin


class TeacherAdmin(Teacher, Admin):
    """
    教师兼行政人员类（多重继承）
    
    同时拥有教师（系部、专业、职称）和行政人员（政治面貌）的属性。
    构造函数直接调用 BaseClass.__init__() 而非 super()，绕开 MRO 问题。
    """

    def __init__(self, person_id: str, person_name: str, person_gender: str, person_age: str,
                 department: str, major: str, professional_title: str,
                 political_affiliation: str):
        # 直接调用基类构造函数，避免多重继承的 MRO 问题
        BaseClass.__init__(self, person_id, person_name, person_gender, person_age)
        self._department = department
        self._major = major
        self._professional_title = professional_title
        self._political_affiliation = political_affiliation

    @classmethod
    def get_fields(cls):
        return [("department", "所在系部"), ("major", "专业"), ("professionalTitle", "职称"), ("politicalAffiliation", "政治面貌")]

    def get_display_fields(self, brief: bool = False) -> list:
        """返回用于展示的特有字段值"""
        if brief:
            return [self._department, self._political_affiliation]
        return [self._department, self._major, self._professional_title, self._political_affiliation]

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d['personID'], d['personName'], d['personGender'], d['personAge'],
                   d.get('department', ''), d.get('major', ''), d.get('professionalTitle', ''), d.get('politicalAffiliation', ''))

    def to_dict(self):
        data = BaseClass.to_dict(self)
        data.update({
            '__class__': 'TeacherAdmin',
            'politicalAffiliation': self._political_affiliation
        })
        return data

    def __repr__(self):
        return f"TeacherAdmin(person_id={self._person_id}, person_name={self._person_name}, person_gender={self._person_gender}, person_age={self._person_age}, department={self._department}, major={self._major}, professional_title={self._professional_title}, political_affiliation={self._political_affiliation})"

    def __str__(self):
        return f"{self._person_name}({self._person_id})，{self._person_gender}，{self._person_age}岁，{self._department}，{self._major}，{self._professional_title}，{self._political_affiliation}"
