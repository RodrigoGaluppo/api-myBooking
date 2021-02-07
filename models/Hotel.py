from sql_alchemy import database


class HotelModel(database.Model):

    __tablename__ = "hotels"

    hotel_id = database.Column(database.Integer,primary_key=True,nullable=False, unique=True, autoincrement=True)
    name = database.Column(database.String(80))
    stars = database.Column(database.Float(precision=1))
    price = database.Column(database.Float(precision=2))
    city = database.Column(database.String(80))
    site_id = database.Column(database.Integer,database.ForeignKey("sites.site_id"))
    site = database.relationship("SiteModel")

    def __init__(self,name,stars,price,city,site_id):
        self.name = name
        self.stars = stars
        self.price = price
        self.city = city
        self.site_id = site_id

    def json(self):
        return {
            'hotel_id':self.hotel_id,
            'name':self.name,
            'stars':self.stars,
            'price':self.price,
            'city':self.city,
            "site_id":self.site_id
        }
    
    @classmethod
    def find_hotel(cls,hotel_id):
        hotel = cls.query.filter_by(hotel_id = hotel_id).first()
        if hotel:
            return hotel
        else:
            return None

    def save_hotel(self):
        database.session.add(self)
        database.session.commit()
    
    def update_hotel(self,name,stars,price,city):
        self.name = name
        self.stars = stars
        self.price = price
        self.city = city

    def delete_hotel(self):
        database.session.delete(self)
        database.session.commit()
        