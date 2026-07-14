"""
行政人员类模块
"""
from src.models.base import BaseClass


class Admin(BaseClass):
    """行政人员类，继承 BaseClass，新增政治面貌、职称"""

    def __init__(self, person_id: str, person_name: str, person_gender: str, person_age: str,
                 political_affiliation: str, professional_title: str):
        super().__init__(person_id, person_name, person_gender, person_age)
        self._political_affiliation = political_affiliation
        self._professional_title = professional_title

    @classmethod
    def get_fields(cls):
        """返回行政人员特有字段定义"""
        return [("politicalAffiliation", "政治面貌"), ("professionalTitle", "职称")]

    def get_display_fields(self, brief: bool = False) -> list:
        """返回展示字段，brief=True 时返回简要信息"""
        if brief:
            return [self._professional_title]
        return [self._political_affiliation, self._professional_title]

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d['personID'], d['personName'], d['personGender'], d['personAge'],
                   d.get('politicalAffiliation', ''), d.get('professionalTitle', ''))

    def to_dict(self):
        data = super().to_dict()
        data.update({
            '__class__': 'Admin',
            'politicalAffiliation': self._political_affiliation,
            'professionalTitle': self._professional_title
        })
        return data

    def __repr__(self):
        return f"Admin(person_id={self._person_id}, person_name={self._person_name}, person_gender={self._person_gender}, person_age={self._person_age}, political_affiliation={self._political_affiliation}, professional_title={self._professional_title})"

    def __str__(self):
        return f"{self._person_name}({self._person_id})，{self._person_gender}，{self._person_age}岁，{self._political_affiliation}，{self._professional_title}"
