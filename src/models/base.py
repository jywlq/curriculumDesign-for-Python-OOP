# 基类
class BaseClass:
    def __init__(self, person_id: str, person_name: str, person_gender: str, person_age: str):
        '''
        基类：编号，姓名，性别，年龄
        '''
        self._person_id = person_id
        self._person_name = person_name
        self._person_gender = person_gender
        self._person_age = person_age

    @classmethod
    def get_fields(cls):
        return []

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d['personID'], d['personName'], d['personGender'], d['personAge'])

    def to_dict(self):
        return {
            '__class__': 'BaseClass',
            'personID': self._person_id,
            'personName': self._person_name,
            'personGender': self._person_gender,
            'personAge': self._person_age
        }

    def __repr__(self):
        return f"BaseClass(person_id={self._person_id}, person_name={self._person_name}, person_gender={self._person_gender}, person_age={self._person_age})"

    def __str__(self):
        return f"{self._person_name}({self._person_id})，{self._person_gender}，{self._person_age}岁"
