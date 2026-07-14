# 高校人员信息管理系统

基于 Python 面向对象设计的高校人员信息管理系统，支持教师、实验员、行政人员、教师兼行政人员四类人员的全生命周期管理。提供 CLI 和 TUI 双界面。

## 快速开始

```bash
# 安装依赖
pip install textual rich

# TUI 界面（默认，基于 Textual，支持鼠标交互）
python main.py

# CLI 界面（传统命令行）
python main.py --cli
```

## 面向对象设计特性

### 抽象
`BaseClass` 作为人员基类，定义公共属性（编号、姓名、性别、年龄）和通用接口（`get_fields()`、`to_dict()`、`from_dict()`、`get_display_fields()`），为所有人员类型提供统一的抽象层。

### 封装
所有人员属性使用下划线前缀命名（`_person_id`、`_person_name` 等），通过序列化方法（`to_dict()` / `from_dict()`）和展示方法（`get_display_fields()`）提供受控的外部访问接口。

### 继承
四类人员继承体系：

```
BaseClass（基类）
├── Teacher（教师）
├── Experimenter（实验员）
├── Admin（行政人员）
└── TeacherAdmin（教师兼行政人员）← 多重继承
```

### 多态
每个子类独立实现以下方法，实现统一接口下的差异化行为：

| 方法 | 用途 |
|------|------|
| `get_fields()` | 返回特有字段定义（用于输入表单） |
| `get_display_fields(brief)` | 返回展示字段（用于列表/详情页） |
| `to_dict()` | 序列化为 JSON 字典 |
| `from_dict(d)` | 从字典反序列化 |

## 功能清单

| 功能 | 说明 | 状态 |
|------|------|------|
| 添加人员 | 支持四类人员，编号唯一性校验，动态表单 | ✅ |
| 查询人员 | 按编号/姓名前缀组合筛选，支持交集 | ✅ |
| 显示人员 | 精美列表展示，类型色条、斑马纹、hover 高亮 | ✅ |
| 编辑人员 | 筛选后选择修改，弹窗表单，编号唯一性校验 | ✅ |
| 删除人员 | 筛选后选择删除，二次确认弹窗 | ✅ |
| 统计人员 | 按类型/性别统计，可视化进度条 | ✅ |
| 保存/读取 | JSON 持久化，自动/手动保存模式 | ✅ |
| CSV 导出 | 导出全部人员数据为 CSV 文件 | ✅ |
| CSV 导入 | 批量导入 CSV 文件，自动去重 | ✅ |
| TUI 界面 | 基于 Textual 的终端图形界面，鼠标/键盘双操作 | ✅ |
| CLI 界面 | 传统命令行交互界面，完整功能 | ✅ |

## 人员类型与字段

| 类型 | 编号前缀 | 公共字段 | 特有字段 |
|------|----------|----------|----------|
| 教师 | T | 编号、姓名、性别、年龄 | 所在系部、专业、职称 |
| 实验员 | E | 编号、姓名、性别、年龄 | 所在实验室、职务 |
| 行政人员 | A | 编号、姓名、性别、年龄 | 政治面貌、职称 |
| 教师兼行政 | TA | 编号、姓名、性别、年龄 | 所在系部、专业、职称、政治面貌 |

## 项目结构

```
├── main.py                          # 程序入口
├── README.md                        # 项目说明
├── AGENTS.md                        # 开发指南
├── src/
│   ├── __init__.py
│   ├── models/                      # 数据模型层
│   │   ├── __init__.py
│   │   ├── base.py                  # BaseClass 基类
│   │   ├── teacher.py               # Teacher 教师类
│   │   ├── experimenter.py          # Experimenter 实验员类
│   │   ├── admin.py                 # Admin 行政人员类
│   │   └── teacher_admin.py         # TeacherAdmin 教师兼行政（多重继承）
│   ├── services/                    # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── person_service.py        # PersonService（增删改查 + JSON 持久化 + 统计）
│   │   ├── config.py                # 配置读写（自动保存开关）
│   │   ├── csv_export.py            # CSV 导出
│   │   └── csv_import.py            # CSV 导入
│   └── ui/                          # 用户界面层
│       ├── __init__.py
│       ├── constants.py             # 统一常量（TYPE_META、ID_PATTERN、STAT_* 等）
│       ├── cmd_ui.py                # CLI 主界面
│       ├── collector.py             # 信息收集器（CLI 用）
│       ├── filter.py                # 筛选器（CLI + TUI 共用）
│       ├── exceptions.py            # ReturnBack 异常
│       └── tui/                     # TUI 界面模块
│           ├── __init__.py
│           ├── tui_app.py           # TUI 主应用（PersonTuiApp）
│           ├── widgets.py           # 通用组件（RichPanelPage、DataChanged）
│           ├── confirm_screen.py    # 通用确认弹窗
│           ├── person_list_page.py  # 人员列表页
│           ├── person_detail_page.py# 人员详情弹窗
│           ├── person_filter_page.py# 人员筛选页
│           ├── person_edit_screen.py# 人员编辑弹窗
│           ├── person_add_screen.py # 人员添加弹窗
│           ├── person_form_screen.py# 人员表单基类（Add/Edit 继承）
│           ├── person_delete_confirm.py # 删除确认弹窗
│           └── csv_import_screen.py # CSV 导入引导页
├── data/
│   ├── person.json                  # 人员数据（JSON 格式）
│   ├── config.json                  # 配置文件
│   ├── person.csv                   # CSV 导出文件
│   └── import/                      # CSV 导入目录
│       └── test.csv                 # 示例 CSV 文件
└── docs/
    ├── class-diagram.md             # UML 类图
    └── change.md                    # 改动记录
```

## 三层架构

```
┌─────────────────────────────────────────────────────────┐
│                    UI 层（用户界面）                      │
│   cmd_ui.py (CLI)  │  tui/ (TUI，基于 Textual)           │
├─────────────────────────────────────────────────────────┤
│                 Service 层（业务逻辑）                    │
│   person_service.py │ csv_export.py │ csv_import.py      │
│   增删改查 │ JSON 持久化 │ 编号校验 │ 统计 │ 导入导出     │
├─────────────────────────────────────────────────────────┤
│                  Model 层（数据模型）                     │
│   BaseClass │ Teacher │ Experimenter │ Admin │ ...      │
│   属性定义 │ 序列化 │ 多态展示字段                        │
└─────────────────────────────────────────────────────────┘
```

## 关键设计点

### 多重继承处理
`TeacherAdmin` 同时继承 `Teacher` 和 `Admin`，通过直接调用 `BaseClass.__init__()` 绕开 MRO 问题：

```python
class TeacherAdmin(Teacher, Admin):
    def __init__(self, ...):
        BaseClass.__init__(self, person_id, person_name, person_gender, person_age)
        # ...
```

### 序列化机制
JSON 中使用 `__class__` 字段标识类型，加载时通过 class_map 映射还原：

```json
{
    "__class__": "Teacher",
    "personID": "T001",
    "personName": "张三",
    "department": "计算机系",
    ...
}
```

### 统一常量管理
人员类型元数据、统计键、编号正则等统一定义在 `constants.py`，`STAT_*` 常量源头在 `person_service.py`（service 层），`constants.py` 从 service 导入：

```python
TYPE_META = {
    "Teacher":      ("👨‍🏫", "教师",       "cyan",    "--teacher",       "教师"),
    "Experimenter": ("🔬", "实验员",     "green",   "--experimenter",  "实验员"),
    # ...
}
```

### 数据去重
`load()` 和 `find_person()` 双端按 `_person_id` 去重，确保数据源和筛选结果均无重复。

## TUI 界面特性

- **左右布局**：左侧导航菜单（带图标分组），右侧内容区
- **鼠标交互**：支持点击菜单、点击列表行查看详情弹窗
- **键盘快捷键**：`q` 退出、`s` 保存、`r` 刷新，`↑↓` 导航，`Enter` 选中
- **响应式设计**：自适应终端大小
- **丰富样式**：类型色条、斑马纹、hover 效果、选中高亮
- **弹窗组件**：添加/编辑/删除/确认均使用居中弹窗

## 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 类名 | PascalCase | `BaseClass`、`PersonService` |
| 方法/变量 | snake_case | `person_id`、`get_display_fields` |
| 常量 | UPPER_CASE | `TYPE_META`、`STAT_TOTAL` |
| 私有属性 | 下划线前缀 | `_person_id`、`_department` |

## 文档

- [UML 类图](docs/class-diagram.md)
- [改动记录](docs/change.md)
- [开发指南](AGENTS.md)