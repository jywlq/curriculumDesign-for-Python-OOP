# 项目说明

### 项目架构：

```markdown
myWork/              
│
├── src/                      # 所有源代码
│   ├── __init__.py           # 让 src 成为 Python 包
│   ├── models.py             # 数据模型类（Person, Teacher 等）
│   ├── services.py           # 业务逻辑类（增删改查、文件读写）
│   └── ui.py                 # 命令行交互界面（菜单、输入输出）
│
├── data/                     # 数据文件存放
│   └── (程序运行后自动生成 persons.json)
│
├── docs/                     # 你的设计文档
│   ├── 类图.png
│   └── 流程图.png
│
├── tests/                    # 简单测试（可选，加分项）
│   └── test_services.py
│
├── main.py                   # 程序入口（与 src 同级）
└── README.md                 # 项目说明
```

