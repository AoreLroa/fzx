from loguru import logger

from flask_app.utils.abs_webpage import BaseWebPage
from flask_app.utils.requests_utils import requests_chat_completion


class BaseOpenai(BaseWebPage):
    def __init__(self, request_name, api_key):
        self._request_name = request_name
        self._api_key = api_key

    @property
    def method(self):
        return "post"

    @property
    def url(self):
        return ""

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self._api_key}",
        }

    @property
    def data(self):
        return {}

    def params(self):
        pass

    def make_request(self):
        try:
            response = requests_chat_completion(
                request_name=self._request_name, method=self.method,
                url=self.url, headers=self.headers, data=self.data)
            return response
        except TimeoutError:
            logger.error(f"[{self._request_name}] ::: 请求超时")
        except Exception as all_e:
            logger.error(f"[{self._request_name}] ::: 请求遇到预期外的异常 {all_e}")

    def parse_response(self, data):
        pass


class ChatCompletionPage(BaseOpenai):

    _REQUESTS_NAME = "CHAT_COMPLETION"

    def __init__(self, api_key, chat_message_list, model_name, functions=None, function_call=None):
        super().__init__(request_name=self._REQUESTS_NAME, api_key=api_key)
        self._chat_message_list = chat_message_list
        self._function_call = function_call
        self._model_name = model_name
        self._functions = functions

    @property
    def url(self):
        return "https://api.openai.com/v1/chat/completions"

    @property
    def data(self):
        datas = {"model": self._model_name, "messages": self._chat_message_list}
        if self._functions and len(self._functions) >= 1:
            datas.update({
                "functions": self._functions
            })
        if self._function_call and len(self._function_call) >= 1:
            datas.update({
                "function_call": self._function_call
            })
        return datas

    def parse_response(self, data):
        try:
            return data["choices"][0]["message"]
        except Exception as all_e:
            logger.error(f"[{self._request_name}] ::: 解析请求结果出现预期外的异常 {all_e}")
