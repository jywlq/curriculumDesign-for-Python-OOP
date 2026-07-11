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

## 4. 数据格式统一

将 `person.json` 中的 `__class__` 字段从 snake_case 改为 PascalCase，与类名保持一致。

### 改动详情

| 原值 | 新值 |
|------|------|
| `"teacher"` | `"Teacher"` |
| `"experimenter"` | `"Experimenter"` |
| `"admin"` | `"Admin"` |
| `"teacher_admin"` | `"TeacherAdmin"` |

### 涉及文件

- `data/person.json`
- `src/services/person_service.py`（还原 class_map 为简洁写法）

---

## 5. 手动保存/读取提示

为手动保存（菜单8）和读取数据（菜单9）增加操作成功提示，不影响其他地方的保存/读取。

### 改动详情

| 操作 | 改动前 | 改动后 |
|------|--------|--------|
| 菜单8 手动保存 | 闪屏 | 清屏 + 显示"保存成功" |
| 菜单9 读取数据 | 闪屏 | 清屏 + 显示"读取成功" |

### 代码改动

```python
# 菜单映射改为 manual_save / manual_load
"8": self.manual_save,
"9": self.manual_load,

# 新增两个方法，底层 save/load_data 不变
def manual_save(self):
    self.save()
    self.show_message('保存成功')

def manual_load(self):
    self.load_data()
    self.show_message('读取成功')
```

### 涉及文件

- `src/ui/cmd_ui.py`

---

## 6. 统计功能增强

增强人员统计功能，增加总人数和性别分布统计，并美化显示界面。

### 数据层改动

**文件：** `src/services/person_service.py`

`get_person_statistics()` 增加：
- 总人数统计
- 男/女员工数量统计

### 显示层改动

**文件：** `src/ui/cmd_ui.py`

`get_person_statistics()` 改为表格格式显示：
- 使用 `╔═══╗` 框线
- 分区显示：总览 + 按类型
- 对齐格式化

### 显示效果

```
╔══════════════════════════╗
║       人员统计           ║
╠══════════════════════════╣
║  【总览】                ║
║  总人数：30              ║
║  男员工：18              ║
║  女员工：12              ║
╠══════════════════════════╣
║  【按类型】              ║
║  教师：    12            ║
║  实验员：  8             ║
║  行政人员：6             ║
║  教师兼行政：4           ║
╚══════════════════════════╝
```

### 涉及文件

- `src/services/person_service.py`
- `src/ui/cmd_ui.py`

---

## 7. 无效操作提示修复

修复查询模式下按无效键不提示的问题。

### 问题描述

查询、修改、删除共用 `_filter_list` 方法，但查询模式下按无效键不提示"无效的操作编号"。

### 原因

原代码有 `if action_name:` 判断，查询模式下 `action_name=None`，所以跳过提示。

### 修复

去掉 `if action_name:` 条件，无条件提示无效操作。

```python
# 改动前
else:
    if action_name:
        self.show_message('无效的操作编号')

# 改动后
else:
    self.show_message('无效的操作编号')
```

### 涉及文件

- `src/ui/cmd_ui.py`

---

## 8. 新增文档

- `docs/change.md` - 本文档，记录所有改动
- `.mimocode/plans/statistics-improvement.md` - 统计功能改进计划

---

## 后续待完成

- README.md 重写
