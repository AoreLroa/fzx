
def chat_completions(zhipuai_client, model_name, messages, tools=None):
    if not model_name or not messages:
        raise f"model_name or messages is null, you must provide 'model_name' and 'messages'"
    request_dict = {
        "model": model_name,
        "messages": messages,
    }
    if tools:
        request_dict["tools"] = tools
    try:
        response = zhipuai_client.chat.completions.create(**request_dict)
        return response.choices[0]
    except Exception as all_e:
        print(all_e)
