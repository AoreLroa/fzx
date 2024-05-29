from loguru import logger

from ..api.weather_com_api.weather_query_api import CurrentWeatherPage


class WeatherComService:

    def __init__(self, api_key):
        self._api_key = api_key

    def query_current_weather_by_location(self, location):
        """
        根据指定的地点，查询当前的天气。
            地点格式为：国家 城市（或者地名）
        :return:
        """
        cw_obj = CurrentWeatherPage(api_key=self._api_key, location=location)
        try:
            return cw_obj.parse_response(data=cw_obj.make_request())
        except Exception as all_e:
            logger.error(f"预期外的异常 {all_e}")
