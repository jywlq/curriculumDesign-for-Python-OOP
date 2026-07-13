"""
人员筛选页面组件

通用筛选页面，支持查询/修改/删除三种模式。
复用 PersonFilter 类进行筛选，复用 PersonListPage 显示列表。
"""
from textual.app import ComposeResult
from textual.widgets import Static, Button, Input, ListView, ListItem
from textual.containers import VerticalScroll, Horizontal, Vertical

from src.services import PersonService
from src.ui.filter import PersonFilter
from src.ui.person_list_page import PersonListPage, PersonListItem
from src.ui.person_detail_page import PersonDetailScreen
from src.ui.person_edit_screen import PersonEditScreen
from src.ui.person_delete_confirm import PersonDeleteConfirmScreen


class PersonFilterPage(VerticalScroll):
    """通用筛选页面，支持查询/修改/删除三种模式

    顶部：筛选输入区（编号/姓名输入框 + 筛选/重置按钮）
    中部：人员列表（复用 PersonListPage）
    点击行：根据 action_name 决定行为（查看详情/修改/删除确认）
    """

    DEFAULT_CSS = """
    PersonFilterPage {
        height: 100%;
        padding: 1 2;
    }

    #filter-bar {
        height: auto;
        margin-bottom: 1;
        padding: 1 0;
    }
    #filter-bar > Input {
        width: 1fr;
        margin-right: 1;
    }
    #filter-bar > Button {
        width: auto;
        min-width: 10;
        margin-left: 1;
    }

    #filter-list-container {
        height: 1fr;
    }
    #filter-list-container > Static {
        height: auto;
    }
    """

    def __init__(self, service: PersonService, action_name: str = "查询"):
        self.service = service
        self.action_name = action_name
        self.person_filter = PersonFilter(service)
        self.current_list = self.person_filter.get_result()
        super().__init__()

    def compose(self) -> ComposeResult:
        # 顶部：筛选区
        with Horizontal(id="filter-bar"):
            yield Input(placeholder="编号前缀", id="filter-id")
            yield Input(placeholder="姓名前缀", id="filter-name")
            yield Button("筛选", variant="primary", id="btn-filter")
            yield Button("重置", variant="default", id="btn-reset")

        # 中部：列表区（复用 PersonListPage，传入回调）
        with Vertical(id="filter-list-container"):
            yield PersonListPage(
                self.service,
                self.current_list,
                on_select_callback=self._on_person_selected
            )

    def _refresh_list(self) -> None:
        """刷新列表显示"""
        self.current_list = self.person_filter.get_result()
        container = self.query_one("#filter-list-container", Vertical)
        container.remove_children()
        container.mount(PersonListPage(
            self.service,
            self.current_list,
            on_select_callback=self._on_person_selected
        ))

    def _do_filter(self) -> None:
        """执行筛选"""
        filter_id = self.query_one("#filter-id", Input).value.strip()
        filter_name = self.query_one("#filter-name", Input).value.strip()
        self.person_filter.update_id(filter_id)
        self.person_filter.update_name(filter_name)
        self._refresh_list()

    def _on_person_selected(self, person) -> None:
        """行选中回调 - 根据 action_name 决定行为"""
        if self.action_name == "查询":
            self.app.push_screen(PersonDetailScreen(person))
        elif self.action_name == "修改":
            self.app.push_screen(PersonEditScreen(person, self.service, on_done=self._refresh_list))
        elif self.action_name == "删除":
            self.app.push_screen(PersonDeleteConfirmScreen(person, self.service, on_done=self._refresh_list))

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """输入框按 Enter 触发筛选"""
        self._do_filter()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮点击事件"""
        if event.button.id == "btn-filter":
            self._do_filter()
        elif event.button.id == "btn-reset":
            self.person_filter.reset()
            self.query_one("#filter-id", Input).value = ""
            self.query_one("#filter-name", Input).value = ""
            self._refresh_list()
