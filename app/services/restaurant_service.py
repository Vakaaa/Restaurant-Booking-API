from app.extensions import db
from app.models.restaurant import Restaurant
from sqlalchemy.exc import IntegrityError
import datetime

class CreateRestaurant():
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
        

