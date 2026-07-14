"""
人员表单弹窗基类

提取 PersonEditScreen 和 PersonAddScreen 的公共代码：
共享 CSS、_collect_data、_convert_to_init_params、_validate_data、按钮处理。
"""
from textual.app import ComposeResult, Screen
from textual.widgets import Static, Button, Input, Label, Select
from textual.containers import Container, Vertical, Horizontal

from src.services import PersonService
from src.ui.tui.confirm_screen import ConfirmScreen
from src.ui.constants import ID_PATTERN, CLASS_MAP, camel_to_snake
from src.ui.tui.widgets import DataChanged


class PersonFormScreen(Screen):
    """人员表单弹窗基类"""

    BINDINGS = [
        ("escape", "cancel", "取消"),
    ]

    DEFAULT_CSS = """
    PersonFormScreen {
        align: center middle;
        background: black 30%;
    }

    #edit-container {
        width: 60%;
        min-width: 50;
        height: auto;
        max-height: 80%;
        overflow-y: auto;
        background: $surface;
        border: round $primary;
        padding: 1 2;
    }

    #edit-title {
        height: 3;
        text-align: center;
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    #edit-form {
        height: auto;
    }

    .field-group {
        height: auto;
        margin-bottom: 1;
    }
    .field-label {
        height: 2;
        color: $text-muted;
    }
    .field-input {
        height: 3;
    }

    #edit-buttons {
        height: 4;
        margin-top: 1;
        align: center middle;
    }
    #edit-buttons > Button {
        width: 16;
        margin: 0 1;
    }
    """

    def __init__(self, service: PersonService, on_done=None):
        self.service = service
        self.on_done = on_done
        super().__init__()

    def _get_person_class(self):
        """返回当前操作的人员类型，由子类实现"""
        raise NotImplementedError

    def _get_fields(self):
        """获取当前人员类型的字段列表"""
        cls = self._get_person_class()
        return cls.get_fields() if cls else []

    def _collect_data(self) -> dict:
        """收集表单数据（返回驼峰格式，供验证用）"""
        gender_val = self.query_one("#input-gender", Select).value
        data = {
            "personID": self.query_one("#input-id", Input).value.strip(),
            "personName": self.query_one("#input-name", Input).value.strip(),
            "personGender": gender_val if gender_val != Select.BLANK else "",
            "personAge": self.query_one("#input-age", Input).value.strip(),
        }
        # 收集特有字段（驼峰格式）
        for field_key, _ in self._get_fields():
            try:
                input_widget = self.query_one(f"#input-{field_key}", Input)
                data[field_key] = input_widget.value.strip()
            except Exception:
                data[field_key] = ""
        return data

    def _convert_to_init_params(self, data: dict) -> dict:
        """将收集的数据转换为 __init__ 参数格式（驼峰→下划线）"""
        result = {
            "person_id": data["personID"],
            "person_name": data["personName"],
            "person_gender": data["personGender"],
            "person_age": data["personAge"],
        }
        for field_key, _ in self._get_fields():
            snake_key = camel_to_snake(field_key)
            result[snake_key] = data.get(field_key, "")
        return result

    def _validate_data(self, data: dict) -> str:
        """验证数据，返回错误信息，成功返回空字符串"""
        if not data["personID"]:
            return "编号不能为空"
        if not ID_PATTERN.match(data["personID"]):
            return "编号格式错误，应为 T/E/A/TA + 三位数字"
        if not data["personName"]:
            return "姓名不能为空"
        if len(data["personName"]) < 2 or len(data["personName"]) > 20:
            return "姓名长度必须在 2-20 个字符之间"
        if data["personGender"] not in ("男", "女"):
            return "性别只能是男或女"
        try:
            age = int(data["personAge"])
            if age < 1 or age > 150:
                return "年龄必须在 1-150 之间"
        except ValueError:
            return "年龄必须是一个整数"
        for field_key, field_prompt in self._get_fields():
            if not data.get(field_key, ""):
                return f"{field_prompt}不能为空"
        return ""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮点击事件"""
        if event.button.id == "btn-save":
            data = self._collect_data()
            error = self._validate_data(data)
            if error:
                self.app.notify(error, title="验证失败", severity="warning", timeout=3)
                return
            self.app.push_screen(
                ConfirmScreen(self._get_confirm_message(), self._do_save, data)
            )
        elif event.button.id == "btn-cancel":
            self.app.pop_screen()

    def _get_confirm_message(self) -> str:
        """返回确认对话框的消息文本"""
        raise NotImplementedError

    def _do_save(self, data: dict) -> None:
        """执行保存操作，由子类实现"""
        raise NotImplementedError

    def action_cancel(self) -> None:
        """取消操作"""
        self.app.pop_screen()