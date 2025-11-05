"""
@ coding : utf-8 
@Time    : 2025/11/1 22:38
@Author  : admin1
@Project : api_auto
@File    : conftest.py
@Desc    :
@Notes   : 
"""

import pytest
import yaml
from core.context import Context
from core.requestor import requestor

# 读取 base_url
with open("config/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
base_url = config["base_url"]


@pytest.fixture(scope="session", autouse=True)
def init_token():
    """整个测试执行前，登录一次，把 token 存到 Context"""
    with open("config/config.yaml",encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    if Context.get("token"):   # 如果已经有 token，就不重复登录
        return

    resp = requestor.send("post", cfg["base_url"] + "/auth/login",
                          json={"username": cfg["username"], "password": cfg["password"]})
    token = resp.json().get("data", {}).get("access_token")
    if not token:
        raise RuntimeError("登录失败，无法获取token")
    Context.set("token", token)
    print("[init_token] ✅ 已获取 token：", token[:10], "...")



