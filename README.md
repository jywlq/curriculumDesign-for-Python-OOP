# 高校人员信息管理系统

基于 Python 面向对象设计的高校人员信息管理系统，支持教师、实验员、行政人员、教师兼行政人员四类人员的全生命周期管理。

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
| 添加人员 | 支持四类人员，编号唯一性校验，支持连续添加 | ✅ |
| 查询人员 | 按编号/姓名前缀筛选，支持组合筛选 | ✅ |
| 显示人员 | 显示所有人员记录，每条一行 | ✅ |
| 编辑人员 | 筛选后选择序号修改，保持编号唯一性 | ✅ |
| 删除人员 | 筛选后选择序号删除，需确认(y/n) | ✅ |
| 统计人员 | 按类型统计人数，统计男/女员工数量 | ✅ |
| 保存功能 | 将人员记录存入 JSON 文件 | ✅ |
| 读取功能 | 从文件读取人员信息到系统 | ✅ |
| TUI 界面 | 基于 Textual 的终端图形界面，支持鼠标点击 | ✅ |

## 人员类型与字段

| 类型 | 编号前缀 | 特有字段 |
|------|----------|----------|
| 教师 | T | 所在系部、专业、职称 |
| 实验员 | E | 所在实验室、职务 |
| 行政人员 | A | 政治面貌、职称 |
| 教师兼行政 | TA | 所在系部、专业、职称、政治面貌 |

## 运行方式

```bash
# TUI 界面（默认，基于 Textual）
python main.py

# CLI 界面（传统命令行）
python main.py --cli
```

### 依赖安装

```bash
pip install textual rich
```

## 项目结构

```
├── main.py                     # 程序入口
├── src/
│   ├── models/                 # 数据模型层
│   │   ├── base.py             # BaseClass 基类
│   │   ├── teacher.py          # Teacher 教师类
│   │   ├── experimenter.py     # Experimenter 实验员类
│   │   ├── admin.py            # Admin 行政人员类
│   │   └── teacher_admin.py    # TeacherAdmin 教师兼行政（多重继承）
│   ├── services/               # 业务逻辑层
│   │   └── person_service.py   # PersonService（增删改查 + 持久化）
│   └── ui/                     # 用户界面层
│       ├── constants.py        # 统一常量（TYPE_META）
│       ├── widgets.py          # 通用 UI 组件（RichPanelPage）
│       ├── tui_app.py          # TUI 主应用
│       ├── person_list_page.py # TUI 人员列表页
│       ├── person_detail_page.py # TUI 详情弹窗
│       ├── cmd_ui.py           # CLI 主界面
│       ├── collector.py        # 信息收集器
│       ├── filter.py           # 筛选器
│       └── exceptions.py       # ReturnBack 异常
├── data/
│   ├── person.json             # 人员数据（JSON 格式）
│   └── config.json             # 配置文件
└── docs/                       # 设计文档
```

## 三层架构

```
┌─────────────────────────────────────────────────────┐
│                   UI 层（用户界面）                   │
│   cmd_ui.py (CLI)  │  tui_app.py (TUI)              │
├─────────────────────────────────────────────────────┤
│                Service 层（业务逻辑）                 │
│              person_service.py                       │
│    增删改查 │ JSON 持久化 │ 编号校验 │ 统计           │
├─────────────────────────────────────────────────────┤
│                 Model 层（数据模型）                  │
│  BaseClass │ Teacher │ Experimenter │ Admin │ ...   │
│    属性定义 │ 序列化 │ 多态展示字段                   │
└─────────────────────────────────────────────────────┘
```

## 关键设计点

### 多重继承处理

`TeacherAdmin` 同时继承 `Teacher` 和 `Admin`，通过直接调用 `BaseClass.__init__()` 绕开 MRO 问题：

```python
class TeacherAdmin(Teacher, Admin):
    def __init__(self, ...):
        # 直接调用基类构造函数，避免多重继承的 MRO 问题
        BaseClass.__init__(self, person_id, person_name, person_gender, person_age)
        self._department = department
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

人员类型元数据（图标/名称/颜色/CSS类/统计key）统一定义在 `constants.py` 的 `TYPE_META` 中，消除硬编码：

```python
TYPE_META = {
    "Teacher":      ("👨‍🏫", "教师",       "cyan",    "--teacher",       "教师"),
    "Experimenter": ("🔬", "实验员",     "green",   "--experimenter",  "实验员"),
    ...
}
```

## 测试验证

```bash
# 导入测试
python -c "from src.ui.tui_app import PersonTuiApp; print('OK')"

# Model 层多态测试
python -c "
from src.models.teacher import Teacher
t = Teacher('T001', '张三', '男', '30', '计算机系', '软件工程', '教授')
print(t.get_display_fields(brief=True))   # ['计算机系', '教授']
print(t.get_display_fields(brief=False))  # ['计算机系', '软件工程', '教授']
"
```

## 创新设计

### TUI 终端图形界面

基于 Textual 库实现的现代化终端界面，特性包括：

- **左右布局**：左侧导航菜单（带图标分组），右侧内容区
- **鼠标交互**：支持点击菜单、点击列表行查看详情弹窗
- **键盘快捷键**：`q` 退出、`s` 保存、`r` 刷新
- **响应式设计**：自适应终端大小
- **丰富样式**：类型色条、斑马纹、hover 效果、选中高亮

### 代码质量优化

- **统一常量**：消除硬编码，便于维护
- **多态设计**：Model 层 `get_display_fields()` 方法，UI 层无需 if-elif 判断类型
- **通用组件**：`RichPanelPage` 基类复用页面结构
- **异常处理**：TUI 层完善的 try/except 保护

## 开发指南

### 添加新人员类型

1. `src/models/` 创建新类，继承 `BaseClass`
2. 实现 `get_fields()`、`to_dict()`、`from_dict()`、`get_display_fields()`
3. `src/services/person_service.py` 的 class_map 注册
4. `src/ui/constants.py` 的 TYPE_META 添加条目
5. `src/ui/collector.py` 的 PERSON_TYPE 添加映射

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 类名 | PascalCase | `BaseClass`、`PersonService` |
| 方法/变量 | snake_case | `person_id`、`get_display_fields` |
| 常量 | UPPER_CASE | `TYPE_META`、`CONFIG_FILE` |
| 私有属性 | 下划线前缀 | `_person_id`、`_department` |

## 课程设计对应

| 课程目标 | 对应实现 |
|----------|----------|
| 课程目标1：面向对象设计 | 抽象（BaseClass）、封装（私有属性）、继承（4类人员）、多态（get_fields 等） |
| 课程目标2：系统分析与设计 | 三层架构（Model-Service-UI）、模块化设计、JSON 持久化 |
| 课程目标3：软件工程实践 | 完整功能实现、TUI 创新界面、代码规范、测试验证 |
