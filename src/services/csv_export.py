"""
数据导出模块

支持将人员数据导出为 CSV 格式。
"""
import csv
from typing import List
from src.models import Teacher, Experimenter, Admin, TeacherAdmin


class DataExporter:
    """数据导出类，提供 CSV 导出功能"""

    @staticmethod
    def export_csv(person_list: List, filename: str = 'data/person.csv'):
        """
        将人员列表导出为 CSV 文件

        Args:
            person_list: 人员对象列表
            filename: 导出文件路径，默认 data/person.csv
        """
        headers = ['编号', '姓名', '性别', '年龄', '类型', '特有字段']

        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for p in person_list:
                ptype, extra = DataExporter._get_person_info(p)
                writer.writerow([
                    p._person_id,
                    p._person_name,
                    p._person_gender,
                    p._person_age,
                    ptype,
                    extra
                ])

    @staticmethod
    def _get_person_info(person):
        """获取人员类型和特有字段描述"""
        if isinstance(person, TeacherAdmin):
            return '教师兼行政人员', f"系部:{person._department}, 专业:{person._major}, 职称:{person._professional_title}, 政治面貌:{person._political_affiliation}"
        elif isinstance(person, Teacher):
            return '教师', f"系部:{person._department}, 专业:{person._major}, 职称:{person._professional_title}"
        elif isinstance(person, Experimenter):
            return '实验员', f"实验室:{person._laboratory}, 职务:{person._duties}"
        elif isinstance(person, Admin):
            return '行政人员', f"政治面貌:{person._political_affiliation}, 职称:{person._professional_title}"
        return '未知', ''
