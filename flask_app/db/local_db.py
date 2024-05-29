from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..settings import local_mysql_config as lmc
from ..utils.mate_class import SingletonMeta
from ..models.db_model import FunctionRegedit, VariableRegedit
from ..models.zhipuai_model import FunctionBody, Property, Tool

# 数据库链接
engine = create_engine(f"mysql+mysqlconnector://{lmc['user']}:{lmc['password']}@{lmc['host']}:{lmc['port']}/{lmc['database']}")


class DBOperation(metaclass=SingletonMeta):

    # 全局唯一会话
    _session = sessionmaker(bind=engine)()

    def regedit_function(self, f_name, f_description, **kwargs):
        """
        注册函数
        :param f_name: 函数名
        :param f_description: 函数的描述
        :param kwargs: 动态参数
        :return:
        """
        try:
            function_record = FunctionRegedit(function_name=f_name, function_description=f_description)
            self._session.add(function_record)
            self._session.commit()

            if function_record.function_id <= 0:
                raise Exception("function regedit is fail, Exception: No corresponding 'function_id' is generated")
            # 创建变量
            variable_obj_list = []
            for v_name, v_value in kwargs.items():
                variable = VariableRegedit(
                    function_id=function_record.function_id,
                    variable_name=v_name,
                    variable_type=v_value['type'],
                    variable_description=v_value['description'])
                variable_obj_list.append(variable)
            self._session.add_all(variable_obj_list)
            self._session.commit()
            print(f"function {f_name} regedit success")
        except Exception as e:
            print(e)
        finally:
            self._session.close()

    def get_functions_info(self):
        """
        获取所有可用函数信息
        :return:
        """
        res_data = Tool()
        try:
            # 查询条件：function_active 值为 1
            active_functions = self._session.query(FunctionRegedit).filter_by(function_active=1).all()

            # 连表查询
            for function in active_functions:
                fun_obj = FunctionBody(
                    function_name=function.function_name,
                    function_description=function.function_description
                )
                variables = self._session.query(VariableRegedit).filter_by(function_id=function.function_id).all()
                print(fun_obj)
                for variable in variables:
                    fun_obj.set_parameters(Property(
                        variable_name=variable.variable_name,
                        variable_type=variable.variable_type,
                        variable_description=variable.variable_description
                    ))
                    print(variable)
                else:
                    res_data.set_tools_info(tool_function=fun_obj)

        except Exception as e:
            print(e)
        finally:
            self._session.close()
            return res_data
