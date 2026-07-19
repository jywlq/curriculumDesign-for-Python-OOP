"""
实验员类模块
"""
from src.models.base import BaseClass


class Experimenter(BaseClass):
    """实验员类，继承 BaseClass，新增所在实验室、职务"""

    type_name = '实验员'

    def __init__(self, person_id: str, person_name: str, person_gender: str, person_age: str,
                 laboratory: str, duties: str):
        super().__init__(person_id, person_name, person_gender, person_age)
        self._laboratory = laboratory
        self._duties = duties

    @classmethod
    def get_fields(cls):
        """返回实验员特有字段定义"""
        return [("laboratory", "所在实验室"), ("duties", "职务")]

    def get_display_fields(self, brief: bool = False) -> list:
        """返回展示字段，brief=True 时返回简要信息"""
        if brief:
            return [self._laboratory]
        return [self._laboratory, self._duties]

    def get_extra_description(self) -> str:
        return f"实验室:{self._laboratory}, 职务:{self._duties}"

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d['personID'], d['personName'], d['personGender'], str(d['personAge']),
                   d.get('laboratory', ''), d.get('duties', ''))

    def to_dict(self):
        data = super().to_dict()
        data.update({
            '__class__': 'Experimenter',
            'laboratory': self._laboratory,
            'duties': self._duties
        })
        return data

    def __repr__(self):
        return f"Experimenter(person_id={self._person_id}, person_name={self._person_name}, person_gender={self._person_gender}, person_age={self._person_age}, laboratory={self._laboratory}, duties={self._duties})"

    def __str__(self):
        return f"{self._person_name}({self._person_id})，{self._person_gender}，{self._person_age}岁，{self._laboratory}，{self._duties}"
