from flask import Flask
from flask_restful import Api

from backend.resources import WebSiteInformation

APP_NAME = "website_analyzer"

app = Flask(APP_NAME)
api = Api(app)

api.add_resource(WebSiteInformation, '/website_info')

if __name__ == '__main__':
    app.run(debug=True)
