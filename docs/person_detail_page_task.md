# 人员详细信息页面设计任务

## 你需要做的

设计一个 TUI 页面组件 `PersonDetailPage`，显示某个人员的详细信息。

## 数据结构

person 对象有以下属性（用 `person.属性名` 访问）：

```python
# 公共字段（所有人都有）
person._person_id      # 编号，如 T001
person._person_name    # 姓名
person._person_gender  # 性别
person._person_age     # 年龄

# 通过 type(person).__name__ 获取类型，可能是：
# "Teacher"        教师
# "Experimenter"   实验员
# "Admin"          行政人员
# "TeacherAdmin"   教师兼行政

# 教师特有（Teacher / TeacherAdmin）
person._department           # 所在系部
person._major                # 专业
person._professional_title   # 职称

# 实验员特有（Experimenter）
person._laboratory   # 所在实验室
person._duties       # 职务

# 行政人员特有（Admin / TeacherAdmin）
person._political_affiliation  # 政治面貌
```

## 页面要求

1. 用 rich 的 Panel + Table 渲染，不要用 DataTable
2. 先显示公共字段，再根据类型显示特有字段
3. 底部有"返回"按钮
4. 支持滚动（继承 VerticalScroll）

## 你需要提供的代码

只需要提供 `PersonDetailPage` 这个类的完整代码（compose + CSS），不需要处理事件和 Screen 切换。

```python
class PersonDetailPage(VerticalScroll):
    def __init__(self, person):
        self.person = person
        super().__init__()
    
    def compose(self) -> ComposeResult:
        # 你的设计
        pass
```
