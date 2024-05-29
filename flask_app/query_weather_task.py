import json

from loguru import logger

from service.zhipuai_service import ZhiPuaiService
from settings import WEATHER_KEY, ZHIPU_API_KEY
from service.weather_com_service import WeatherComService

zhipu_service = function_call = functions = chat_message_list = None


def judge_reply(reply_msg) -> dict:
    """
    解析回复的内容，判断是否有效，如果有效，判断是否需要调用方法函数
    :param reply_msg:
    :return:
    """
    parse_res_flag = {"execute_function": False, "function_name": "", "function_args": {}}
    try:
        role = reply_msg.get("role", None)
        answer_type = reply_msg.get("tool_calls", {})

        if role == "assistant" and answer_type:
            parse_res_flag["execute_function"] = True
            parse_res_flag["function_name"] = reply_msg.get("tool_calls", {})[0].get("function", {}).get("name", "")
            parse_res_flag["function_args"].update(
                json.loads(reply_msg.get("tool_calls", {})[0].get("function", {}).get("arguments", {}))
            )
        else:
            parse_res_flag["content"] = reply_msg.get("content", "")
    except Exception as all_e:
        logger.error(f"[解析回复内容] ::: 非预期异常 {all_e}")
    finally:
        logger.info(f"[解析回复内容] ::: 解析结果 {parse_res_flag}")
        return parse_res_flag


def weather_start_task(query_msg: str):
    """
    定时任务
    :param query_msg: 用户的询问语
    :return:
    """
    global zhipu_service, function_call, functions, chat_message_list

    query_res = None
    if not zhipu_service:
        model_name = "glm-4"

        zhipu_service = ZhiPuaiService(
            api_key=ZHIPU_API_KEY, model_name=model_name
        )

    # 将用户的提问，维护进入对话中，并询问 大模型
    reply_res = zhipu_service.completion(message=query_msg)
    # 判断 大模型 的回复是否有效等
    parse_reply_flag = judge_reply(reply_msg=reply_res)

    # 判断是否需要调用对应的函数
    if parse_reply_flag["execute_function"]:
        msg = ""
        function_name = parse_reply_flag["function_name"]
        function_args = parse_reply_flag["function_args"]
        wc_service = WeatherComService(api_key=WEATHER_KEY)
        if function_name == "query_current_weather_by_location":
            query_res = wc_service.query_current_weather_by_location(**function_args)
            msg = "\t".join([f"{key}={value}" for key, value in query_res.items()])
        logger.debug(msg)
        # 再给到大模型，根据参数生成回复内容  TODO 可以优化。目前一次使用一个对象
        reply_res = zhipu_service.reply_completion(question=query_msg, data=query_res)
        parse_reply_flag = judge_reply(reply_msg=reply_res)
        reply_res = parse_reply_flag["content"]
    else:
        reply_res = parse_reply_flag["content"]
    return reply_res


if __name__ == "__main__":
    while True:
        q = input("请问你要查询天气吗？\n")
        answer = weather_start_task(query_msg=q)
        print(answer)
