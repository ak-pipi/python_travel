# config/config_manager.py
# -*- coding: utf-8 -*-
"""
配置管理器，用于加载和管理DeepSeek相关配置
"""

import os
import configparser
from pathlib import Path
from typing import Any, Optional


class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.config = configparser.ConfigParser()
            self.config_path = self._get_config_path()
            self._load_config()
            self._initialized = True

    def _get_config_path(self) -> Path:
        """获取配置文件路径"""
        # 获取项目根目录（假设配置文件在项目根目录下）
        project_root = Path(__file__).parent.parent
        config_path = project_root / 'conf' / 'deepseek.ini'

        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        return config_path

    def _load_config(self):
        """加载配置"""
        self.config.read(self.config_path, encoding='utf-8')

    def get(self, section: str, key: str,
            default: Any = None, value_type: type = str) -> Any:
        """安全获取配置值"""
        try:
            if not self.config.has_section(section):
                return default

            if value_type == int:
                return self.config.getint(section, key, fallback=default)
            elif value_type == float:
                return self.config.getfloat(section, key, fallback=default)
            elif value_type == bool:
                return self.config.getboolean(section, key, fallback=default)
            else:
                return self.config.get(section, key, fallback=default)
        except (ValueError, configparser.Error):
            return default

    def get_deepseek_config(self) -> dict:
        """获取DeepSeek相关配置"""
        return {
            'api_key': self.get('deepseek', 'APIKey'),
            'model_name': self.get('deepseek', 'Model', 'deepseek-chat'),
            'api_base': self.get('deepseek', 'BaseURL', 'https://api.deepseek.com'),
            'temperature': self.get('deepseek', 'Temperature', 0.7, float),
            'max_tokens': self.get('deepseek', 'MaxTokens', 2048, int),
            'timeout': self.get('deepseek', 'Timeout', 30, int)
        }


# 创建全局实例
config_manager = ConfigManager()