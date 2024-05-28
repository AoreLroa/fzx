import requests

from loguru import logger


def updates_headers(headers: dict):
    """
    更新 通用的 请求头
    :param headers: 通用的请求头
    :return:
    """
    comm_headers = {
        "Content-Type": "application/json"
    }
    if headers:
        comm_headers.update(headers)
        if headers.get("del_filed", None):
            [comm_headers.pop(key) for key in headers.get("del_-filed")]
    return comm_headers


def requests_weather_com(request_name: str, method: str, url: str, headers: dict = None, params: dict = None):
    """
    三方天气网站的公共请求方法
    :param request_name: 请求的接口名称
    :param method: 请求类型——POST、GET、UPDATE
    :param url: 请求到接口地址
    :param headers: 请求头。有公共请求头，如果接口对请求头有特殊参数的要求，可以基于公共请求头进行更新后使用
    :param params: 请求携带的参数
    :return response: 返回一个 json 格式的数据
    """
    json_data = {}
    try:
        response = requests.request(
            method=method.upper(), url=url, params=params, timeout=30,
            headers=updates_headers(headers=headers))

        json_data = response.json()
    except TimeoutError as te_e:
        logger.error(f"[{request_name}] ::: 请求超时 {te_e}")
    except Exception as all_e:
        logger.error(f"[{request_name}] ::: 请求遇到预料之外的异常 {all_e}")
    finally:
        return json_data


def requests_chat_completion(request_name: str, method: str, url: str, headers: dict = None, data: dict = None):
    """
    openai 的接口请求方法
    :param request_name: 接口请求名称
    :param method: 请求方法
    :param url: 请求的接口
    :param headers: 请求头
    :param data: 请求参数
    :return:
    """
    json_data = {}
    try:
        response = requests.request(
            method=method.upper(), url=url, data=data, timeout=30,
            headers=updates_headers(headers=headers))

        json_data = response.json()
    except TimeoutError as te_e:
        logger.error(f"[{request_name}] ::: 请求超时 {te_e}")
    except Exception as all_e:
        logger.error(f"[{request_name}] ::: 请求遇到预料之外的异常 {all_e}")
    finally:
        return json_data
