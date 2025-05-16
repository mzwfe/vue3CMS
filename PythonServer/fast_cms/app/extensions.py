# vue3CMS-backend/app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
cors = CORS() # 初始化CORS