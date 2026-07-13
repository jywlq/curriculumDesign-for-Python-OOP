"""
人员信息基类模块

定义所有人员类型的公共字段和序列化方法，是整个数据模型的根基。
子类继承此类获得基础属性，并通过覆写 get_fields() 返回各自特有字段。
"""
from typing import List, Tuple, Dict, Type


class BaseClass:
    """
    人员信息基类
    
    封装人员的四个公共属性：编号、姓名、性别、年龄。
    提供 to_dict() / from_dict() 实现 JSON 持久化，
    get_fields() 作为钩子方法由子类覆写，实现多态。
    """

    def __init__(self, person_id: str, person_name: str, person_gender: str, person_age: str):
        self._person_id = person_id
        self._person_name = person_name
        self._person_gender = person_gender
        self._person_age = person_age

    @classmethod
    def get_fields(cls) -> List[Tuple[str, str]]:
        """返回子类特有字段列表，基类返回空列表（模板方法）"""
        return []

    def get_display_fields(self, brief: bool = False) -> list:
        """返回用于展示的特有字段值列表

        brief=True: 返回 1-2 个关键字段（用于列表行）
        brief=False: 返回全部特有字段（用于详情页）
        """
        return []

    @classmethod
    def from_dict(cls, d: dict) -> 'BaseClass':
        """从字典反序列化"""
        return cls(d['personID'], d['personName'], d['personGender'], d['personAge'])

    def to_dict(self) -> dict:
        """序列化为字典，__class__ 字段用于反序列化时还原类型"""
        return {
            '__class__': 'BaseClass',
            'personID': self._person_id,
            'personName': self._person_name,
            'personGender': self._person_gender,
            'personAge': self._person_age
        }

    def __repr__(self) -> str:
        return f"BaseClass(person_id={self._person_id}, person_name={self._person_name}, person_gender={self._person_gender}, person_age={self._person_age})"

    def __str__(self) -> str:
        return f"{self._person_name}({self._person_id})，{self._person_gender}，{self._person_age}岁"
