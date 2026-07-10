# 教师类
from src.models.base import BaseClass


class Teacher(BaseClass):
    def __init__(self, person_id: str, person_name: str, person_gender: str, person_age: str,
                 department: str, major: str, professional_title: str):
        '''
        教师类：编号，姓名，性别，年龄,所在系部，专业，职称
        '''
        super().__init__(person_id, person_name, person_gender, person_age)
        self._department = department
        self._major = major
        self._professional_title = professional_title

    @classmethod
    def get_fields(cls):
        return [("department", "所在系部"), ("major", "专业"), ("professionalTitle", "职称")]

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d['personID'], d['personName'], d['personGender'], d['personAge'],
                   d.get('department', ''), d['major'], d['professionalTitle'])

    def to_dict(self):
        data = super().to_dict()
        data.update({
            '__class__': 'Teacher',
            'department': self._department,
            'major': self._major,
            'professionalTitle': self._professional_title
        })
        return data

    def __repr__(self):
        return f"Teacher(person_id={self._person_id}, person_name={self._person_name}, person_gender={self._person_gender}, person_age={self._person_age}, department={self._department}, major={self._major}, professional_title={self._professional_title})"

    def __str__(self):
        return f"{self._person_name}({self._person_id})，{self._person_gender}，{self._person_age}岁，{self._department}，{self._major}，{self._professional_title}"
