"""
人员列表页面组件

独立的 PersonListPage 组件，使用 DataTable 渲染可点击的人员列表。
点击行可弹出详情页，后续删查改功能可复用此模块。
"""
from textual.app import ComposeResult
from textual.widgets import Static, DataTable
from textual.containers import VerticalScroll

from src.services import PersonService
from src.ui.person_detail_page import PersonDetailScreen


class PersonListPage(VerticalScroll):
    """可点击的人员列表页面"""

    DEFAULT_CSS = """
    PersonListPage {
        height: 100%;
        padding: 1 2;
    }
    PersonListPage > Static {
        height: auto;
    }
    PersonListPage > #person-table {
        height: 1fr;
        border: round $secondary;
    }
    """

    def __init__(self, service: PersonService):
        self.service = service
        self.persons = service.person_list.copy()
        super().__init__()

    def compose(self) -> ComposeResult:
        type_map = {
            "Teacher": "教师",
            "Experimenter": "实验员",
            "Admin": "行政人员",
            "TeacherAdmin": "教师兼行政",
        }

        yield Static(f"📋 所有人员列表（共 {len(self.persons)} 人）  |  点击行查看详情")

        table = DataTable(id="person-table", cursor_type="row")
        table.add_columns("序号", "编号", "姓名", "性别", "年龄", "类型")

        for i, p in enumerate(self.persons, 1):
            type_name = type_map.get(p.__class__.__name__, p.__class__.__name__)
            gender_icon = "♂" if p._person_gender == "男" else "♀"
            table.add_row(
                str(i),
                p._person_id,
                p._person_name,
                f"{gender_icon} {p._person_gender}",
                str(p._person_age),
                type_name,
            )

        yield table

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """点击行查看详情"""
        if event.cursor_row is not None and 0 <= event.cursor_row < len(self.persons):
            person = self.persons[event.cursor_row]
            self.app.push_screen(PersonDetailScreen(person))
