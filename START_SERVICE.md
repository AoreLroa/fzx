# 服务的部署启动文档

## 服务介绍
* 目前服务仅支持三方天气查询，且该功能只有一个根据地名查询当前天气的功能。

## 服务部署
* 服务构建虚拟环境，并使用 `requirements.txt` 安装依赖。
* 根据 `config.ini` 的配置属性，配置好本地的 数据库
* 运行 `init_server.py` 文件，初始化数据库。
* 目前主服务并未完善，启用 `flask_app` 文件夹下的 `query_weather_task.py`，使用服务。