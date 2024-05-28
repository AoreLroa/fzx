from loguru import logger
from zhipuai import ZhipuAI

from db.local_db import DBOperation
from sdk.zhipuai_sdk.chat_completion_sdk import chat_completions


class ZhiPuaiService:

    _zhipuai_client = None

    def __init__(self, api_key=None, model_name=None):
        # 构造初始化变量
        self._zhipuai_client = ZhipuAI(api_key=api_key)
        self._model_name = model_name
        self.db_operation = DBOperation()
        self.tools = None

        # 构造初始化数据
        self.init_service()

    def init_service(self):
        self.tools = self.db_operation.get_functions_info()

    def completion(self, message):
        """
        生成式，不存储上下文
        :param message: 用户询问的消息
        :return:
        """
        chat_message_list = [
            {"role": "system", "content": "不要假设或猜测传入函数的参数值。如果用户的描述不明确，请要求用户提供必要信息"},
            {"role": "user", "content": f"{message}"}
        ]
        response = chat_completions(
            zhipuai_client=self._zhipuai_client,
            model_name=self._model_name,
            messages=chat_message_list,
            tools=self.tools.get_tools_json()
        )
        logger.debug(f"获取的结果: {response.message.model_dump()}")
        return response.message.model_dump()

    def reply_completion(self, question, data=None):
        """
        根据给入的数据，通过 prompt 让大模型生成对应的自然语言反馈
        :param question: 用户的问题
        :param data: 生成回答时的参数
        :return:
        """
        chat_message_list = [
            {"role": "system", "content": "根据用户的问题 和 给入的参数，生成自然语言形式的反馈内容，内容要流畅、自然，如果无法生成内容，则返回如下信息“抱歉，我没理解你的意思”。"},
            {"role": "user",
             "content": f"问题：【{question}】\n可用信息：【{data}】，\n"
                        f"请根据“问题”，使用给到的“可用信息”，生成自然语言形式的反馈内容，并使用中文双引号括起来。"}
        ]
        response = chat_completions(
            zhipuai_client=self._zhipuai_client,
            model_name=self._model_name,
            messages=chat_message_list,
            tools=""
        )
        logger.debug(f"获取的结果: {response.message.model_dump()}")
        return response.message.model_dump()
