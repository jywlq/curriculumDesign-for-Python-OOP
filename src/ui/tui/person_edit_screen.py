"""
人员修改弹窗组件

显示当前人员信息，用户可逐字段修改后保存。
通过 get_fields() 动态获取特有字段，实现多态。
"""
from textual.app import ComposeResult, Screen
from textual.widgets import Static, Button, Input, Label, Select
from textual.containers import Container, Vertical, Horizontal

from src.services import PersonService
from src.ui.tui.confirm_screen import ConfirmScreen
from src.ui.constants import ID_PATTERN, CLASS_MAP, camel_to_snake
from src.ui.tui.widgets import DataChanged


class PersonEditScreen(Screen):
    """人员修改弹窗 - 居中弹窗

    用法：
        app.push_screen(PersonEditScreen(person, service))

    关闭方式：
        - 点击「保存」按钮（保存后关闭）
        - 点击「取消」按钮（不保存关闭）
        - 按 Escape（不保存关闭）
    """

    BINDINGS = [
        ("escape", "cancel", "取消"),
    ]

    DEFAULT_CSS = """
    PersonEditScreen {
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

    def __init__(self, person, service: PersonService, on_done=None):
        self.person = person
        self.service = service
        self.on_done = on_done
        self.person_type = type(person).__name__
        self.fields = {}  # 存储输入控件引用
        super().__init__()

    def compose(self) -> ComposeResult:
        with Container(id="edit-container"):
            yield Static(f"✏️ 修改人员信息", id="edit-title")

            with Vertical(id="edit-form"):
                # 公共字段
                with Vertical(classes="field-group"):
                    yield Label("编号（格式：T/E/A/TA + 三位数字）", classes="field-label")
                    yield Input(
                        value=self.person._person_id,
                        placeholder="编号",
                        classes="field-input",
                        id="input-id"
                    )

                with Vertical(classes="field-group"):
                    yield Label("姓名", classes="field-label")
                    yield Input(
                        value=self.person._person_name,
                        placeholder="姓名",
                        classes="field-input",
                        id="input-name"
                    )

                with Vertical(classes="field-group"):
                    yield Label("性别", classes="field-label")
                    yield Select(
                        options=[("男", "男"), ("女", "女")],
                        prompt="请选择性别",
                        value=self.person._person_gender,
                        id="input-gender",
                        classes="field-input",
                    )

                with Vertical(classes="field-group"):
                    yield Label("年龄", classes="field-label")
                    yield Input(
                        value=str(self.person._person_age),
                        placeholder="年龄",
                        classes="field-input",
                        id="input-age"
                    )

                # 特有字段（通过 get_fields() 动态生成）
                for field_key, field_prompt in type(self.person).get_fields():
                    # 从 person 对象获取当前值（驼峰转下划线）
                    attr_name = f"_{camel_to_snake(field_key)}"
                    current_value = getattr(self.person, attr_name, "")
                    with Vertical(classes="field-group"):
                        yield Label(field_prompt, classes="field-label")
                        yield Input(
                            value=current_value,
                            placeholder=field_prompt,
                            classes="field-input",
                            id=f"input-{field_key}"
                        )

            with Horizontal(id="edit-buttons"):
                yield Button("✓ 保存", variant="success", id="btn-save")
                yield Button("✕ 取消", variant="default", id="btn-cancel")

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
        for field_key, _ in type(self.person).get_fields():
            input_widget = self.query_one(f"#input-{field_key}", Input)
            data[field_key] = input_widget.value.strip()
        return data

    def _convert_to_init_params(self, data: dict) -> dict:
        """将收集的数据转换为 __init__ 参数格式（驼峰→下划线）"""
        # 公共字段映射
        result = {
            "person_id": data["personID"],
            "person_name": data["personName"],
            "person_gender": data["personGender"],
            "person_age": data["personAge"],
        }
        # 特有字段：驼峰转下划线
        for field_key, _ in type(self.person).get_fields():
            snake_key = camel_to_snake(field_key)
            result[snake_key] = data[field_key]
        return result

    def _validate_data(self, data: dict) -> str:
        """验证数据，返回错误信息，成功返回空字符串"""
        # 编号验证
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
        # 检查特有字段是否为空
        for field_key, field_prompt in type(self.person).get_fields():
            if not data[field_key]:
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

            # 弹出确认对话框
            self.app.push_screen(
                ConfirmScreen("确认保存修改？", self._do_save, data)
            )

        elif event.button.id == "btn-cancel":
            self.app.pop_screen()

    def _do_save(self, data: dict) -> None:
        """执行保存"""
        person_class = CLASS_MAP.get(self.person_type)
        if not person_class:
            self.app.notify("未知的人员类型", title="错误", severity="error", timeout=3)
            return

        try:
            # 转换数据格式：驼峰→下划线
            init_params = self._convert_to_init_params(data)
            new_person = person_class(**init_params)
            if self.service.update_person(self.person._person_id, new_person):
                self.app.notify("修改成功", title="成功", severity="information", timeout=2)
                # 发送数据变更消息
                self.post_message(DataChanged())
                if self.on_done:
                    self.on_done()
                self.app.pop_screen()
            else:
                self.app.notify("修改失败，编号可能已存在", title="失败", severity="warning", timeout=3)
        except Exception as e:
            self.app.notify(f"修改失败：{e}", title="错误", severity="error", timeout=3)

    def action_cancel(self) -> None:
        """取消操作"""
        self.app.pop_screen()
