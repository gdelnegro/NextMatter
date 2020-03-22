from flask import Flask
from flask_restful import Api

from backend.resources import WebSiteInformationResource

APP_NAME = "website_analyzer"

app = Flask(APP_NAME)
api = Api(app)

api.add_resource(WebSiteInformationResource, '/website_info/<string:url>')

if __name__ == '__main__':
    app.run(debug=True)
