# 人员信息管理系统

Python 命令行人员管理系统，用于管理教师、实验员、行政人员等信息。

## 功能特性

- **添加人员**：支持四种人员类型，编号唯一性校验
- **查询人员**：按编号/姓名前缀筛选，支持组合筛选
- **显示人员**：显示所有人员记录
- **修改人员**：筛选后选择序号修改
- **删除人员**：筛选后选择序号删除，支持确认操作
- **统计人员**：按类型统计人数
- **数据持久化**：JSON格式存储，支持自动保存/手动保存
- **配置持久化**：自动保存状态跨会话保持

## 项目结构

```
.
├── main.py                 # 程序入口
├── src/
│   ├── models/             # 数据模型
│   │   ├── base.py         # 基类 baseClass
│   │   ├── teacher.py      # 教师类
│   │   ├── experimenter.py # 实验员类
│   │   ├── admin.py        # 行政人员类
│   │   └── teacher_admin.py# 教师兼行政人员类
│   ├── services/           # 业务逻辑
│   │   └── person_service.py
│   └── ui/                 # 命令行界面
│       ├── exceptions.py   # 异常类
│       ├── filter.py       # 筛选器
│       ├── collector.py    # 信息收集器
│       └── cmd_ui.py       # 主界面
├── data/                   # 数据文件
│   ├── person.json         # 人员数据
│   └── config.json         # 配置文件
├── docs/                   # 设计文档
│   ├── 类图.png
│   └── 流程图.png
└── text/                   # 课程设计文档
```

## 运行方式

```bash
python main.py
```

## 菜单说明

| 编号 | 功能 | 说明 |
|------|------|------|
| 1 | 添加人员 | 选择类型→输入信息→支持连续添加 |
| 2 | 查询人员 | 筛选列表，按编号/姓名前缀筛选 |
| 3 | 显示人员 | 显示所有人员记录 |
| 4 | 修改人员 | 筛选后选择序号修改 |
| 5 | 删除人员 | 筛选后选择序号删除，需确认 |
| 6 | 统计人员 | 按类型统计人数 |
| 7 | 自动保存 | 切换开关(已开启/已关闭) |
| 8 | 手动保存 | 立即保存数据 |
| 9 | 读取数据 | 重新加载数据文件 |
| 0 | 退出系统 | 保存并退出 |

## 人员类型

| 类型 | 特有字段 |
|------|----------|
| 教师 | 所在系部、专业、职称 |
| 实验员 | 所在实验室、职务 |
| 行政人员 | 政治面貌、职称 |
| 教师兼行政人员 | 所在系部、专业、职称、政治面貌 |

## 技术特点

### 面向对象特性

- **抽象**：baseClass 作为基类，定义公共属性和方法
- **封装**：私有属性（`_personID`、`_personName` 等）
- **继承**：teacher、experimenter、admin 继承 baseClass
- **多态**：`getFields()`、`to_dict()`、`from_dict()` 各类自行实现

### 架构设计

- **三层架构**：models（数据）→ services（业务）→ ui（界面）
- **模块化**：每个类独立文件，职责清晰
- **异常处理**：ReturnBack 异常实现菜单返回，KeyboardInterrupt 保护退出

### 数据持久化

- 人员数据：`data/person.json`
- 配置数据：`data/config.json`
- 支持自动保存（每次增删改后）
- 支持手动保存/读取

## 操作说明

### 通用操作

- 输入 `0`：返回上级菜单 / 退出系统
- 按 `Ctrl+C`：保存并退出系统

### 筛选操作（查询/修改/删除）

1. 选择 `1` 按编号筛选
2. 选择 `2` 按姓名筛选
3. 选择 `3` 重置筛选条件
4. 选择 `4` 执行操作（修改/删除）

### 删除确认

删除前会提示确认：
```
确认删除 张三(T001)？(y/n)：
```
- 输入 `y`：执行删除
- 输入 `n`：取消删除

## 数据格式

### person.json

```json
[
    {
        "__class__": "teacher",
        "personID": "T001",
        "personName": "张三",
        "personGender": "男",
        "personAge": "35",
        "department": "计算机系",
        "major": "软件工程",
        "professionalTitle": "副教授"
    }
]
```

### config.json

```json
{
    "autoSaveOn": false
}
```

## 开发说明

### 添加新人员类型

1. 在 `src/models/` 创建新类，继承 baseClass
2. 实现 `getFields()`、`to_dict()`、`from_dict()` 方法
3. 在 `src/models/__init__.py` 导出
4. 在 `src/services/person_service.py` 的 classMap 中注册
5. 在 `src/ui/collector.py` 的 PERSON_TYPE 中添加映射

### 命名规范

- 类名：驼峰命名（`personService`、`PersonFilter`）
- 方法名：驼峰命名（`inputWithBack`、`clearScreen`）
- 私有属性：下划线前缀（`_personID`、`_personName`）
