"""
@ coding : utf-8 
@Time    : 2025/11/1 23:04
@Author  : admin1
@Project : api_auto
@File    : response_handler.py
@Desc    :
@Notes   : 
"""
class BaseResponse:
    def __init__(self, response):
        self.raw =response
        try:
            self.body = response.json()
        except Exception:
            self.body = {}
    @property
    def data(self):
        return self.body.get("data") or {}
    def get(self,key,default=None):
        return self.data.get(key,default)