"""
@ coding : utf-8 
@Time    : 2025/11/2 17:58
@Author  : admin1
@Project : api_auto
@File    : test_all_cases.py
@Desc    :
@Notes   : 
"""
from pathlib import Path

from core.runner import generate_testcase_from_yaml


class TestAPICase:
    # def test_fun(self):
    #     print(1)
    pass

ymal_files = Path("testcases").glob("*.yaml")
for file in ymal_files:
    print(file)
    func = generate_testcase_from_yaml(file)
    setattr(TestAPICase, f"test_{file.stem}", func)
