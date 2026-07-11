# 改动记录

## 1. 命名规范重构

将代码命名从驼峰/小写改为 Python PEP 8 标准。

### 类名：小写 → PascalCase

| 原名 | 新名 |
|------|------|
| baseClass | BaseClass |
| teacher | Teacher |
| experimenter | Experimenter |
| admin | Admin |
| teacher_admin | TeacherAdmin |
| personService | PersonService |

### 方法名/变量名：驼峰 → snake_case

| 原名 | 新名 |
|------|------|
| personID | person_id |
| personName | person_name |
| personGender | person_gender |
| personAge | person_age |
| department | department |
| major | major |
| professionalTitle | professional_title |
| politicalAffiliation | political_affiliation |
| laboratory | laboratory |
| duties | duties |
| inputWithBack | input_with_back |
| clearScreen | clear_screen |
| showAllPerson | show_all_person |
| showMenu | show_menu |
| showMessage | show_message |
| showFilterMenu | show_filter_menu |
| loadConfig | load_config |
| saveConfig | save_config |
| saveIfAuto | save_if_auto |
| dataChange | data_change |
| addPerson | add_person |
| findPerson | find_person |
| updatePerson | update_person |
| deletePerson | delete_person |
| getPersonStatistics | get_person_statistics |
| personIDCheck | person_id_check |
| loaddata | load_data |
| autoSave | auto_save |
| filterID | filter_id |
| filterName | filter_name |
| updateID | update_id |
| updateName | update_name |
| getResult | get_result |
| PERSON_TYPE | PERSON_TYPE（常量保持） |
| MENU | MENU（常量保持） |
| CONFIG_FILE | CONFIG_FILE（常量保持） |

### 涉及文件

- `src/models/base.py`
- `src/models/teacher.py`
- `src/models/experimenter.py`
- `src/models/admin.py`
- `src/models/teacher_admin.py`
- `src/models/__init__.py`
- `src/services/__init__.py`
- `src/services/person_service.py`
- `src/ui/__init__.py`
- `src/ui/cmd_ui.py`
- `src/ui/collector.py`
- `src/ui/filter.py`
- `src/ui/exceptions.py`

---

## 2. 注释完善

为所有源码文件添加规范的 docstring 注释。

### 注释风格

- **标准风格**：`base.py`、`teacher_admin.py`、`person_service.py`、`cmd_ui.py`、`collector.py`
- **简洁风格**：其他文件

### 主要注释内容

| 文件 | 注释内容 |
|------|----------|
| `base.py` | 模块docstring（说明设计模式）+ 类docstring（说明封装和模板方法）+ 方法docstring |
| `teacher_admin.py` | 类docstring（说明多重继承和绕开MRO） |
| `person_service.py` | 模块docstring + 类docstring + 所有方法docstring |
| `cmd_ui.py` | 模块docstring + 类docstring + 关键方法docstring |
| `collector.py` | 模块docstring（说明多态）+ 类docstring + 方法docstring |
| 其他文件 | 模块docstring + 类docstring |

### 涉及文件

- `main.py`
- `src/models/__init__.py`
- `src/models/base.py`
- `src/models/teacher.py`
- `src/models/experimenter.py`
- `src/models/admin.py`
- `src/models/teacher_admin.py`
- `src/services/__init__.py`
- `src/services/person_service.py`
- `src/ui/__init__.py`
- `src/ui/cmd_ui.py`
- `src/ui/collector.py`
- `src/ui/filter.py`
- `src/ui/exceptions.py`

---

## 3. 输入验证增强

增强用户输入的格式和长度验证。

### 改动详情

| 字段 | 改动前 | 改动后 |
|------|--------|--------|
| 编号 | 只检查字母数字 | 正则验证：`^(T\|E\|A\|TA)\d{3}$` |
| 姓名 | 无长度限制 | 2-20 个字符 |
| 年龄 | 有验证但提示简单 | 输入时提示范围 |

### 新增代码

```python
import re

# 编号格式规则：类型前缀 + 三位数字
ID_PATTERN = re.compile(r'^(T|E|A|TA)\d{3}$')
```

### 编号格式规范

| 人员类型 | 前缀 | 示例 |
|----------|------|------|
| 教师 | T | T001 |
| 实验员 | E | E001 |
| 行政人员 | A | A001 |
| 教师兼行政人员 | TA | TA001 |

### 涉及文件

- `src/ui/collector.py`

---

## 4. 新增文档

- `docs/change.md` - 本文档，记录所有改动

---

## 后续待完成

- 统计功能增强（get_person_statistics 增加总人数、男女比例）
- README.md 重写
