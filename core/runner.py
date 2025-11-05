"""
@ coding : utf-8 
@Time    : 2025/11/2 17:52
@Author  : admin1
@Project : api_auto
@File    : runner.py
@Desc    : 读取 YAML → 动态生成 pytest 用例
          ✅ 支持流程用例（一个 YAML 多接口）
          ✅ 支持 params 数据驱动
          ✅ 自动替换 ${变量}，自动提取变量
          ✅ 自动写 Allure 报告
"""
import yaml
import allure
from core.requestor import requestor
from core.context import Context
from core.extractor import extract_value
from core.validator import do_validate
from utils.function_tool import load_csv_to_params

# 读取 base_url
with open("config/config.yaml", "r", encoding="utf-8") as f:
    _cfg = yaml.safe_load(f)
BASE_URL = _cfg["base_url"]


def generate_testcase_from_yaml(yaml_file):
    with open(yaml_file, "r", encoding="utf-8") as f:
        case_list = yaml.safe_load(f)

    # 允许 YAML 既可以是 List（流程），也可以是 Dict（单条）
    if isinstance(case_list, dict):
        case_list = [case_list]

    @allure.feature(case_list[0].get("feature", "默认模块"))
    @allure.story(case_list[0].get("story", "默认功能"))
    def test_func(self):
        # 不在这里清空上下文，避免误清 token；如需清理可在 session 结束时做
        for case in case_list:
            allure.dynamic.feature(case.get("feature", "未命名Feature"))
            allure.dynamic.story(case.get("story", "未命名Story"))
            allure.dynamic.title(case.get("title", "未命名用例"))

            # 数据驱动：每组 params 注入 Context
            # 优先从csv加载
            if "params_file" in case:
                csv_path = case["params_file"]
                params_list = load_csv_to_params(csv_path)
            else:
                params_list = case.get("params", [None])

            for param in params_list:
                if param:
                    for k, v in param.items():
                        Context.set(k, v)

                # ===== 请求准备 =====
                raw_url = case["request"]["url"]
                url = BASE_URL + Context.replace(raw_url)
                method = case["request"]["method"]
                headers = Context.replace(case["request"].get("headers", {}))
                json_data = Context.replace(case["request"].get("json", {}))
                #data_data = Context.replace(case["request"].get("data", None))

                # ===== 发送请求 =====
                resp = requestor.send(method, url, headers=headers,
                                      json=json_data)
                #                      data=data_data if data_data else None)

                # Allure 记录
                with allure.step(f"请求接口: {raw_url}"):
                    try:
                        req_body = resp.request.body
                    except Exception:
                        req_body = None
                    allure.attach(str(resp.request.headers), "请求Headers", allure.attachment_type.TEXT)
                    allure.attach(str(req_body), "请求Body", allure.attachment_type.TEXT)
                    allure.attach(resp.text, "响应Body", allure.attachment_type.JSON)

                # ===== 提取变量 =====
                if "extract" in case:
                    extract_value(resp, case["extract"], Context)

                # ===== 断言 =====
                if "validate" in case:
                    do_validate(resp, case["validate"])
                # 清楚当前的临时变量
                Context.clear_params()

    return test_func