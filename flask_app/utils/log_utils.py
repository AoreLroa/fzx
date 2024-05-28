import datetime
import inspect
from threading import Thread

from utils.mate_class import SingletonMeta
from utils.auto_increment_link_queue import LinkQueue


class LogMessage:

    def __init__(
            self,
            date_formate: str = "%Y-%m-%d %H:%M:%S",
            log_level: str = None,
            log_file_path: str = None,
            log_msg: str = None,
            log_stack: str = None
    ):
        """
        :param date_formate: 日志信息产生的时间
        :param log_level: 日志级别
        :param log_file_path: 日志信息要写入的文件路径
        :param log_msg: 带写入的日志信息
        :param log_stack: 日志的调用栈路径
        """
        self._log_date = datetime.datetime.now().strftime(date_formate)
        self._log_level = log_level.upper()
        self._log_file_path = log_file_path
        self._log_msg = log_msg
        self._log_stack = log_stack

    def __str__(self):
        """
        日志消息体的直接展示格式
        :return:
        """
        return f"{self.log_formate_date} | {self.log_level} |{self.log_stack}: {self.log_msg}"

    @property
    def log_file_path(self):
        return self._log_file_path

    @property
    def log_formate_date(self):
        return self._log_date

    @property
    def log_level(self):
        return self._log_level

    @property
    def log_stack(self):
        return self._log_stack

    @property
    def log_msg(self):
        return self._log_msg


class WYLOG(metaclass=SingletonMeta):
    """
    日志类
        单例日志类
    """
    # 存储待写入文件中的消息的队列
    _MSG_QUEUE = LinkQueue()

    # 日志的严重级别，从低到高
    _LOG_LEVEL = ["DEBUG", "INFO", "WARRING", "ERROR", "CRITICAL"]
    # 日志阀门，管理日志文件写入的日志信息级别，默认是 DEBUG 级别
    _LOG_VALVE = "DEBUG"
    # 日志级别对应的颜色
    _LEVEL_COLOR_MAPPING = {
        "CRITICAL": "\033[41m",  # 红色背景
        "ERROR": "\033[91m",  # 红色
        "SUCCESS": "\033[92m",  # 绿色
        "WARRING": "\033[93m",  # 黄色
        "DEBUG": "\033[94m",  # 蓝色
        "INFO": "\033[97m",  # 白色
    }

    def __init__(self, project_root):
        self._project_root = project_root

    def print_log_to_control(self, log_obj: LogMessage):
        print_color = self._LEVEL_COLOR_MAPPING[log_obj.log_level]
        print_msg = (f"{log_obj.log_formate_date} | {log_obj.log_level} |"
                     f"{log_obj.log_stack}: {log_obj.log_msg}")
        print(print_color + print_msg)

    def debug(self, file_path, msg):
        """
        记录 debug 级别的日志信息
        :param file_path:
        :param msg:
        :return:
        """
        frame = inspect.stack()[1]
        log_stack = f"{frame.filename.replace(self._project_root, '')}-{frame.lineno}"
        msg_obj = LogMessage(log_file_path=file_path, log_level="DEBUG", log_msg=msg, log_stack=log_stack)
        self._MSG_QUEUE.add(value=msg_obj)
        self.print_log_to_control(log_obj=msg_obj)

    def info(self, file_path, msg):
        """
        记录 info 级别的日志信息
        :param file_path:
        :param msg:
        :return:
        """
        frame = inspect.stack()[1]
        log_stack = f"{frame.filename.replace(self._project_root, '')}-{frame.lineno}"
        msg_obj = LogMessage(log_file_path=file_path, log_level="INFO", log_msg=msg, log_stack=log_stack)
        self._MSG_QUEUE.add(value=msg_obj)
        self.print_log_to_control(log_obj=msg_obj)

    def warring(self, file_path, msg):
        """
        记录 warring 级别的日志信息
        :param file_path:
        :param msg:
        :return:
        """
        frame = inspect.stack()[1]
        log_stack = f"{frame.filename.replace(self._project_root, '')}-{frame.lineno}"
        msg_obj = LogMessage(log_file_path=file_path, log_level="WARRING", log_msg=msg, log_stack=log_stack)
        self._MSG_QUEUE.add(value=msg_obj)
        self.print_log_to_control(log_obj=msg_obj)

    def error(self, file_path, msg):
        """
        记录 error 级别的日志信息
        :param file_path:
        :param msg:
        :return:
        """
        frame = inspect.stack()[1]
        log_stack = f"{frame.filename.replace(self._project_root, '')}-{frame.lineno}"
        msg_obj = LogMessage(log_file_path=file_path, log_level="ERROR", log_msg=msg, log_stack=log_stack)
        self._MSG_QUEUE.add(value=msg_obj)
        self.print_log_to_control(log_obj=msg_obj)

    def critical(self, file_path, msg):
        """
        记录 critical 级别的日志信息
        :param file_path:
        :param msg:
        :return:
        """
        frame = inspect.stack()[1]
        log_stack = f"{frame.filename.replace(self._project_root, '')}-{frame.lineno}"
        msg_obj = LogMessage(log_file_path=file_path, log_level="CRITICAL", log_msg=msg, log_stack=log_stack)
        self._MSG_QUEUE.add(value=msg_obj)
        self.print_log_to_control(log_obj=msg_obj)
