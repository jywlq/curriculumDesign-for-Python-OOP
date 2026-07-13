"""
人员详情弹窗组件

简洁的居中弹窗，点击列表行时弹出显示人员核心信息。
继承 Screen，支持 Enter / Escape 关闭，也可点击返回按钮关闭。
"""
from textual.app import ComposeResult, Screen
from textual.widgets import Static, Button, Label
from textual.containers import Container, Vertical, Horizontal
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich import box


# ──────────────────────────────────────────────
# 辅助函数：构建详情内容的 rich Panel
# ──────────────────────────────────────────────

def render_person_detail_modal(person) -> Panel:
    """渲染人员详情弹窗的内容面板（紧凑一行式）

    布局：
    ┌─────────────────────────────────────┐
    │  👨‍🏫 张三（T001）  教师              │
    ├─────────────────────────────────────┤
    │  男 | 30岁 | 计算机系 | 软件工程     │
    └─────────────────────────────────────┘
    """
    person_type = type(person).__name__

    # 类型 → (图标, 中文名, 主题色)
    type_info = {
        "Teacher":      ("👨‍🏫", "教师",        "cyan"),
        "Experimenter": ("🔬", "实验员",      "green"),
        "Admin":        ("💼", "行政人员",    "magenta"),
        "TeacherAdmin": ("👨‍💼", "教师兼行政",  "yellow"),
    }
    icon, type_name, accent = type_info.get(person_type, ("👤", "未知", "white"))

    # ── 第一行：姓名 + 编号 + 类型 ──
    title_line = Text()
    title_line.append(f"  {icon}  ", style=f"bold {accent}")
    title_line.append(person._person_name, style="bold white")
    title_line.append(f"（{person._person_id}）", style="dim")
    title_line.append("  ")
    title_line.append(type_name, style=f"bold {accent}")

    # ── 第二行：核心字段，用 | 分隔 ──
    info_parts = []

    # 性别 + 年龄（公共）
    gender_icon = "♂ 男" if person._person_gender == "男" else "♀ 女"
    info_parts.append(gender_icon)
    info_parts.append(f"{person._person_age} 岁")

    # 特有字段（根据类型）
    if person_type == "Teacher":
        info_parts.append(person._department)
        info_parts.append(person._major)
        info_parts.append(person._professional_title)
    elif person_type == "Experimenter":
        info_parts.append(person._laboratory)
        info_parts.append(person._duties)
    elif person_type == "Admin":
        info_parts.append(person._political_affiliation)
        info_parts.append(person._professional_title)
    elif person_type == "TeacherAdmin":
        info_parts.append(person._department)
        info_parts.append(person._major)
        info_parts.append(person._professional_title)
        info_parts.append(person._political_affiliation)

    info_line = Text("  " + "  |  ".join(info_parts) + "  ", style="white")

    # ── 组装 ──
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_row(title_line)
    grid.add_row(Text("  " + "─" * 40, style=accent + " 50%"))
    grid.add_row(info_line)

    return Panel(
        grid,
        border_style=accent,
        padding=(1, 0),
        box=box.ROUNDED,
    )


# ──────────────────────────────────────────────
# 弹窗 Screen
# ──────────────────────────────────────────────

class PersonDetailScreen(Screen):
    """人员详情弹窗 - 居中小弹窗

    用法：
        app.push_screen(PersonDetailScreen(person))

    关闭方式：
        - 点击「返回」按钮
        - 按 Enter
        - 按 Escape
    """

    BINDINGS = [
        ("enter", "close", "关闭"),
        ("escape", "close", "关闭"),
    ]

    DEFAULT_CSS = """
    PersonDetailScreen {
        align: center middle;
        background: black 30%;
    }

    #modal-container {
        width: 50%;
        min-width: 50;
        height: auto;
        background: $surface;
        border: round $primary;
        padding: 0;
    }

    #modal-content {
        height: auto;
        padding: 0;
    }
    #modal-content > Static {
        height: auto;
    }

    #modal-footer {
        height: 4;
        padding: 0 2;
        background: $surface-darken-1;
        border-top: solid $primary 20%;
        align: center middle;
    }

    #close-btn {
        width: 16;
    }
    """

    def __init__(self, person):
        self.person = person
        super().__init__()

    def compose(self) -> ComposeResult:
        with Container(id="modal-container"):
            with Vertical(id="modal-content"):
                yield Static(render_person_detail_modal(self.person))
            with Horizontal(id="modal-footer"):
                yield Button("✓ 返回", variant="primary", id="close-btn")

    def action_close(self) -> None:
        """关闭弹窗"""
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """点击按钮关闭"""
        if event.button.id == "close-btn":
            self.app.pop_screen()
