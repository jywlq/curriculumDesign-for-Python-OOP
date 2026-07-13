# 人员详情弹窗设计任务

## 需求

把现在的全屏详情页改成一个小弹窗，点击列表行时弹出，显示该人员的核心信息。

## 弹窗要求

### 外观

- 不是全屏，是一个居中的小弹窗（宽度约占屏幕 50%）
- 有圆角边框
- 半透明背景遮罩（可选）

### 内容

简洁显示，一两行搞定：

```
┌─────────────────────────────────────┐
│  👨‍🏫 张三（T001）  教师              │
├─────────────────────────────────────┤
│  男 | 30岁 | 计算机系 | 软件工程     │
├─────────────────────────────────────┤
│  [返回]                             │
└─────────────────────────────────────┘
```

根据类型不同显示不同特有字段：
- 教师：系部、专业、职称
- 实验员：实验室、职务
- 行政：政治面貌、职称
- 教师兼行政：系部、专业、职称、政治面貌

### 交互

- 点击返回按钮关闭
- 按 Enter 或 Escape 关闭

## 接口

```python
class PersonDetailScreen(Screen):
    """人员详情弹窗"""
    
    def __init__(self, person):
        self.person = person
        super().__init__()
    
    def compose(self) -> ComposeResult:
        # 你的设计
        pass
```

person 对象的属性：
- `_person_id` — 编号
- `_person_name` — 姓名
- `_person_gender` — 性别
- `_person_age` — 年龄
- 教师：`_department`, `_major`, `_professional_title`
- 实验员：`_laboratory`, `_duties`
- 行政：`_political_affiliation`, `_professional_title`

## 文件位置

写到 `src/ui/person_detail_page.py`，替换掉原来的 PersonDetailPage 类。
