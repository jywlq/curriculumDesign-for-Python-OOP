# 教师兼行政人员类
from src.models.base import BaseClass
from src.models.teacher import Teacher
from src.models.admin import Admin


class TeacherAdmin(Teacher, Admin):
    def __init__(self, person_id: str, person_name: str, person_gender: str, person_age: str,
                 department: str, major: str, professional_title: str,
                 political_affiliation: str):
        '''
        教师兼行政人员类：编号，姓名，性别，年龄，所在系部，专业，职称，政治面貌
        '''
        BaseClass.__init__(self, person_id, person_name, person_gender, person_age)
        self._department = department
        self._major = major
        self._professional_title = professional_title
        self._political_affiliation = political_affiliation

    @classmethod
    def get_fields(cls):
        return [("department", "所在系部"), ("major", "专业"), ("professionalTitle", "职称"), ("politicalAffiliation", "政治面貌")]

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d['personID'], d['personName'], d['personGender'], d['personAge'],
                   d.get('department', ''), d['major'], d['professionalTitle'], d['politicalAffiliation'])

    def to_dict(self):
        data = Teacher.to_dict(self)
        data.update({
            '__class__': 'TeacherAdmin',
            'politicalAffiliation': self._political_affiliation
        })
        return data

    def __repr__(self):
        return f"TeacherAdmin(person_id={self._person_id}, person_name={self._person_name}, person_gender={self._person_gender}, person_age={self._person_age}, department={self._department}, major={self._major}, professional_title={self._professional_title}, political_affiliation={self._political_affiliation})"

    def __str__(self):
        return f"{self._person_name}({self._person_id})，{self._person_gender}，{self._person_age}岁，{self._department}，{self._major}，{self._professional_title}，{self._political_affiliation}"
