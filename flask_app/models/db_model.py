from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# 定义基类
Base = declarative_base()


# 定义FunctionRegedit类
class FunctionRegedit(Base):
    """
    函数注册器 类
    """

    __tablename__ = 'function_regedit'
    __table_args__ = {
        'comment': '函数注册表，记录所有注册的函数信息'
    }

    function_id = Column(Integer, primary_key=True, autoincrement=True, comment='函数编号，主键，自增')
    function_name = Column(String(100), nullable=False, comment='函数名称')
    function_description = Column(String(255), nullable=False, comment='描述函数的作用和含义')
    function_active = Column(Integer, default=1, nullable=False, comment='逻辑删除，1-true表示有效，0-false表示已删除')

    # 如果需要，可以定义关系
    variables = relationship('VariableRegedit', backref='function')


# 定义VariableRegedit类
class VariableRegedit(Base):
    """
    变量注册器 类
    """

    __tablename__ = 'variable_regedit'
    __table_args__ = {
        'comment': '变量表，所有注册的函数的入参都会存放在这张表'
    }

    variable_id = Column(Integer, primary_key=True, autoincrement=True, comment='变量编号，主键，自增')
    function_id = Column(Integer, ForeignKey('function_regedit.function_id'),
                         nullable=False, comment='函数编号，外键，关联 function_regedit 表的 function_id')
    variable_name = Column(String(100), nullable=False, comment='变量名称')
    variable_type = Column(String(20), nullable=False, comment='变量类型')
    variable_description = Column(String(255), comment='描述变量的作用和含义')
    variable_active = Column(Integer, default=1, nullable=False, comment='逻辑删除，1-true表示有效，0-false表示已删除')
