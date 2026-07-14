"""
UI 层通用组件

提供 RichPanelPage 基类，合并 WelcomePage / PlaceholderPage / _RichPanelPage
等结构相同的页面组件，消除重复代码。
"""
from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import VerticalScroll
from textual.message import Message
from rich.panel import Panel


class RichPanelPage(VerticalScroll):
    """通用 Rich Panel 页面基类

    用于展示任意 rich Panel 内容，合并原本结构相同的
    WelcomePage、PlaceholderPage、_RichPanelPage 三个类。
    """

    DEFAULT_CSS = """
    RichPanelPage {
        height: 100%;
        padding: 1 2;
    }
    RichPanelPage > Static {
        height: auto;
    }
    """

    def __init__(self, panel: Panel):
        self._panel = panel
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static(self._panel)

    def update_panel(self, new_panel: Panel) -> None:
        """刷新内容"""
        self.remove_children()
        self._panel = new_panel
        self.mount(Static(new_panel))


class DataChanged(Message):
    """数据变更消息"""
    pass
