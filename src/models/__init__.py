"""
数据模型模块 - 定义四类人员的类结构
"""
from src.models.base import BaseClass
from src.models.teacher import Teacher
from src.models.experimenter import Experimenter
from src.models.admin import Admin
from src.models.teacher_admin import TeacherAdmin

__all__ = ['BaseClass', 'Teacher', 'Experimenter', 'Admin', 'TeacherAdmin']
