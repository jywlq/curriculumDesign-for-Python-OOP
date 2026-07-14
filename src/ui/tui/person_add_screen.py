"""
人员添加弹窗组件

显示空白表单，用户选择类型后填写各字段并保存。
通过 get_fields() 动态获取特有字段，实现多态。
"""
from textual.app import ComposeResult, Screen
from textual.widgets import Static, Button, Input, Label, Select
from textual.containers import Container, Vertical, Horizontal

from src.services import PersonService
from src.ui.tui.confirm_screen import ConfirmScreen
from src.ui.constants import ID_PATTERN, CLASS_MAP, camel_to_snake
from src.ui.tui.widgets import DataChanged


class PersonAddScreen(Screen):
    """人员添加弹窗 - 居中弹窗

    用法：
        app.push_screen(PersonAddScreen(service))

    关闭方式：
        - 点击「保存」按钮（保存后关闭）
        - 点击「取消」按钮（不保存关闭）
        - 按 Escape（不保存关闭）
    """

    BINDINGS = [
        ("escape", "cancel", "取消"),
    ]

    DEFAULT_CSS = """
    PersonAddScreen {
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
        self.selected_type = "Teacher"  # 默认选中教师类型
        super().__init__()

    def compose(self) -> ComposeResult:
        with Container(id="edit-container"):
            yield Static("➕ 添加人员", id="edit-title")

            with Vertical(id="edit-form"):
                # 人员类型选择器
                with Vertical(classes="field-group"):
                    yield Label("人员类型", classes="field-label")
                    yield Select(
                        options=[
                            ("教师", "Teacher"),
                            ("实验员", "Experimenter"),
                            ("行政人员", "Admin"),
                            ("教师兼行政", "TeacherAdmin"),
                        ],
                        prompt="请选择人员类型",
                        id="select-type",
                        classes="field-input",
                    )

                # 公共字段
                with Vertical(classes="field-group"):
                    yield Label("编号（格式：T/E/A/TA + 三位数字）", classes="field-label")
                    yield Input(
                        placeholder="编号",
                        classes="field-input",
                        id="input-id"
                    )

                with Vertical(classes="field-group"):
                    yield Label("姓名", classes="field-label")
                    yield Input(
                        placeholder="姓名",
                        classes="field-input",
                        id="input-name"
                    )

                with Vertical(classes="field-group"):
                    yield Label("性别", classes="field-label")
                    yield Select(
                        options=[("男", "男"), ("女", "女")],
                        prompt="请选择性别",
                        id="input-gender",
                        classes="field-input",
                    )

                with Vertical(classes="field-group"):
                    yield Label("年龄", classes="field-label")
                    yield Input(
                        placeholder="年龄",
                        classes="field-input",
                        id="input-age"
                    )
            with Horizontal(id="edit-buttons"):
                yield Button("✓ 保存", variant="success", id="btn-save")
                yield Button("✕ 取消", variant="default", id="btn-cancel")

    def on_mount(self) -> None:
        """挂载后设置默认选中值并初始化额外字段"""
        select = self.query_one("#select-type", Select)
        select.value = "Teacher"
        gender_select = self.query_one("#input-gender", Select)
        gender_select.value = "男"
        self._rebuild_extra_fields()

    def on_select_changed(self, event: Select.Changed) -> None:
        """类型选择器变更时重建额外字段"""
        if event.select.id == "select-type" and event.value is not None:
            self.selected_type = event.value
            self._rebuild_extra_fields()

    def _rebuild_extra_fields(self) -> None:
        """根据当前选中的类型重建额外字段，直接挂载到 #edit-form 末尾"""
        form = self.query_one("#edit-form", Vertical)

        # 批量移除旧的特有字段组（通过 CSS class 选择器）
        form.remove_children(".extra-field")

        person_class = CLASS_MAP.get(self.selected_type)
        if not person_class:
            return

        for field_key, field_prompt in person_class.get_fields():
            form.mount(
                Vertical(
                    Label(field_prompt, classes="field-label"),
                    Input(
                        placeholder=field_prompt,
                        classes="field-input",
                        id=f"input-{field_key}"
                    ),
                    classes="field-group extra-field",
                )
            )

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
        person_class = CLASS_MAP.get(self.selected_type)
        if person_class:
            for field_key, _ in person_class.get_fields():
                try:
                    input_widget = self.query_one(f"#input-{field_key}", Input)
                    data[field_key] = input_widget.value.strip()
                except Exception:
                    data[field_key] = ""
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
        person_class = CLASS_MAP.get(self.selected_type)
        if person_class:
            for field_key, _ in person_class.get_fields():
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
        person_class = CLASS_MAP.get(self.selected_type)
        if person_class:
            for field_key, field_prompt in person_class.get_fields():
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

            # 弹出确认对话框
            self.app.push_screen(
                ConfirmScreen("确认添加此人员？", self._do_save, data)
            )

        elif event.button.id == "btn-cancel":
            self.app.pop_screen()

    def _do_save(self, data: dict) -> None:
        """执行保存"""
        person_class = CLASS_MAP.get(self.selected_type)
        if not person_class:
            self.app.notify("未知的人员类型", title="错误", severity="error", timeout=3)
            return

        try:
            # 转换数据格式：驼峰→下划线
            init_params = self._convert_to_init_params(data)
            new_person = person_class(**init_params)

            # 检查编号是否重复
            if self.service.person_id_check(new_person._person_id):
                self.app.notify("添加失败，编号已存在", title="失败", severity="warning", timeout=3)
                return

            if self.service.add_person(new_person):
                self.app.notify("添加成功", title="成功", severity="information", timeout=2)
                # 发送数据变更消息
                self.post_message(DataChanged())
                if self.on_done:
                    self.on_done()
                self.app.pop_screen()
            else:
                self.app.notify("添加失败", title="失败", severity="warning", timeout=3)
        except Exception as e:
            self.app.notify(f"添加失败：{e}", title="错误", severity="error", timeout=3)

    def action_cancel(self) -> None:
        """取消操作"""
        self.app.pop_screen()