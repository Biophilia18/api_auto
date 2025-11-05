"""
@ coding : utf-8 
@Time    : 2025/11/4 9:29
@Author  : admin1
@Project : api_auto
@File    : function_tool.py
@Desc    :
@Notes   : 
"""
import csv


def get_json_value(data, path: str):
    """
    常用工具：JSON 点路径取值
    支持：
    - "a.b.c"
    - 列表下标："items.0.id"
    """
    cur = data
    for part in path.split("."):
        if isinstance(cur, list) and part.isdigit():
            idx = int(part)
            cur = cur[idx]
        elif isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            raise KeyError(f"JSON中未找到字段路径：{path}")
    return cur

def load_csv_to_params(file_path):
    """读取csv，返回列表形式的params"""
    params = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # row是dict形式：{"name":xx, "sku":xx,...}
            params.append(row)
    return params
