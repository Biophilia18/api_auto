"""
@ coding : utf-8 
@Time    : 2025/11/2 19:01
@Author  : admin1
@Project : api_auto
@File    : context.py
@Desc    :
@Notes   : 全局上下文：保存跨接口变量（如 token、id），并支持 ${var} 占位替换
- Context.set / get：变量读写
- Context.replace：递归替换 str/dict/list 中的 ${var}
- Context.clear_temp(keep_keys)：清理变量时可保留指定 key（例如 token）
"""
import re
from copy import deepcopy

class Context:
    _storage = {}

    @classmethod
    def set(cls, key, value):
        cls._storage[key] = value

    @classmethod
    def get(cls, key, default=None):
        return cls._storage.get(key, default)

    @classmethod
    def replace(cls, data):
        """
        递归替换字符串中的 ${var} 为 Context 中存储的值
        """
        from copy import deepcopy
        data = deepcopy(data)

        if isinstance(data, str):
            for k, v in cls._storage.items():
                data = data.replace(f"${{{k}}}", str(v))
            return data

        if isinstance(data, dict):
            return {k: cls.replace(v) for k, v in data.items()}

        if isinstance(data, list):
            return [cls.replace(i) for i in data]

        return data

    @classmethod
    def clear_params(cls):
        """
        清除当前 case 中的参数变量，例如 name/sku/price，
        但不清除 token，确保登录只做一次
        """
        keys_to_del = []
        for k in cls._storage:
            if k not in ("token",):  # 可以自行扩展白名单
                keys_to_del.append(k)
        for k in keys_to_del:
            cls._storage.pop(k, None)