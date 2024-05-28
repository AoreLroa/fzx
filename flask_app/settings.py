import os
import configparser

# 项目根目录的绝对路径
BASE_PATH = os.path.dirname(__file__)

# 读取 ini 中的配置信息
config = configparser.ConfigParser()

# 读取配置文件
config.read(f"{BASE_PATH}/config.ini", encoding="utf-8")

# 获取 智谱清言 的配置信息
zhipuai_config = config['zhipuai_config']
# 获取 openai 的配置信息
openai_config = config['openai_config']
# 获取 三方天气 的配置信息
weather_com_config = config["weather_com"]
# 获取数据库链接属性
local_mysql_config = config["mysql"]

# zhipuai
ZHIPU_API_KEY = zhipuai_config["API_KEY"]  # API KEY

# openai
OPEN_API_KEY = openai_config["API_KEY"]  # API KEY

# 三方天气
WEATHER_KEY = weather_com_config["API_KEY"]  # API KEY
WEATHER_DOMAIN = weather_com_config["DOMAIN"]  # 域名
