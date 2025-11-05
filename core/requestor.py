"""
@ coding : utf-8 
@Time    : 2025/11/2 17:39
@Author  : admin1
@Project : api_auto
@File    : requestor.py
@Desc    :
@Notes   : 统一请求管理
"""
import json
import logging
import time

import requests

from utils.logger import Logger


class Requestor:
    """
    统一 requests.Session；带基本日志
    """
    def __init__(self):
        self.session = requests.Session()
        self.logger = Logger().get_logger()

    def send(self, method, url, **kwargs):
        # 结构化日志
        line = "-" * 65
        self.logger.info(f"\n{line}")
        self.logger.info(f"[REQUEST] {method.upper()} {url}")

        if "headers" in kwargs:
            self.logger.info(f" [HEADERS]:")
            for k, v in kwargs["headers"].items():
                self.logger.info(f"   {k}: {v}")

        if "json" in kwargs and kwargs["json"]:
            body_str = json.dumps(kwargs["json"], ensure_ascii=False, indent=4)
            self.logger.info(f" [JSON Body]:")
            self.logger.info(f"{body_str}")
        elif "data" in kwargs and kwargs["data"]:
            self.logger.info(f" Form Data:")
            self.logger.info(str(kwargs['data']))
        # 发送请求并计时
            # ========== 发送请求并计时 ==========
        start_time = time.time()
        resp = self.session.request(method=method, url=url, **kwargs)
        elapsed_time = round((time.time() - start_time) * 1000, 2)
        # 响应日志
        try:
            body = json.dumps(resp.json(), ensure_ascii=False, indent=4)
        except Exception:
            body = resp.text
        self.logger.info("\n[RESPONSE]")
        self.logger.info(f"  Status : {resp.status_code}")
        self.logger.info(f"  Elapsed Time: {elapsed_time} ms")
        self.logger.info(f"  Response Body   :\n{body}")
        self.logger.info(line + "\n")

        return resp


requestor = Requestor() #单例形式