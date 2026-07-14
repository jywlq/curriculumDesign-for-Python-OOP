"""
TUI 界面模块 - 基于 Textual 的终端用户界面

使用 rich + textual 实现类 GUI 体验，支持鼠标点击和键盘操作。
左右布局：左侧导航菜单（带图标分组），右侧内容区（带统计卡片）。
"""
from textual.app import App, ComposeResult
from textual.widgets import (
    Footer, Static, ListItem, ListView, Label, Button, DataTable
)
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual import events
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich import box

from src.services import PersonService
from src.services.config import load_auto_save, save_auto_save
from src.ui.tui.person_list_page import PersonListPage
from src.ui.tui.person_filter_page import PersonFilterPage
from src.ui.constants import (
    TYPE_META, STAT_TOTAL, STAT_MALE, STAT_FEMALE,
    STAT_TEACHER, STAT_EXPERIMENTER, STAT_ADMIN, STAT_TEACHER_ADMIN,
    BAR_BLOCK_PERCENT, BAR_TOTAL_BLOCKS,
)
from src.ui.tui.widgets import RichPanelPage
from src.services.csv_export import DataExporter
from src.services.csv_import import DataImporter
from src.ui.tui.person_add_screen import PersonAddScreen
from src.ui.tui.csv_import_screen import CsvImportScreen



# 菜单项配置：(图标, 名称, 分组)
MENU_ITEMS = [                      #菜单栏映射
    # 人员管理
    ("➕", "添加人员", "人员管理"),
    ("🔍", "查询人员", "人员管理"),
    ("📋", "显示人员", "人员管理"),
    ("✏️ ", "修改人员", "人员管理"),
    ("🗑️ ", "删除人员", "人员管理"),
    ("📊", "统计人员", "人员管理"),
    # 数据操作
    ("💾", "手动保存", "数据操作"),
    ("📂", "读取数据", "数据操作"),
    ("📤", "导出 CSV", "数据操作"),
    ("📥", "导入 CSV", "数据操作"),
]

MENU_GROUPS = ["人员管理", "数据操作"]


# ── 辅助函数 ──

def render_welcome_page(service: PersonService, auto_save: bool) -> Panel:
    """渲染欢迎页面板"""
    stat = service.get_person_statistics()

    # 构建统计表格
    table = Table(
        show_header=False,
        expand=True,
        box=box.SIMPLE_HEAVY,
        padding=(0, 2),
    )
    table.add_column("label", justify="right", style="bold cyan")
    table.add_column("value", justify="left", style="bold white")

    table.add_row("👥 总人数", f"{stat[STAT_TOTAL]} 人")
    table.add_row("👨 男员工", f"{stat[STAT_MALE]} 人")
    table.add_row("👩 女员工", f"{stat[STAT_FEMALE]} 人")
    table.add_row("───", "───")
    table.add_row("👨‍🏫 教师", f"{stat[STAT_TEACHER]} 人")
    table.add_row("🔬 实验员", f"{stat[STAT_EXPERIMENTER]} 人")
    table.add_row("💼 行政人员", f"{stat[STAT_ADMIN]} 人")
    table.add_row("👨‍💼 教师兼行政", f"{stat[STAT_TEACHER_ADMIN]} 人")

    # 构建主面板
    content = Table.grid(expand=True)
    content.add_column(justify="center")

    title_text = Text("\n✨ 欢迎使用人员信息管理系统 ✨\n", style="bold gold1")
    subtitle_text = Text("TUI版界面\n\n25计科(创)李鑫杰\n\n", style="italic dim")
    content.add_row(title_text)
    content.add_row(subtitle_text)

    # 统计卡片区域
    stat_panel = Panel(
        table,
        title="📊 数据概览",
        border_style="cyan",
        padding=(1, 2),
    )
    content.add_row(stat_panel)

    # 提示信息
    status_text = Text(
        f"\n💡 右上角开关自动保存功能    "
        f"📌 从左侧菜单选择功能开始使用\n",
        style="dim"
    )
    content.add_row(status_text)

    return Panel(
        content,
        border_style="blue",
        padding=(1, 3),
    )


def render_statistics_page(service: PersonService) -> Panel:
    """渲染统计人员页面,统计卡片"""
    stat = service.get_person_statistics()

    # 总览卡片（横向排列的统计数字）
    overview_grid = Table.grid(expand=True)
    overview_grid.add_column(justify="center", ratio=1)
    overview_grid.add_column(justify="center", ratio=1)
    overview_grid.add_column(justify="center", ratio=1)

    overview_grid.add_row(
        Panel(
            Text(f"\n👥 总人数\n\n", style="bold white") + Text(f"    {stat[STAT_TOTAL]}    \n", style="bold gold1 size 10"),
            border_style="blue",
            padding=(1, 1),
        ),
        Panel(
            Text(f"\n👨 男员工\n\n", style="bold white") + Text(f"    {stat[STAT_MALE]}    \n", style="bold cyan"),
            border_style="cyan",
            padding=(1, 1),
        ),
        Panel(
            Text(f"\n👩 女员工\n\n", style="bold white") + Text(f"    {stat[STAT_FEMALE]}    \n", style="bold magenta"),
            border_style="magenta",
            padding=(1, 1),
        ),
    )

    # 按类型统计表格
    type_table = Table(
        title="📋 按人员类型统计",
        expand=True,
        box=box.ROUNDED,
        padding=(0, 2),
        header_style="bold yellow",
        border_style="yellow",
    )
    type_table.add_column("人员类型", style="bold", justify="left")
    type_table.add_column("人数", justify="right")
    type_table.add_column("占比", justify="right")

    total = stat[STAT_TOTAL] if stat[STAT_TOTAL] > 0 else 1
    type_data = [
        ("👨‍🏫 教师", stat[STAT_TEACHER], "cyan"),
        ("🔬 实验员", stat[STAT_EXPERIMENTER], "green"),
        ("💼 行政人员", stat[STAT_ADMIN], "magenta"),
        ("👨‍💼 教师兼行政", stat[STAT_TEACHER_ADMIN], "yellow"),
    ]
    for name, count, color in type_data:
        pct = count / total * 100
        bar = "█" * int(pct / BAR_BLOCK_PERCENT) + "░" * (BAR_TOTAL_BLOCKS - int(pct / BAR_BLOCK_PERCENT))
        type_table.add_row(
            f"[{color}]{name}[/{color}]",
            f"[bold]{count} 人[/bold]",
            f"[{color}]{bar}[/{color}] {pct:.1f}%",
        )

    # 组合主面板
    main_content = Table.grid(expand=True)
    main_content.add_column()

    main_content.add_row(Text("\n📊 人员统计信息\n", style="bold gold1 size 4"))
    main_content.add_row(Text("  数据概览\n", style="bold dim"))
    main_content.add_row(overview_grid)
    main_content.add_row(Text("\n"))
    main_content.add_row(type_table)
    main_content.add_row(Text(f"\n  💡 数据更新于当前会话  |  共 {stat[STAT_TOTAL]} 条记录\n", style="dim"))

    return Panel(
        main_content,
        title="📊 人员统计",
        border_style="cyan",
        padding=(1, 2),
    )


# ── 菜单项元组件 ──


class MenuGroupHeader(Static):
    """菜单分组标题"""
    DEFAULT_CSS = """
    MenuGroupHeader {
        padding: 1 0 0 1;
        color: $text-muted;
        text-style: bold;
        background: $surface-darken-2;
        height: 3;
        border-bottom: solid $primary 30%;
    }
    """


class MenuItem(ListItem):
    """带图标的菜单项"""

    DEFAULT_CSS = """
    MenuItem {
        padding: 1 2;
        color: $text-muted;
        height: 3;
        transition: background 150ms;
    }
    MenuItem:hover {
        background: $primary 20%;
        color: $text;
    }
    MenuItem.--active {
        background: $primary 40%;
        color: $text;
        border-left: thick $primary;
    }
    MenuItem > Static {
        width: 100%;
    }
    """

    def __init__(self, icon: str, label: str, menu_index: int):
        self.icon = icon
        self.label = label
        self.menu_index = menu_index
        super().__init__(Static(f"{icon}  {label}"))


# ── 左侧导航栏组件 ──

class Sidebar(Container):
    """左侧导航栏"""

    active_index = reactive(-1)

    DEFAULT_CSS = """
    Sidebar {
        width: 26;
        height: 100%;
        background: $surface-darken-1;
        border-right: solid $primary 30%;
    }
    Sidebar > #sidebar-title {
        padding: 1 2;
        height: 4;
        background: $primary 20%;
        color: $text;
        text-style: bold;
        content-align: center middle;
        border-bottom: solid $primary 50%;
    }
    Sidebar > ListView {
        height: 1fr;
        background: transparent;
    }
    Sidebar > ListView:focus {
        background: transparent;
    }
    Sidebar > #sidebar-footer {
        height: 3;
        padding: 0 2;
        background: $surface-darken-2;
        border-top: solid $primary 20%;
        color: $text-muted;
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("📁 功能菜单", id="sidebar-title")

        # 构建菜单项：单独加载welcome页面，然后分组加载其他页面
        items = [MenuItem("🏠", "Welcome!", -1)]

        current_group = None
        for i, (icon, name, group) in enumerate(MENU_ITEMS):
            if group != current_group:
                current_group = group
                items.append(
                    ListItem(
                        MenuGroupHeader(f"  ▸ {group}"),
                        disabled=True,
                    )
                )
            items.append(MenuItem(icon, name, i))
        # 遍历 MENU_ITEMS，遇到新分组就插入一个不可点击的分组标题，再加菜单项
        yield ListView(*items, id="nav-list")
        yield Static("⌨️  ↑↓ 选择 · Enter 确认", id="sidebar-footer")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """菜单选中事件"""
        item = event.item
        if isinstance(item, MenuItem):
            self.active_index = item.menu_index
            self.post_message(MenuSelected(item.menu_index))

    def watch_active_index(self, old_index: int, new_index: int) -> None:
        """监听选中变化，更新高亮"""
        list_view = self.query_one("#nav-list", ListView)
        for child in list_view.children:
            if isinstance(child, MenuItem):
                child.set_class(child.menu_index == new_index, "--active")


class MenuSelected(events.Message):
    """菜单选中消息"""
    def __init__(self, index: int):
        self.index = index
        super().__init__()


# ── 顶部状态栏 ──

class AutoSaveToggled(events.Message):
    """自动保存状态切换消息"""
    def __init__(self, value: bool):
        self.value = value
        super().__init__()


class StatusBar(Static):
    """顶部状态栏"""

    DEFAULT_CSS = """
    StatusBar {
        height: 3;
        padding: 0 2;
        background: $primary-darken-2;
        color: $text;
        dock: top;
    }
    StatusBar > Horizontal {
        height: 100%;
        align: center middle;
    }
    #status-title {
        width: 1fr;
        text-style: bold;
    }
    #auto-save-btn {
        width: auto;
        min-width: 18;
    }
    """

    def __init__(self, auto_save: bool):
        self.auto_save = auto_save
        super().__init__()

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("🏢 人员信息管理系统", id="status-title")
            yield Button(self._get_button_label(), id="auto-save-btn", variant="success" if self.auto_save else "warning")

    def _get_button_label(self) -> str:
        return "🟢 自动保存: 开" if self.auto_save else "🟡 自动保存: 关"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """点击按钮切换自动保存"""
        if event.button.id == "auto-save-btn":
            self.auto_save = not self.auto_save
            btn = self.query_one("#auto-save-btn", Button)
            btn.label = self._get_button_label()
            btn.variant = "success" if self.auto_save else "warning"
            self.post_message(AutoSaveToggled(self.auto_save))

    def update_auto_save(self, value: bool) -> None:
        """更新自动保存状态显示"""
        self.auto_save = value
        btn = self.query_one("#auto-save-btn", Button)
        btn.label = self._get_button_label()
        btn.variant = "success" if self.auto_save else "warning"


# ── 主内容区 ──

class MainContent(Container):
    """主内容区 - 左右布局"""

    DEFAULT_CSS = """
    MainContent {
        height: 1fr;
    }
    MainContent > Horizontal {
        height: 1fr;
    }
    #content-area {
        height: 1fr;
        width: 1fr;
        background: $surface;
    }
    """

    # 菜单名称 → 页面构造函数的映射
    PAGE_MAP = {
        "查询人员": lambda svc, auto: PersonFilterPage(svc, "查询"),
        "显示人员": lambda svc, auto: PersonListPage(svc),
        "修改人员": lambda svc, auto: PersonFilterPage(svc, "修改"),
        "删除人员": lambda svc, auto: PersonFilterPage(svc, "删除"),
        "统计人员": lambda svc, auto: RichPanelPage(render_statistics_page(svc)),
    }

    def __init__(self, service: PersonService, auto_save: bool):
        self.service = service
        self.auto_save = auto_save
        super().__init__()

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Sidebar()
            yield Vertical(
                RichPanelPage(render_welcome_page(self.service, self.auto_save)),
                id="content-area"
            )

    def _build_page(self, index: int):
        """根据菜单索引构建页面组件（统一页面构建逻辑）"""
        if index == -1:
            return RichPanelPage(render_welcome_page(self.service, self.auto_save))
        icon, name, _ = MENU_ITEMS[index]
        builder = self.PAGE_MAP.get(name)
        return builder(self.service, self.auto_save) if builder else RichPanelPage(render_welcome_page(self.service, self.auto_save))

    def on_menu_selected(self, event: MenuSelected) -> None:
        """处理菜单选中消息"""
        if event.index == -1:
            # Welcome page
            content = self.query_one("#content-area", Vertical)
            content.remove_children()
            content.mount(self._build_page(event.index))
            return

        icon, name, _ = MENU_ITEMS[event.index]

        # 操作类菜单项：不切换页面，直接执行操作
        if name == "添加人员":
            self.app.push_screen(PersonAddScreen(self.service, on_done=self._refresh_current_page))
            return
        elif name == "手动保存":
            try:
                self.service.save()
                self.app.notify("💾 数据已保存", title="保存成功", severity="information", timeout=2)
                self._refresh_current_page()
            except Exception as e:
                self.app.notify(f"保存失败：{e}", title="错误", severity="error", timeout=3)
            return
        elif name == "读取数据":
            try:
                self.service.load()
                self.app.notify("📂 数据已重新加载", title="读取成功", severity="information", timeout=2)
                self._refresh_current_page()
            except Exception as e:
                self.app.notify(f"加载失败：{e}", title="错误", severity="error", timeout=3)
            return
        elif name == "导出 CSV":
            try:
                DataExporter.export_csv(self.service.person_list)
                self.app.notify("📤 数据已导出到 data/person.csv", title="导出成功", severity="information", timeout=3)
            except Exception as e:
                self.app.notify(f"导出失败：{e}", title="错误", severity="error", timeout=3)
            return
        elif name == "导入 CSV":
            self.app.push_screen(CsvImportScreen(self.service, on_done=self._refresh_current_page))
            return

        # 其他菜单项：正常切换页面
        content = self.query_one("#content-area", Vertical)
        content.remove_children()
        content.mount(self._build_page(event.index))

    def refresh_welcome(self) -> None:
        """刷新欢迎页数据"""
        content = self.query_one("#content-area", Vertical)
        sidebar = self.query_one(Sidebar)
        if sidebar.active_index is None or sidebar.active_index < 0:
            content.remove_children()
            content.mount(RichPanelPage(render_welcome_page(self.service, self.auto_save)))

    def _refresh_current_page(self) -> None:
        """刷新当前页面数据"""
        sidebar = self.query_one(Sidebar)
        content = self.query_one("#content-area", Vertical)
        active_idx = sidebar.active_index

        # 操作类菜单项（索引 6-9）没有对应页面，不重建
        if active_idx is None or 6 <= active_idx <= 9:
            return

        content.remove_children()
        content.mount(self._build_page(active_idx))


# ── App 主类 ──

class PersonTuiApp(App):
    """人员信息管理系统 TUI 应用"""

    CSS = """
    Screen {
        background: $surface;
    }

    Footer {
        background: $primary-darken-3;
        color: $text-muted;
        height: 2;
    }
    Footer > .footer--key {
        background: $primary-darken-2;
        color: $text;
    }
    """

    TITLE = "人员信息管理系统"
    SUB_TITLE = "Python 面向对象课程设计"

    # 绑定快捷键
    BINDINGS = [
        ("q", "quit", "退出"),
        ("s", "save", "保存"),
        ("r", "reload", "刷新"),
    ]

    def __init__(self):
        super().__init__()
        self.service = PersonService()
        self.service.load()
        self.auto_save_on = False
        self.load_config()

    def load_config(self):
        """从 config.json 加载自动保存开关状态"""
        self.auto_save_on = load_auto_save()

    def save_config(self):
        """将自动保存开关状态持久化到 config.json"""
        save_auto_save(self.auto_save_on)

    def compose(self) -> ComposeResult:
        yield StatusBar(self.auto_save_on)
        yield MainContent(self.service, self.auto_save_on)
        yield Footer()

    def action_save(self) -> None:
        """手动保存"""
        try:
            self.service.save()
            self.notify("💾 数据已保存", title="保存成功", severity="information", timeout=2)
            self._refresh_current_page()
        except Exception as e:
            self.notify(f"保存失败：{e}", title="错误", severity="error", timeout=3)

    def action_reload(self) -> None:
        """重新加载数据"""
        try:
            self.service.load()
            self.notify("📂 数据已重新加载", title="读取成功", severity="information", timeout=2)
            self._refresh_current_page()
        except Exception as e:
            self.notify(f"加载失败：{e}", title="错误", severity="error", timeout=3)

    def _refresh_current_page(self) -> None:
        """刷新当前页面的数据"""
        main_content = self.query_one(MainContent)
        main_content.auto_save = self.auto_save_on
        sidebar = main_content.query_one(Sidebar)
        content = main_content.query_one("#content-area", Vertical)
        active_idx = sidebar.active_index
        # 操作类菜单项（索引 6-9）没有对应页面，不重建
        if active_idx is not None and 6 <= active_idx <= 9:
            return
        content.remove_children()
        content.mount(main_content._build_page(active_idx))

    def action_quit(self) -> None:
        """退出应用"""
        self.service.save()
        self.exit()

    def on_auto_save_toggled(self, event: AutoSaveToggled) -> None:
        """处理自动保存状态切换"""
        self.auto_save_on = event.value
        self.save_config()
        msg = "自动保存已开启" if self.auto_save_on else "自动保存已关闭"
        self.notify(msg, title="设置变更", severity="information", timeout=2)

    def on_mount(self) -> None:
        """应用启动后"""
        self.notify(
            f"欢迎使用人员信息管理系统\n当前共 {len(self.service.person_list)} 条记录",
            title="系统启动",
            severity="information",
            timeout=3,
        )


if __name__ == "__main__":
    PersonTuiApp().run()
