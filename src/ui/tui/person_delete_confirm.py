"""
人员删除确认弹窗组件

显示人员信息，用户确认后删除。
复用 render_person_detail_modal() 渲染人员信息。
"""
from textual.app import ComposeResult, Screen
from textual.widgets import Static, Button
from textual.containers import Container, Vertical, Horizontal

from src.services import PersonService
from src.ui.tui.person_detail_page import render_person_detail_modal
from src.ui.tui.widgets import DataChanged


class PersonDeleteConfirmScreen(Screen):
    """删除确认弹窗 - 居中弹窗

    用法：
        app.push_screen(PersonDeleteConfirmScreen(person, service))

    关闭方式：
        - 点击「确认删除」按钮（删除后关闭）
        - 点击「取消」按钮（不删除关闭）
        - 按 Escape（不删除关闭）
    """

    BINDINGS = [
        ("escape", "cancel", "取消"),
    ]

    DEFAULT_CSS = """
    PersonDeleteConfirmScreen {
        align: center middle;
        background: black 30%;
    }

    #confirm-container {
        width: 50%;
        min-width: 40;
        height: auto;
        background: $surface;
        border: round $error;
        padding: 1 2;
    }

    #confirm-title {
        height: 3;
        text-align: center;
        text-style: bold;
        color: $error;
        margin-bottom: 1;
    }

    #confirm-message {
        height: auto;
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }

    #confirm-buttons {
        height: 4;
        margin-top: 1;
        align: center middle;
    }
    #confirm-buttons > Button {
        width: 16;
        margin: 0 1;
    }
    """

    def __init__(self, person, service: PersonService, on_done=None):
        self.person = person
        self.service = service
        self.on_done = on_done
        super().__init__()

    def compose(self) -> ComposeResult:
        with Container(id="confirm-container"):
            yield Static("⚠️ 确认删除", id="confirm-title")
            yield Static("此操作不可撤销，确定要删除以下人员吗？", id="confirm-message")
            yield Static(render_person_detail_modal(self.person))
            with Horizontal(id="confirm-buttons"):
                yield Button("确认删除", variant="error", id="btn-confirm")
                yield Button("取消", variant="default", id="btn-cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮点击事件"""
        if event.button.id == "btn-confirm":
            if self.service.delete_person(self.person._person_id):
                self.app.notify(
                    f"已删除: {self.person._person_name}",
                    title="删除成功",
                    severity="information",
                    timeout=2
                )
                # 发送数据变更消息
                self.post_message(DataChanged())
                if self.on_done:
                    self.on_done()
                self.app.pop_screen()
            else:
                self.app.notify("删除失败", title="错误", severity="error", timeout=3)

        elif event.button.id == "btn-cancel":
            self.app.pop_screen()

    def action_cancel(self) -> None:
        """取消操作"""
        self.app.pop_screen()
