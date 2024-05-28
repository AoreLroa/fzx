"""
智谱清言 的 函数调用 功能相关类
    Property: 单个属性类
    FunctionBody: 单个函数的定义
    Tool: 工具类
"""


class Property:
    """
    单个属性类
    """
    _variable_name = ""
    _variable_type = None
    _variable_description = ""

    def __init__(self, variable_name, variable_type, variable_description):
        """
        属性构造函数
        :param variable_name: 变量名称
        :param variable_type: 变量类型
        :param variable_description: 变量描述
        """
        self._variable_name = variable_name
        self._variable_type = variable_type
        self._variable_description = variable_description

    def __str__(self):
        return f"变量名: {self._variable_name} , 变量类型: {self._variable_type} , 变量描述: {self._variable_description}"

    def get_property_json(self) -> dict:
        """
        将属性以 dict 形式返回
        :return:
        """
        return {
            self._variable_name: {
                "description": self._variable_description,
                "type": self._variable_type,
            }
        }

    @property
    def variable_name(self):
        return self._variable_name


class FunctionBody:
    """
    单个函数的定义
    """
    _function_name = ""
    _function_description = ""
    _function_parameters = []

    def __init__(self, function_name, function_description):
        """
        函数构造函数
        :param function_name: 函数名
        :param function_description: 函数的描述
        """
        self._function_name = function_name
        self._function_description = function_description

    def __str__(self):
        return f"函数名: {self._function_name} , 函数描述: {self._function_description}"

    def set_parameters(self, v_property: Property):
        """
        设置函数参数
        :param v_property:
        :return:
        """
        self._function_parameters.append(v_property)

    def get_function_body_json(self) -> dict:
        """
        获取函数的定义
        :return:
        """
        request_dict = {
            "name": self._function_name,
            "description": self._function_description,
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
        for parameter in self._function_parameters:
            request_dict["parameters"]["properties"].update(parameter.get_property_json())
            request_dict["parameters"]["required"].append(parameter.variable_name)

        return request_dict


class Tool:
    """
    "函数调用" 时的请求参数体
    """

    _tool_type = "function"
    _tool_function = []
    _tool_choice = "auto"

    def set_tools_info(self, tool_type=None, tool_function: FunctionBody = None):
        """
        设置 Tool 的参数值
        :param tool_type:
        :param tool_function:
        :return:
        """
        if tool_type:
            self._tool_type = tool_type
        self._tool_function.append(tool_function)

    def get_tools_json(self) -> list:
        """
        获取 dict 格式的 tools
        :return:
        """
        res_data = []
        base_data_dict = {
            "type": self._tool_type,
            "function": {}
        }
        for function in self._tool_function:
            res_data.append({
                **(base_data_dict.copy())
            })
            res_data[-1]['function'].update(function.get_function_body_json())
        return res_data
