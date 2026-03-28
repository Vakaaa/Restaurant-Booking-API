from app.extensions import db
from app.models.restaurant import Restaurant
from sqlalchemy.exc import IntegrityError
import datetime

class RestaurantService():
    @staticmethod
    def create_restaurant(
        name:str,
        open_time:datetime.time,
        close_time:datetime.time,
        address:str,
        phone:str | None = None,
        description:str |None = None
):
        name = name.strip()
        address = address.strip()
        existing_restaurant = Restaurant.query.filter_by(name=name).first()
        if existing_restaurant:
            return None,{"error":"Restaurant with this name is already exist"},409
        restaurant = Restaurant(
            name = name,
            open_time=open_time,
            close_time = close_time,
            address = address,
            phone = phone,
            description = description
        )

        try:
            db.session.add(restaurant)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None,{"error":"Restaurant with this name is already exist"},409
        except Exception:
            db.session.rollback()
            return None,{"error":"Creation failed"},500
        
        return restaurant,None,201
        
    @staticmethod
    def get_all_restaurants(page:int = 1,limit:int = 10):
        if page < 1:
            return None,{"error":"Page must be greater than or equal to 1"},400
        if limit < 1:
            return None,{"error":"Limit must be greater than or equal to 1"},400
        
        max_limit = 50
        if limit > max_limit:
            limit = max_limit
        

        try:
            query = Restaurant.query.order_by(Restaurant.name)
            total = query.count()
            restaurants = query.offset((page-1)*limit).limit(limit).all()
            final_restaurants = [restaurant.to_dict() for restaurant in restaurants]
            return {
                "restaurants":final_restaurants,
                "pagination":{
                    "page":page,
                    "limit":limit,
                    "total":total,
                    "pages":(total + limit -1)//limit
                }
            },None,200
        except Exception:
            return None,{"error":"Failed to fetch restaurants"},500
    @staticmethod
    def get_restaurant(restaurant_id):
        try:
            restaurant = db.session.get(Restaurant,restaurant_id)
            if not restaurant:
                return None,{"error":"Restaurant not found"},404
            return restaurant,None,200
        except Exception:
            return None,{"error":"Server error"},500

