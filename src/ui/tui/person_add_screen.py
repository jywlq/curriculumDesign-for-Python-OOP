"""
人员添加弹窗组件

显示空白表单，用户选择类型后填写各字段并保存。
通过 get_fields() 动态获取特有字段，实现多态。
"""
from textual.app import ComposeResult
from textual.widgets import Static, Button, Input, Label, Select
from textual.containers import Container, Vertical, Horizontal

from src.services import PersonService
from src.ui.constants import CLASS_MAP
from src.ui.tui.person_form_screen import PersonFormScreen
from src.ui.tui.widgets import DataChanged


class PersonAddScreen(PersonFormScreen):
    """人员添加弹窗 - 居中弹窗

    用法：
        app.push_screen(PersonAddScreen(service))

    关闭方式：
        - 点击「保存」按钮（保存后关闭）
        - 点击「取消」按钮（不保存关闭）
        - 按 Escape（不保存关闭）
    """

    def __init__(self, service: PersonService, on_done=None):
        self.selected_type = "Teacher"
        super().__init__(service, on_done)

    def _get_person_class(self):
        return CLASS_MAP.get(self.selected_type)

    def _get_confirm_message(self) -> str:
        return "确认添加此人员？"

    def compose(self) -> ComposeResult:
        with Container(id="edit-container"):
            yield Static("➕ 添加人员", id="edit-title")

            with Vertical(id="edit-form"):
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

    def _do_save(self, data: dict) -> None:
        """执行保存"""
        person_class = CLASS_MAP.get(self.selected_type)
        if not person_class:
            self.app.notify("未知的人员类型", title="错误", severity="error", timeout=3)
            return

        try:
            init_params = self._convert_to_init_params(data)
            new_person = person_class(**init_params)

            if self.service.person_id_check(new_person._person_id):
                self.app.notify("添加失败，编号已存在", title="失败", severity="warning", timeout=3)
                return

            if self.service.add_person(new_person):
                self.app.notify("添加成功", title="成功", severity="information", timeout=2)
                self.post_message(DataChanged())
                if self.on_done:
                    self.on_done()
                self.app.pop_screen()
            else:
                self.app.notify("添加失败", title="失败", severity="warning", timeout=3)
        except Exception as e:
            self.app.notify(f"添加失败：{e}", title="错误", severity="error", timeout=3)