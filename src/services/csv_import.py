"""
数据导入模块

支持从 CSV 文件批量导入人员数据。
与导出模块配套，支持导入导出格式的 CSV 文件。
"""
import csv
from typing import List, Tuple
from src.models import Teacher, Experimenter, Admin, TeacherAdmin


class DataImporter:
    """数据导入类，提供 CSV 导入功能"""

    # 类型名称到类对象的映射
    TYPE_MAP = {
        '教师': Teacher,
        '实验员': Experimenter,
        '行政人员': Admin,
        '教师兼行政人员': TeacherAdmin,
    }

    # 中文字段名到英文字段名的映射
    FIELD_MAP = {
        '系部': 'department',
        '专业': 'major',
        '职称': 'professionalTitle',
        '政治面貌': 'politicalAffiliation',
        '实验室': 'laboratory',
        '职务': 'duties',
    }

    @staticmethod
    def import_csv(filename: str = 'data/person.csv') -> Tuple[List, int]:
        """
        从 CSV 文件导入人员数据

        Args:
            filename: CSV 文件路径

        Returns:
            (人员对象列表, 跳过数量)
        """
        persons = []
        skipped = 0

        with open(filename, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            header = next(reader)  # 跳过表头

            for row in reader:
                try:
                    person = DataImporter._parse_row(row)
                    if person:
                        persons.append(person)
                    else:
                        skipped += 1
                except Exception:
                    skipped += 1  # 解析失败跳过

        return persons, skipped

    @staticmethod
    def _parse_row(row):
        """解析 CSV 行为人员对象"""
        if len(row) < 6:
            return None

        # 前5列是固定字段，第6列及之后合并为特有字段字符串
        person_id = row[0]
        name = row[1]
        gender = row[2]
        age = row[3]
        ptype = row[4]
        # 合并第6列及之后的所有内容（CSV中逗号分隔的特有字段）
        extra = ','.join(row[5:])

        # 获取对应的类
        person_class = DataImporter.TYPE_MAP.get(ptype)
        if not person_class:
            return None

        # 解析特有字段
        extra_dict = DataImporter._parse_extra_fields(extra)

        # 构造完整数据
        data = {
            'personID': person_id,
            'personName': name,
            'personGender': gender,
            'personAge': int(age),
            **extra_dict
        }

        return person_class.from_dict(data)

    @staticmethod
    def _parse_extra_fields(extra_str):
        """解析特有字段字符串为字典"""
        result = {}
        if not extra_str.strip():
            return result

        # 格式：系部:计算机系, 专业:软件工程, 职称:副教授
        for item in extra_str.split(', '):
            if ':' in item:
                key, value = item.split(':', 1)
                # 将中文字段名映射为英文
                eng_key = DataImporter.FIELD_MAP.get(key, key)
                result[eng_key] = value

        return result
