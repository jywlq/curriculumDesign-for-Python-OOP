# 实验员类
from src.models.base import BaseClass


class Experimenter(BaseClass):
    def __init__(self, person_id: str, person_name: str, person_gender: str, person_age: str,
                 laboratory: str, duties: str):
        '''
        实验员类：编号，姓名，性别，年龄，所在实验室，职务
        '''
        super().__init__(person_id, person_name, person_gender, person_age)
        self._laboratory = laboratory
        self._duties = duties

    @classmethod
    def get_fields(cls):
        return [("laboratory", "所在实验室"), ("duties", "职务")]

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d['personID'], d['personName'], d['personGender'], d['personAge'],
                   d['laboratory'], d['duties'])

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
