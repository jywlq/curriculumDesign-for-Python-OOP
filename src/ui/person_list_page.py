"""
人员列表页面组件

独立的 PersonListPage 组件，使用 ListView + 自定义 PersonListItem 渲染精美的可点击列表。
每行有左侧类型色条、斑马纹、hover 效果、选中高亮。
点击行可弹出 PersonDetailScreen 详情弹窗。
"""
from textual.app import ComposeResult
from textual.widgets import Static, ListItem, ListView
from textual.containers import VerticalScroll
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich import box

from src.services import PersonService
from src.ui.person_detail_page import PersonDetailScreen
from src.ui.constants import TYPE_META, COL_WIDTH_SEQ, COL_WIDTH_ID, COL_WIDTH_NAME


def _build_row_text(person, index: int) -> Text:
    """构建单行人员信息的 rich Text

    从左到右：序号 | 编号 | 姓名 | 性别年龄 | 类型标签 | 副信息
    """
    person_type = type(person).__name__
    icon, type_name, color, _, _ = TYPE_META.get(
        person_type, ("👤", "未知", "white", "", "")
    )

    # 性别图标 + 颜色
    if person._person_gender == "男":
        gender_text = f"♂ {person._person_age}岁"
        gender_style = "cyan"
    else:
        gender_text = f"♀ {person._person_age}岁"
        gender_style = "magenta"

    # 副信息（1-2 个特有字段）
    display_fields = person.get_display_fields(brief=True)
    sub_info = " · ".join(display_fields) if display_fields else ""

    # 组装
    line = Text()
    line.append(f"#{index:<{COL_WIDTH_SEQ}d} ", style="dim")                     # 序号
    line.append(f"{person._person_id:<{COL_WIDTH_ID}s} ", style="dim cyan")      # 编号
    line.append(f"{person._person_name:<{COL_WIDTH_NAME}s} ", style="bold white")  # 姓名
    line.append(f"{gender_text:<10s} ", style=gender_style)         # 性别+年龄
    line.append(f"[{type_name}]", style=f"bold {color}")            # 类型标签
    if sub_info:
        line.append(f"  {sub_info}", style="dim italic")            # 副信息

    return line


def _build_header_panel(service: PersonService) -> Panel:
    """构建顶部标题栏 Panel"""
    stat = service.get_person_statistics()

    # 统计行
    stat_text = Text()
    stat_text.append("  共 ", style="white")
    stat_text.append(f"{stat['总人数']}", style="bold gold1")
    stat_text.append(" 人    ", style="white")
    stat_text.append("👨‍🏫 ", style="cyan")
    stat_text.append(f"{stat['教师']}", style="bold cyan")
    stat_text.append(" 教师   ", style="dim")
    stat_text.append("🔬 ", style="green")
    stat_text.append(f"{stat['实验员']}", style="bold green")
    stat_text.append(" 实验员   ", style="dim")
    stat_text.append("💼 ", style="magenta")
    stat_text.append(f"{stat['行政人员']}", style="bold magenta")
    stat_text.append(" 行政   ", style="dim")
    stat_text.append("👨‍💼 ", style="yellow")
    stat_text.append(f"{stat['教师兼行政人员']}", style="bold yellow")
    stat_text.append(" 兼岗  ", style="dim")

    # 提示行
    tip_text = Text(
        "  💡 点击行或按 Enter 查看详情    ↑↓ 移动选择",
        style="dim",
    )

    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_row(Text("  📋 人员列表", style="bold gold1"))
    grid.add_row(Text(" "))
    grid.add_row(stat_text)
    grid.add_row(Text(" "))
    grid.add_row(tip_text)

    return Panel(
        grid,
        border_style="cyan",
        box=box.ROUNDED,
        padding=(0, 0),
    )


'''自定义行组件'''

class PersonListItem(ListItem):
    """人员列表行 - 绑定 person 对象，带类型色条"""

    DEFAULT_CSS = """
    PersonListItem {
        height: 3;
        padding: 0 1;
        border-left: solid transparent;
        transition: background 120ms;
    }
    PersonListItem > Static {
        width: 1fr;
        height: auto;
        content-align: left middle;
    }

    /* 斑马纹 */
    PersonListItem.--odd {
        background: $surface 50%;
    }
    PersonListItem.--even {
        background: $surface-darken-1 30%;
    }

    /* hover */
    PersonListItem:hover {
        background: $primary 15%;
    }

    /* 选中高亮 */
    PersonListItem.--highlight {
        background: $primary 35%;
        color: $text;
    }

    /* 类型色条 - 左侧竖条 */
    PersonListItem.--teacher {
        border-left: thick cyan;
    }
    PersonListItem.--experimenter {
        border-left: thick green;
    }
    PersonListItem.--admin {
        border-left: thick magenta;
    }
    PersonListItem.--teacher-admin {
        border-left: thick yellow;
    }
    """

    def __init__(self, person, index: int):
        self.person = person
        self.person_type = type(person).__name__
        self.index = index
        self.row_text = _build_row_text(person, index)
        super().__init__()

        # 添加类型 CSS 类
        _, _, _, css_class, _ = TYPE_META.get(
            self.person_type, ("", "", "", "", "")
        )
        if css_class:
            self.add_class(css_class)

        # 斑马纹
        self.add_class("--odd" if index % 2 == 1 else "--even")

    def compose(self) -> ComposeResult:
        yield Static(self.row_text)


'''主页面组件'''

class PersonListPage(VerticalScroll):
    """精美的可点击人员列表页面

    顶部：rich Panel 标题栏（含人数统计）
    中部：ListView + PersonListItem（色条/斑马纹/hover/选中）
    点击行 → 弹出 PersonDetailScreen 详情弹窗
    """

    DEFAULT_CSS = """
    PersonListPage {
        height: 100%;
        padding: 1 2;
    }

    #list-header {
        height: auto;
        margin-bottom: 1;
    }
    #list-header > Static {
        height: auto;
    }

    #person-list {
        height: 1fr;
        background: $surface;
        border: round $primary 30%;
    }
    #person-list:focus {
        background: $surface;
    }

    #empty-tip {
        height: 3;
        color: $text-muted;
        content-align: center middle;
    }
    """

    def __init__(self, service: PersonService, persons: list = None, on_select_callback=None):
        self.service = service
        self.persons = persons if persons is not None else service.person_list.copy()
        self.on_select_callback = on_select_callback
        super().__init__()

    def compose(self) -> ComposeResult:
        # 顶部标题栏
        yield Static(_build_header_panel(self.service), id="list-header")

        # 人员列表
        if not self.persons:
            # 空数据状态
            yield ListView(
                ListItem(Static("📭  暂无人员数据", id="empty-tip"), disabled=True),
                id="person-list",
            )
            return

        items = [
            PersonListItem(p, i)
            for i, p in enumerate(self.persons, 1)
        ]
        yield ListView(*items, id="person-list")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """行选中事件 - 点击或按 Enter 触发"""
        item = event.item
        if isinstance(item, PersonListItem):
            if self.on_select_callback:
                self.on_select_callback(item.person)
            else:
                self.app.push_screen(PersonDetailScreen(item.person))
