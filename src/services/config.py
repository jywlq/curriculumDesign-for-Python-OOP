"""
配置管理模块

负责自动保存开关状态的读写，供 CmdUI 和 TuiApp 共用。
"""
import json

CONFIG_FILE = 'data/config.json'


def load_auto_save() -> bool:
    """从 config.json 加载自动保存开关状态"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get('autoSaveOn', False)
    except (FileNotFoundError, json.JSONDecodeError):
        return False


def save_auto_save(value: bool) -> None:
    """将自动保存开关状态持久化到 config.json"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump({'autoSaveOn': value}, f, ensure_ascii=False, indent=4)
