from backend.common import api, app
from backend.resources import WebSiteInformationResource

api.add_resource(WebSiteInformationResource, '/website_info/<string:url>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
