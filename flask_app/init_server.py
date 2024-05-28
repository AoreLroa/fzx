from models.db_model import Base
from db.local_db import engine

# 创建表
Base.metadata.create_all(engine)