"""
通用确认弹窗组件

可复用的确认对话框，支持自定义标题、消息和确认回调。
"""
from textual.app import ComposeResult, Screen
from textual.widgets import Static, Button
from textual.containers import Container, Vertical, Horizontal


class ConfirmScreen(Screen):
    """通用确认弹窗

    用法：
        app.push_screen(ConfirmScreen("确认删除？", on_confirm, data))

    参数：
        message: 显示的确认消息
        on_confirm: 确认回调函数，接收 data 参数
        data: 传递给回调函数的数据
    """

    BINDINGS = [
        ("escape", "cancel", "取消"),
    ]

    DEFAULT_CSS = """
    ConfirmScreen {
        align: center middle;
        background: black 30%;
    }

    #confirm-container {
        width: 40%;
        min-width: 35;
        height: auto;
        background: $surface;
        border: round $primary;
        padding: 1 2;
    }

    #confirm-message {
        height: auto;
        text-align: center;
        text-style: bold;
        color: $text;
        margin: 2 0;
    }

    #confirm-buttons {
        height: 4;
        margin-top: 1;
        align: center middle;
    }
    #confirm-buttons > Button {
        width: 14;
        margin: 0 1;
    }
    """

    def __init__(self, message: str, on_confirm=None, data=None):
        self.message = message
        self.on_confirm = on_confirm
        self.data = data
        super().__init__()

    def compose(self) -> ComposeResult:
        with Container(id="confirm-container"):
            yield Static(self.message, id="confirm-message")
            with Horizontal(id="confirm-buttons"):
                yield Button("确认", variant="primary", id="btn-confirm")
                yield Button("取消", variant="default", id="btn-cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮点击事件"""
        if event.button.id == "btn-confirm":
            self.app.pop_screen()
            if self.on_confirm:
                if self.data is not None:
                    self.on_confirm(self.data)
                else:
                    self.on_confirm()
        elif event.button.id == "btn-cancel":
            self.app.pop_screen()

    def action_cancel(self) -> None:
        """取消操作"""
        self.app.pop_screen()
