from flask_restful import Resource
from backend.models import WebSiteInformation


class WebSiteInformationResource(Resource):

    def get(self, url):
        website = WebSiteInformation(url)
        website.get_website_information()

        return website.to_dict()
