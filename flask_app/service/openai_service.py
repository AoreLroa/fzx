from loguru import logger

from api.openai_api.chat_completion_api import ChatCompletionPage


class OpenaiService:

    # 对话、聊天 上下文
    _CHAT_MESSAGE_CONTEXT = []
    # 暂存 chat_gpt 的回复内容
    _TMP_REPLY = None

    def __init__(self, api_key, chat_message_list, model_name, functions=None, function_call=None):
        self._api_key = api_key
        self._chat_message_list = chat_message_list
        self._model_name = model_name
        self._functions = functions
        self._function_call = function_call

    def chat_completion(self):
        """
        和 chat-gpt 进行对话
        :return:
        """
        cc_obj = ChatCompletionPage(
            api_key=self._api_key,
            chat_message_list=self._chat_message_list,
            model_name=self._model_name,
            functions=self._functions,
            function_call=self._function_call
        )
        try:
            self._TMP_REPLY = cc_obj.parse_response(data=cc_obj.make_request())
            return self._TMP_REPLY
        except Exception as all_e:
            logger.error(f"[] ::: 预期外的异常 {all_e}")

    def update_user_question(self, user_question):
        """
        将用户的提问等消息加入到上下文中
        :param user_question: 用户的提问或消息
        :return:
        """
        self._CHAT_MESSAGE_CONTEXT.append(user_question)

    def update_reply(self, update_flag: bool = True):
        """
        更新 chat_gpt 的回复内容保存到到上下文中
        :param update_flag:
        :return:
        """
        if update_flag:
            self._CHAT_MESSAGE_CONTEXT.append(self._TMP_REPLY)
        self._TMP_REPLY = None
