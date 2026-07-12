"""
TUI 界面模块 - 基于 Textual 的终端用户界面

使用 rich + textual 实现类 GUI 体验，支持鼠标点击和键盘操作。
左右布局：左侧导航菜单，右侧内容区。
"""
from textual.app import App, ComposeResult
from textual.widgets import (
    Header, Footer, Static, ListItem, ListView
)
from textual.containers import Container, Horizontal, Vertical


# ─── 左侧导航栏 ───

class Sidebar(Container):
    """左侧导航栏"""

    DEFAULT_CSS = """
    Sidebar {
        width: 24;
        height: 100%;
        border: round $primary;
        background: $surface-darken-1;
    }
    Sidebar > ListView {
        height: 1fr;
    }
    Sidebar > ListView > ListItem {
        padding: 1 2;
        color: $text-muted;
    }
    Sidebar > ListView > ListItem:hover {
        background: $primary 20%;
        color: $text;
    }
    """

    def compose(self) -> ComposeResult:
        yield ListView(
            ListItem(Static("  添加人员")),
            ListItem(Static("  查询人员")),
            ListItem(Static("  显示人员")),
            ListItem(Static("  修改人员")),
            ListItem(Static("  删除人员")),
            ListItem(Static("  统计人员")),
            ListItem(Static("  手动保存")),
            ListItem(Static("  读取数据")),
            ListItem(Static("  导出 CSV")),
            ListItem(Static("  导入 CSV")),
            id="nav-list"
        )


# ─── 右侧内容页 ───

class ContentPage(Static):
    """通用内容页 - 占位"""

    DEFAULT_CSS = """
    ContentPage {
        height: 100%;
        width: 100%;
        content-align: center middle;
        color: $text-muted;
        border: round $secondary;
        background: $surface;
    }
    """

    def __init__(self, title: str = "开发中..."):
        super().__init__(title)


# ─── 主内容区 ───

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
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Sidebar()
            with Vertical(id="content-area"):
                yield ContentPage("欢迎使用人员信息管理系统\n\n请从左侧菜单选择功能")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """左侧菜单点击事件"""
        index = event.list_view.index
        content = self.query_one("#content-area", Vertical)
        content.remove_children()

        pages = [
            ContentPage("添加人员\n\n开发中..."),
            ContentPage("查询人员\n\n开发中..."),
            ContentPage("显示人员\n\n开发中..."),
            ContentPage("修改人员\n\n开发中..."),
            ContentPage("删除人员\n\n开发中..."),
            ContentPage("统计人员\n\n开发中..."),
            ContentPage("手动保存\n\n开发中..."),
            ContentPage("读取数据\n\n开发中..."),
            ContentPage("导出 CSV\n\n开发中..."),
            ContentPage("导入 CSV\n\n开发中..."),
        ]
        if 0 <= index < len(pages):
            content.append(pages[index])


# ─── App 主类 ───

class PersonTuiApp(App):
    """人员信息管理系统 TUI 应用"""

    CSS = """
    Header {
        height: 4;
        dock: top;
        background: $primary 30%;
        color: $text;
        content-align: center middle;
    }
    """

    TITLE = "人员信息管理系统"
    SUB_TITLE = "Python 面向对象课程设计"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield MainContent()
        yield Footer()


if __name__ == "__main__":
    PersonTuiApp().run()
