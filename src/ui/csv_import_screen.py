"""
CSV导入引导屏幕

复用CLI的导入流程，提示用户将CSV放入指定目录，输入文件名后导入。
"""
from textual.app import ComposeResult, Screen
from textual.widgets import Static, Button, Input, Label
from textual.containers import Container, Vertical, Horizontal

from src.services import PersonService
from src.services.csv_import import DataImporter


class CsvImportScreen(Screen):
    """CSV导入引导屏幕

    用法：
        app.push_screen(CsvImportScreen(service, on_done=callback))
    """

    BINDINGS = [
        ("escape", "cancel", "取消"),
    ]

    DEFAULT_CSS = """
    CsvImportScreen {
        align: center middle;
        background: black 30%;
    }

    #import-container {
        width: 55%;
        min-width: 45;
        height: auto;
        background: $surface;
        border: round $primary;
        padding: 1 2;
    }

    #import-title {
        height: 3;
        text-align: center;
        text-style: bold;
        color: $text;
        margin-bottom: 1;
    }

    #import-guide {
        height: auto;
        margin-bottom: 1;
        color: $text-muted;
    }

    .guide-line {
        height: 2;
        color: $text-muted;
    }

    #import-input-area {
        height: auto;
        margin: 1 0;
    }
    #import-input-area > Label {
        height: 2;
        color: $text-muted;
    }
    #import-input-area > Input {
        height: 3;
    }

    #import-buttons {
        height: 4;
        margin-top: 1;
        align: center middle;
    }
    #import-buttons > Button {
        width: 16;
        margin: 0 1;
    }
    """

    def __init__(self, service: PersonService, on_done=None):
        self.service = service
        self.on_done = on_done
        super().__init__()

    def compose(self) -> ComposeResult:
        with Container(id="import-container"):
            yield Static("📥 导入 CSV 数据", id="import-title")

            with Vertical(id="import-guide"):
                yield Static("请将CSV文件放入 data/import/ 目录", classes="guide-line")
                yield Static("文件需包含表头：编号,姓名,性别,年龄,类型,特有字段", classes="guide-line")
                yield Static("注意：请勿重复导入，表头逗号为英文逗号", classes="guide-line")

            with Vertical(id="import-input-area"):
                yield Label("请输入文件名（如 test.csv）：")
                yield Input(
                    placeholder="文件名",
                    id="import-filename",
                )

            with Horizontal(id="import-buttons"):
                yield Button("✓ 导入", variant="success", id="btn-import")
                yield Button("✕ 取消", variant="default", id="btn-cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-import":
            filename = self.query_one("#import-filename", Input).value.strip()
            if not filename:
                self.app.notify("请输入文件名", title="提示", severity="warning", timeout=2)
                return

            filepath = f"data/import/{filename}"
            try:
                persons, skipped = DataImporter.import_csv(filepath)
                # 过滤编号重复的
                added = 0
                for p in persons:
                    if not self.service.person_id_check(p._person_id):
                        self.service.add_person(p)
                        added += 1
                    else:
                        skipped += 1

                msg = f"导入完成：成功 {added} 条"
                if skipped > 0:
                    msg += f"，跳过 {skipped} 条（重复或格式错误）"
                self.app.notify(msg, title="导入完成", severity="information", timeout=4)

                if self.on_done:
                    self.on_done()
                self.app.pop_screen()
            except FileNotFoundError:
                self.app.notify(f"未找到文件：{filepath}", title="导入失败", severity="error", timeout=3)
            except Exception as e:
                self.app.notify(f"导入失败：{e}", title="错误", severity="error", timeout=3)

        elif event.button.id == "btn-cancel":
            self.app.pop_screen()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """输入框按Enter触发导入"""
        if event.input.id == "import-filename":
            # 模拟点击导入按钮
            self.query_one("#btn-import", Button).press()

    def action_cancel(self) -> None:
        self.app.pop_screen()