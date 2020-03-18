from flask_restful import Resource


class WebSiteInformation(Resource):

    def get(self):
        return {'hello': 'world'}

    def _analyze_website(self, url):
        pass