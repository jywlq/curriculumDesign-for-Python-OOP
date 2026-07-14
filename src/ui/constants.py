"""
UI 层公共常量

统一管理人员类型元数据、统计字典 key、进度条参数等，
消除各文件中的重复定义和魔法数字。
"""


# 人员类型元数据：(图标, 中文名, 主题色, CSS 类名, 统计字典 key)
TYPE_META = {
    "Teacher":      ("👨‍🏫", "教师",       "cyan",    "--teacher",       "教师"),
    "Experimenter": ("🔬", "实验员",     "green",   "--experimenter",  "实验员"),
    "Admin":        ("💼", "行政人员",   "magenta", "--admin",         "行政人员"),
    "TeacherAdmin": ("👨‍💼", "教师兼行政", "yellow",  "--teacher-admin", "教师兼行政人员"),
}

# 统计字典 key 常量（从 service 层导入，供 UI 层使用）
from src.services.person_service import (
    STAT_TOTAL, STAT_MALE, STAT_FEMALE,
    STAT_TEACHER, STAT_EXPERIMENTER, STAT_ADMIN, STAT_TEACHER_ADMIN,
)

# 进度条参数
BAR_BLOCK_PERCENT = 5
BAR_TOTAL_BLOCKS = 20

# 列宽常量
COL_WIDTH_SEQ = 3
COL_WIDTH_ID = 8
COL_WIDTH_NAME = 6

import re
from src.models import Teacher, Experimenter, Admin, TeacherAdmin

# 编号格式规则：类型前缀 + 三位数字
ID_PATTERN = re.compile(r'^(T|E|A|TA)\d{3}$')

# 类名到类对象的映射
CLASS_MAP = {
    "Teacher": Teacher,
    "Experimenter": Experimenter,
    "Admin": Admin,
    "TeacherAdmin": TeacherAdmin,
}

def camel_to_snake(name: str) -> str:
    """驼峰命名转下划线命名"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
