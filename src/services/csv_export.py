"""
数据导出模块

支持将人员数据导出为 CSV 格式。
"""
import csv
from typing import List


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
                writer.writerow([
                    p._person_id,
                    p._person_name,
                    p._person_gender,
                    p._person_age,
                    p.type_name,
                    p.get_extra_description()
                ])
