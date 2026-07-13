"""
人员详情页面组件

独立的 PersonDetailPage 组件，用于显示单个人员的详细信息。
使用 rich 的 Panel + Table 渲染，继承 VerticalScroll 支持滚动。
"""
from textual.app import ComposeResult
from textual.widgets import Static, Button
from textual.containers import Container, VerticalScroll
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich import box


def render_person_detail_page(person) -> Panel:
    """渲染人员详情页面板

    Args:
        person: 人员对象（Teacher / Experimenter / Admin / TeacherAdmin）

    Returns:
        rich Panel 对象
    """
    person_type = type(person).__name__

    # 类型名称、图标、主题色映射
    type_info = {
        "Teacher":      ("👨‍🏫", "教师",        "cyan"),
        "Experimenter": ("🔬", "实验员",      "green"),
        "Admin":        ("💼", "行政人员",    "magenta"),
        "TeacherAdmin": ("👨‍💼", "教师兼行政",  "yellow"),
    }
    icon, type_name, accent_color = type_info.get(person_type, ("👤", "未知", "white"))

    # 性别图标
    gender_icon = "♂ 男" if person._person_gender == "男" else "♀ 女"

    # ── 顶部信息卡片（姓名 + 编号 + 类型标签）──
    header_grid = Table.grid(expand=True)
    header_grid.add_column(justify="left", ratio=2)
    header_grid.add_column(justify="right", ratio=1)

    name_line = Text(f"\n  {icon}  {person._person_name}\n", style=f"bold {accent_color} size 5")
    id_line = Text(f"  编号：{person._person_id}    |    {type_name}\n", style="dim")
    header_grid.add_row(name_line + id_line, Text(""))

    header_panel = Panel(
        header_grid,
        border_style=accent_color,
        padding=(0, 1),
    )

    # ── 公共字段表格 ──
    common_table = Table(
        show_header=False,
        expand=True,
        box=box.SIMPLE_HEAVY,
        padding=(0, 2),
    )
    common_table.add_column("label", justify="right", style="bold cyan", width=12)
    common_table.add_column("value", justify="left", style="white")

    common_table.add_row("姓    名", person._person_name)
    common_table.add_row("编    号", person._person_id)
    common_table.add_row("性    别", gender_icon)
    common_table.add_row("年    龄", f"{person._person_age} 岁")

    common_panel = Panel(
        common_table,
        title="📌 基本信息",
        border_style="cyan",
        padding=(1, 1),
    )

    # ── 特有字段表格（根据类型动态生成）──
    extra_table = Table(
        show_header=False,
        expand=True,
        box=box.SIMPLE_HEAVY,
        padding=(0, 2),
    )
    extra_table.add_column("label", justify="right", style=f"bold {accent_color}", width=12)
    extra_table.add_column("value", justify="left", style="white")

    if person_type in ("Teacher", "TeacherAdmin"):
        extra_table.add_row("所在系部", person._department)
        extra_table.add_row("专    业", person._major)
        extra_table.add_row("职    称", person._professional_title)

    if person_type == "Experimenter":
        extra_table.add_row("所在实验室", person._laboratory)
        extra_table.add_row("职    务", person._duties)

    if person_type in ("Admin", "TeacherAdmin"):
        if person_type == "Admin":
            extra_table.add_row("政治面貌", person._political_affiliation)
            extra_table.add_row("职    称", person._professional_title)
        else:
            # TeacherAdmin 的职称已在教师部分显示，这里只加政治面貌
            extra_table.add_row("政治面貌", person._political_affiliation)

    extra_title = "🏷️  教师信息" if person_type == "Teacher" else \
                  "🏷️  实验员信息" if person_type == "Experimenter" else \
                  "🏷️  行政信息" if person_type == "Admin" else \
                  "🏷️  教师兼行政信息"

    extra_panel = Panel(
        extra_table,
        title=extra_title,
        border_style=accent_color,
        padding=(1, 1),
    )

    # ── 组合主面板 ──
    main_content = Table.grid(expand=True)
    main_content.add_column()

    main_content.add_row(Text(""))
    main_content.add_row(header_panel)
    main_content.add_row(Text("\n"))
    main_content.add_row(common_panel)
    main_content.add_row(Text("\n"))
    main_content.add_row(extra_panel)
    main_content.add_row(Text(""))

    return Panel(
        main_content,
        title=f"{icon} 人员详情",
        border_style=accent_color,
        padding=(1, 2),
    )


class PersonDetailPage(VerticalScroll):
    """人员详情页 - 显示单个人员的详细信息

    用法：
        page = PersonDetailPage(person)
        # 底部有一个返回按钮，id 为 detail-back-btn 内的按钮
    """

    DEFAULT_CSS = """
    PersonDetailPage {
        height: 100%;
        padding: 1 2;
    }
    PersonDetailPage > Static {
        height: auto;
    }
    PersonDetailPage > #detail-back-btn {
        margin-top: 1;
        width: 100%;
        height: 3;
        align: center middle;
    }
    PersonDetailPage > #detail-back-btn > Button {
        width: 20;
    }
    """

    def __init__(self, person):
        self.person = person
        super().__init__()

    def compose(self) -> ComposeResult:
        panel = render_person_detail_page(self.person)
        yield Static(panel)
        with Container(id="detail-back-btn"):
            yield Button("← 返回列表", variant="primary")
