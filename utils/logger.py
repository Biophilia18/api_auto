"""
@ coding : utf-8 
@Time    : 2025/11/2 17:43
@Author  : admin1
@Project : api_auto
@File    : logger.py
@Desc    :
@Notes   : 
"""
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


class Logger:
    def __init__(self, name="API"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # 防止重复添加多个 handler
        if not self.logger.handlers:
            # 1) 日志文件
            file_handler = RotatingFileHandler(
                filename=f"{LOG_DIR}/api.log",
                maxBytes=5 * 1024 * 1024,  # 5MB
                backupCount=3,
                encoding="utf-8"
            )
            file_format = logging.Formatter(
                "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(file_format)

            # 2) 终端输出简洁格式
            console_handler = logging.StreamHandler()
            console_format = logging.Formatter("[%(levelname)s] %(message)s")
            console_handler.setFormatter(console_format)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger