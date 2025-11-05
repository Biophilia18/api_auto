"""
@ coding : utf-8 
@Time    : 2025/11/2 19:18
@Author  : admin1
@Project : api_auto
@File    : validator.py
@Desc    :
@Notes   : 断言用
validate:
  equals:
    状态码为200: [200, status_code]
    业务码为0:   [0, json.code]
  contains:
    返回包含token: ["access_token", text]
    消息为success: ["success", json.message]   # contains 等价于包含/相等，这里是包含
"""
import time

from core.context import Context
from utils.db import db
from utils.function_tool import get_json_value


def do_validate(resp, validate_conf: dict):
    if not validate_conf:
        return

    # 1) equals
    equals = validate_conf.get("equals", {})
    for desc, (expected, actual_expr) in equals.items():
        if actual_expr == "status_code":
            actual = resp.status_code
        elif actual_expr.startswith("json."):
            path = actual_expr.replace("json.", "")
            actual = get_json_value(resp.json(), path)
        else:
            raise ValueError(f"[YAML错误] 不支持的 equals 路径：{actual_expr}")
        assert str(expected) == str(actual), f"[断言失败] {desc}: 期望 {expected}, 实际 {actual}"

    # 2) contains
    contains = validate_conf.get("contains", {})
    for desc, (keyword, target) in contains.items():
        if target == "text":
            assert str(keyword) in resp.text, f"[断言失败] {desc}: 响应不包含 {keyword}"
        elif target.startswith("json."):
            path = target.replace("json.", "")
            actual = get_json_value(resp.json(), path)
            assert str(keyword) in str(actual), f"[断言失败] {desc}: {path} 未包含 {keyword}"
        else:
            raise ValueError(f"[YAML错误] contains 仅支持 text/json.xx, 当前:{target}")

    # 3) db_validate
    db_validate = validate_conf.get("db_validate", {})
    for desc, rule in db_validate.items():
        sql = Context.replace(rule["sql"])
        expected = [Context.replace(str(v)) for v in rule["expect"]]

        result = None
        for i in range(3):  # 最多重试3次
            result = db.query(sql)
            if result:
                break
            time.sleep(0.3)

        if not result:
            raise AssertionError(f"数据库断言失败：{desc} 查询无结果 -> {sql}")

        flat = [str(x) for x in result[0]]
        assert flat == [str(x) for x in expected], \
            f"数据库断言失败：{desc} 期望 {expected}, 实际 {flat}"