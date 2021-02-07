from flask_restful import Resource,reqparse
from models.Site import SiteModel

class Sites(Resource):
    def get(self):
        return {"sites":[site.json() for site in SiteModel.query.all()]}
    
    def post(self):
        arguments = reqparse.RequestParser()
        arguments.add_argument("url",type=str,required=True,help="the filed url is required")
        data = arguments.parse_args()
        
        siteExists = SiteModel.find_site(data.get("url"))
        if siteExists:
            return {"message":"site url was already taken"},400
        
        site = SiteModel(**data)
        try:
            site.save_site()
            return site.json()
        except(e):
            print(e)
            return {"message":"an internal server error ocurred"},500

class Site(Resource):
    def get(self,url):
        site = SiteModel.find_site(url)
        if site:
            return site.json()
        return {"message":"site was not found"},404

        
    def delete(self,url):
        site = SiteModel.find_site(url)
        if site:
            site.delete_site()
            return {"message":"site has been deleted"},200
        return {"message":"site was not found"},404