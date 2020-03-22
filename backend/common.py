from flask import Flask
from flask_caching import Cache
from flask_restful import Api

APP_NAME = "website_analyzer"
CACHE_CONFIG = {
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": 86400,  # 24 hours in seconds,
    "CACHE_REDIS_URL": "redis://cache:6379/0"
}

app = Flask(APP_NAME)
api = Api(app)
cache = Cache(config=CACHE_CONFIG, app=app)
