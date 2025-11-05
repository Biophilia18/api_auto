"""
@ coding : utf-8 
@Time    : 2025/11/2 19:05
@Author  : admin1
@Project : api_auto
@File    : extractor.py
@Desc    :
@Notes   : 提取响应数据中的变量，写入 Context
          ✅ 支持 json 提取: ["json", "data.access_token"]
          ✅ token 自动保存为全局变量
"""
from utils.function_tool import get_json_value
from core.context import Context


def extract_value(resp, extract_dict: dict, ctx: Context = Context):
    if not extract_dict:
        return
    for var_name, rule in extract_dict.items():
        if not isinstance(rule, (list, tuple)) or len(rule) < 1:
            raise ValueError(f"extract 配置错误：{var_name} -> {rule}")
        source = rule[0]
        if source == "json":
            if len(rule) < 2:
                raise ValueError(f"extract json 需要提供路径：{var_name}")
            path = rule[1]
            value = get_json_value(resp.json(), path)
        elif source == "text":
            value = resp.text
        else:
            raise ValueError(f"不支持的提取源：{source}")
        ctx.set(var_name, value)


