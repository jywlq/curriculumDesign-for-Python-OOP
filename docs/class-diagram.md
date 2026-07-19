# UML 类图

> 高校人员信息管理系统 — 完整类图

## Model 层（数据模型）

![UML类图](class-diagram.png)

### 继承关系说明

| 类 | 中文名 | 继承方式 | 特有字段 |
|------|------|------|------|
| `BaseClass` | 人员基类 | 抽象基类 | 编号、姓名、性别、年龄（公共字段） |
| `Teacher` | 教师 | 单继承 BaseClass | 所在系部、专业、职称 |
| `Experimenter` | 实验员 | 单继承 BaseClass | 所在实验室、职务 |
| `Admin` | 行政人员 | 单继承 BaseClass | 政治面貌、职称 |
| `TeacherAdmin` | 教师兼行政人员 | 多重继承 Teacher + Admin | 所在系部、专业、职称、政治面貌 |

### 多态方法

每个子类均覆写以下 4 个方法，通过统一接口实现差异化行为：

| 方法 | 用途 |
|------|------|
| `get_fields()` | 返回特有字段定义（用于输入表单） |
| `get_display_fields(brief)` | 返回展示字段值（brief=True 用于列表行，brief=False 用于详情页） |
| `to_dict()` | 序列化为 JSON 字典 |
| `from_dict(d)` | 从字典反序列化还原对象 |

---

## 关键代码示例

### 1. BaseClass（人员基类）— `src/models/base.py`

```python
class BaseClass:
    """人员信息基类，封装四个公共属性，提供模板方法供子类覆写"""

    def __init__(self, person_id: str, person_name: str, person_gender: str, person_age: str):
        self._person_id = person_id
        self._person_name = person_name
        self._person_gender = person_gender
        self._person_age = person_age

    @classmethod
    def get_fields(cls) -> List[Tuple[str, str]]:
        """返回子类特有字段列表，基类返回空列表（模板方法）"""
        return []

    def get_display_fields(self, brief: bool = False) -> list:
        """返回展示字段值，brief=True 用于列表行，brief=False 用于详情页"""
        return []

    def to_dict(self) -> dict:
        """序列化为字典，__class__ 字段用于反序列化时还原类型"""
        return {
            '__class__': 'BaseClass',
            'personID': self._person_id,
            'personName': self._person_name,
            'personGender': self._person_gender,
            'personAge': self._person_age
        }

    @classmethod
    def from_dict(cls, d: dict) -> 'BaseClass':
        """从字典反序列化"""
        return cls(d['personID'], d['personName'], d['personGender'], str(d['personAge']))
```

### 2. TeacherAdmin（多重继承）— `src/models/teacher_admin.py`

```python
class TeacherAdmin(Teacher, Admin):
    """教师兼行政人员类（多重继承）
    同时拥有教师（系部、专业、职称）和行政人员（政治面貌）的属性。
    构造函数直接调用 BaseClass.__init__() 而非 super()，绕开 MRO 问题。"""

    def __init__(self, person_id, person_name, person_gender, person_age,
                 department, major, professional_title, political_affiliation):
        # 直接调用基类构造函数，避免多重继承的 MRO 问题
        BaseClass.__init__(self, person_id, person_name, person_gender, person_age)
        self._department = department
        self._major = major
        self._professional_title = professional_title
        self._political_affiliation = political_affiliation

    @classmethod
    def get_fields(cls):
        return [("department", "所在系部"), ("major", "专业"),
                ("professionalTitle", "职称"), ("politicalAffiliation", "政治面貌")]

    def get_display_fields(self, brief: bool = False) -> list:
        if brief:
            return [self._department, self._political_affiliation]
        return [self._department, self._major,
                self._professional_title, self._political_affiliation]

    @classmethod
    def from_dict(cls, d: dict):
        return cls(d['personID'], d['personName'], d['personGender'], str(d['personAge']),
                   d.get('department', ''), d.get('major', ''),
                   d.get('professionalTitle', ''), d.get('politicalAffiliation', ''))

    def to_dict(self):
        data = BaseClass.to_dict(self)
        data.update({
            '__class__': 'TeacherAdmin',
            'politicalAffiliation': self._political_affiliation
        })
        return data
```

### 3. PersonService（核心业务逻辑）— `src/services/person_service.py`

```python
class PersonService:
    """人员服务类，封装增删改查和文件读写"""

    def __init__(self):
        self.person_list = []  # 人员列表，存储所有人员对象

    def person_id_check(self, person_id: str) -> bool:
        """检查编号是否已存在"""
        for p in self.person_list:
            if p._person_id == person_id:
                return True
        return False

    def add_person(self, person) -> bool:
        """添加人员"""
        self.person_list.append(person)
        return True

    def find_person(self, person_id: str = '', person_name: str = '') -> List:
        """前缀匹配查询，按编号/姓名组合筛选，AND 逻辑，结果去重"""
        if not person_id and not person_name:
            return self.person_list.copy()
        result = []
        seen = set()
        for p in self.person_list:
            if p._person_id.startswith(person_id) and p._person_name.startswith(person_name):
                if p._person_id not in seen:
                    seen.add(p._person_id)
                    result.append(p)
        return result

    def update_person(self, person_id: str, person) -> bool:
        """修改人员，双重校验：新编号不冲突 + 旧编号必须存在"""
        if self.person_id_check(person._person_id) and person_id != person._person_id:
            return False
        for i, p in enumerate(self.person_list):
            if p._person_id == person_id:
                self.person_list[i] = person
                return True
        return False

    def delete_person(self, person_id: str) -> bool:
        """按编号删除人员"""
        for p in self.person_list:
            if p._person_id == person_id:
                self.person_list.remove(p)
                return True
        return False

    def get_person_statistics(self) -> Dict[str, int]:
        """统计总人数、性别分布和各类人员数量"""
        res = {
            STAT_TOTAL: len(self.person_list), STAT_MALE: 0, STAT_FEMALE: 0,
            STAT_TEACHER: 0, STAT_EXPERIMENTER: 0,
            STAT_ADMIN: 0, STAT_TEACHER_ADMIN: 0
        }
        for p in self.person_list:
            if p._person_gender == "男":
                res[STAT_MALE] += 1
            else:
                res[STAT_FEMALE] += 1
            # 先子类后父类，避免多重继承重复计数
            if isinstance(p, TeacherAdmin):
                res[STAT_TEACHER_ADMIN] += 1
            elif isinstance(p, Teacher):
                res[STAT_TEACHER] += 1
            elif isinstance(p, Experimenter):
                res[STAT_EXPERIMENTER] += 1
            elif isinstance(p, Admin):
                res[STAT_ADMIN] += 1
        return res

    def save(self, filename: str = 'data/person.json'):
        """将人员列表序列化为 JSON 文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in self.person_list],
                      f, ensure_ascii=False, indent=4)

    def load(self, filename: str = 'data/person.json'):
        """从 JSON 文件加载并还原类型，按编号去重"""
        class_map = {c.__name__: c for c in [Teacher, Experimenter, Admin, TeacherAdmin]}
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
            self.person_list.clear()
            seen = set()
            for d in data_list:
                class_name = d.get('__class__', '')
                if class_name not in class_map:
                    print(f'[警告] 未知人员类型: {class_name}，跳过该记录')
                    continue
                cls = class_map[class_name]
                person = cls.from_dict(d)
                if person._person_id not in seen:
                    seen.add(person._person_id)
                    self.person_list.append(person)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
```

---

## 三层架构关系

```
UI 层（用户界面）
  ├── CmdUI (CLI)         ─┐
  └── PersonTuiApp (TUI)  ─┤  共用 PersonService
                            │
Service 层（业务逻辑）      │
  └── PersonService  ◄─────┘
      ├── 增删改查
      ├── JSON 持久化
      ├── 统计
      └── CSV 导入导出

Model 层（数据模型）
  └── BaseClass  ◄──  Teacher, Experimenter, Admin, TeacherAdmin
```

## 设计要点

- **抽象**：`BaseClass` 定义公共属性和 4 个模板方法，子类只需覆写即可接入系统
- **封装**：所有属性用 `_` 前缀，外部通过 `to_dict()` / `from_dict()` 访问
- **继承**：3 个单继承 + 1 个多重继承，`TeacherAdmin` 直接调 `BaseClass.__init__()` 绕开 MRO
- **多态**：`PersonService` 通过 `isinstance` + 统一接口操作不同类型，无需判断 `__class__` 字符串
- **序列化**：JSON 中用 `__class__` 字段标记类型，加载时通过 `class_map` 还原
- **去重**：加载和查询结果双端按编号去重