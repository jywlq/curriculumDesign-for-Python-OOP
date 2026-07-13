# 人员详细信息页面设计文档

## 任务

设计一个"人员详细信息"页面，在显示或筛选列表中点击某条记录时，弹出或跳转到该人员的详细信息页面。

## 数据模型

人员有 4 种类型，每种类型的字段如下：

### 公共字段（所有类型都有）

| 字段名 | 属性名 | 说明 |
|--------|--------|------|
| 编号 | `_person_id` | 格式：T/E/A/TA + 三位数字 |
| 姓名 | `_person_name` | 2-20 个字符 |
| 性别 | `_person_gender` | 男/女 |
| 年龄 | `_person_age` | 1-150 的整数 |
| 类型 | `type(p).__name__` | Teacher/Experimenter/Admin/TeacherAdmin |

### 教师（Teacher）特有字段

| 字段名 | 属性名 |
|--------|--------|
| 所在系部 | `_department` |
| 专业 | `_major` |
| 职称 | `_professional_title` |

### 实验员（Experimenter）特有字段

| 字段名 | 属性名 |
|--------|--------|
| 所在实验室 | `_laboratory` |
| 职务 | `_duties` |

### 行政人员（Admin）特有字段

| 字段名 | 属性名 |
|--------|--------|
| 政治面貌 | `_political_affiliation` |
| 职称 | `_professional_title` |

### 教师兼行政（TeacherAdmin）特有字段

| 字段名 | 属性名 |
|--------|--------|
| 所在系部 | `_department` |
| 专业 | `_major` |
| 职称 | `_professional_title` |
| 政治面貌 | `_political_affiliation` |

## 页面需求

### 布局

采用卡片式布局，参考原项目的统计页面风格：

```
┌─────────────────────────────────────────────┐
│  👤 人员详细信息                              │
├─────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐           │
│  │ 编号        │  │ T001        │           │
│  ├─────────────┤  ├─────────────┤           │
│  │ 姓名        │  │ 张三        │           │
│  ├─────────────┤  ├─────────────┤           │
│  │ 性别        │  │ 男          │           │
│  ├─────────────┤  ├─────────────┤           │
│  │ 年龄        │  │ 30          │           │
│  ├─────────────┤  ├─────────────┤           │
│  │ 类型        │  │ 教师        │           │
│  ├─────────────┤  ├─────────────┤           │
│  │ 所在系部    │  │ 计算机系    │  ← 教师/教师兼行政 |
│  ├─────────────┤  ├─────────────┤           │
│  │ 专业        │  │ 软件工程    │  ← 教师/教师兼行政 |
│  ├─────────────┤  ├─────────────┤           │
│  │ 职称        │  │ 副教授      │  ← 教师/行政/教师兼行政 |
│  └─────────────┘  └─────────────┘           │
├─────────────────────────────────────────────┤
│  [返回] 按钮                                  │
└─────────────────────────────────────────────┘
```

### 交互

1. 在显示人员列表或查询结果列表中，点击某条记录
2. 弹出或跳转到详细信息页面
3. 页面显示该人员的所有字段（公共 + 特有）
4. 底部有"返回"按钮，点击后回到列表

## 接口要求

### 1. 页面组件

```python
class PersonDetailPage(VerticalScroll):
    """人员详细信息页面"""
    
    def __init__(self, person: BaseClass):
        """接收一个人员对象"""
        self.person = person
        super().__init__()
```

### 2. 人员类型映射

```python
# 类型中文名映射
TYPE_MAP = {
    "Teacher": "教师",
    "Experimenter": "实验员",
    "Admin": "行政人员",
    "TeacherAdmin": "教师兼行政",
}
```

### 3. 字段获取

通过 `isinstance()` 判断类型，获取对应字段：

```python
def get_extra_fields(person) -> list:
    """获取人员的特有字段列表，返回 [(字段名, 值), ...]"""
    fields = []
    if isinstance(person, TeacherAdmin):  # 先判断子类
        fields = [("所在系部", person._department), ("专业", person._major), 
                  ("职称", person._professional_title), ("政治面貌", person._political_affiliation)]
    elif isinstance(person, Teacher):
        fields = [("所在系部", person._department), ("专业", person._major), 
                  ("职称", person._professional_title)]
    elif isinstance(person, Experimenter):
        fields = [("所在实验室", person._laboratory), ("职务", person._duties)]
    elif isinstance(person, Admin):
        fields = [("政治面貌", person._political_affiliation), ("职称", person._professional_title)]
    return fields
```

### 4. 页面切换

使用 Textual 的 Screen 机制：

```python
# 打开详情页
self.app.push_screen(PersonDetailPage(person))

# 关闭详情页（返回）
self.app.pop_screen()
```

## 需要修改的文件

1. **新建** `src/ui/tui_app.py` 中添加 `PersonDetailPage` 类
2. **修改** `render_person_list_page()` 函数，让列表行可点击
3. **修改** `MainContent.on_menu_selected()`，处理点击事件

## 注意事项

1. 继承 `VerticalScroll` 以支持滚动
2. 使用 `rich.panel.Panel` 和 `rich.table.Table` 渲染内容（和原项目风格一致）
3. 列表的行点击事件用 Textual 的 `DataTable.RowSelected` 或自定义点击处理
4. 保持与原项目 cmd_ui.py 的风格一致
