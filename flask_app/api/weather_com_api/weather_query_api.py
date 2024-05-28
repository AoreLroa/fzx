from loguru import logger

from utils.requests_utils import requests_weather_com
from settings import WEATHER_DOMAIN, WEATHER_KEY
from utils.abs_webpage import BaseWebPage


class BaseWeatherCom(BaseWebPage):

    def __init__(self, request_name):
        self._request_name = request_name

    @property
    def method(self):
        return "get"

    @property
    def url(self):
        return ""

    @property
    def headers(self):
        return {}

    def data(self):
        pass

    @property
    def params(self):
        return {}

    def make_request(self):
        try:
            response = requests_weather_com(
                request_name=self._request_name, method=self.method,
                url=self.url, headers=self.headers, params=self.params)
            return response
        except TimeoutError:
            logger.error(f"[{self._request_name}] ::: 请求超时")
        except Exception as all_e:
            logger.error(f"[{self._request_name}] ::: 请求遇到预期外的异常 {all_e}")

    def parse_response(self, data):
        pass


class CurrentWeatherPage(BaseWeatherCom):

    _REQUESTS_NAME = "获取[&]当前的天气"

    def __init__(self, api_key, location, **kwargs):
        super().__init__(
            request_name=self._REQUESTS_NAME.replace("&", location)
        )
        self._api_key = api_key
        self._location = location
        self._REQUESTS_NAME.replace("&", location)
        self._kwargs = kwargs

    @property
    def url(self):
        return WEATHER_DOMAIN + "/current.json"

    @property
    def params(self):
        return {
            "key": self._api_key,  # 接口的 API_KEY
            "lang": "zh",  # 响应体的内容使用简体中文
            "q": self._location,  # 查询的天气目标地
        }

    def parse_response(self, data):
        try:
            return {
                "时间": data["location"]["localtime"],
                "国家": data["location"]["country"],
                "地点（城市）": data["location"]["name"],
                "天气": data["current"]["condition"]["text"],
                "气温": data["current"]["temp_c"],
            }
        except Exception as all_e:
            logger.error(f"[{self._request_name}] ::: 解析请求时出现预期外的异常 {all_e}")


if __name__ == "__main__":
    n_location = "上海 中国"
    cw_obj = CurrentWeatherPage(api_key=WEATHER_KEY, location=n_location)
    try:
        cw_obj.parse_response(cw_obj.make_request())
    except Exception as all_e1:
        logger.error(f"预期外的异常 {all_e1}")
