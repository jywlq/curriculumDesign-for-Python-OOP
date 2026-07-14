"""
人员信息管理系统 - 程序入口

支持两种界面：
- python main.py        启动 TUI 界面（默认）
- python main.py --cli  启动命令行界面
"""
import sys

if '--cli' in sys.argv:
    from src.ui.cmd_ui import CmdUI
    app = CmdUI()
    app.run()
else:
    from src.ui.tui.tui_app import PersonTuiApp
    PersonTuiApp().run()
