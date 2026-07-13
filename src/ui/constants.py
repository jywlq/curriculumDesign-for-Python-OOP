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

# 统计字典 key 常量
STAT_TOTAL = "总人数"
STAT_MALE = "男员工"
STAT_FEMALE = "女员工"
STAT_TEACHER = "教师"
STAT_EXPERIMENTER = "实验员"
STAT_ADMIN = "行政人员"
STAT_TEACHER_ADMIN = "教师兼行政人员"

# 进度条参数
BAR_BLOCK_PERCENT = 5
BAR_TOTAL_BLOCKS = 20

# 列宽常量
COL_WIDTH_SEQ = 3
COL_WIDTH_ID = 8
COL_WIDTH_NAME = 6
