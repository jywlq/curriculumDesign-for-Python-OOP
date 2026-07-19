"""
人员修改弹窗组件

显示当前人员信息，用户可逐字段修改后保存。
通过 get_fields() 动态获取特有字段，实现多态。
"""
from textual.app import ComposeResult
from textual.widgets import Static, Button, Input, Label, Select
from textual.containers import Container, Vertical, Horizontal

from src.services import PersonService
from src.ui.constants import CLASS_MAP, camel_to_snake
from src.ui.tui.person_form_screen import PersonFormScreen
from src.ui.tui.widgets import DataChanged


class PersonEditScreen(PersonFormScreen):
    """人员修改弹窗 - 居中弹窗

    用法：
        app.push_screen(PersonEditScreen(person, service))

    关闭方式：
        - 点击「保存」按钮（保存后关闭）
        - 点击「取消」按钮（不保存关闭）
        - 按 Escape（不保存关闭）
    """

    def __init__(self, person, service: PersonService, on_done=None):
        self.person = person
        super().__init__(service, on_done)

    def _get_person_class(self):
        return type(self.person)

    def _get_confirm_message(self) -> str:
        return "确认保存修改？"

    def compose(self) -> ComposeResult:
        with Container(id="edit-container"):
            yield Static("✏️ 修改人员信息", id="edit-title")

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
                        allow_blank=False,
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

    def _do_save(self, data: dict) -> None:
        """执行保存"""
        person_class = CLASS_MAP.get(type(self.person).__name__)
        if not person_class:
            self.app.notify("未知的人员类型", title="错误", severity="error", timeout=3)
            return

        try:
            init_params = self._convert_to_init_params(data)
            new_person = person_class(**init_params)
            if self.service.update_person(self.person._person_id, new_person):
                self.app.notify("修改成功", title="成功", severity="information", timeout=2)
                self.post_message(DataChanged())
                if self.on_done:
                    self.on_done()
                self.app.pop_screen()
            else:
                self.app.notify("修改失败，编号可能已存在", title="失败", severity="warning", timeout=3)
        except Exception as e:
            self.app.notify(f"修改失败：{e}", title="错误", severity="error", timeout=3)