from app.extensions import db
from app.models.table import Table
from app.models.restaurant import Restaurant
from sqlalchemy.exc import IntegrityError


class TableService():
    @staticmethod
    def create_table(
        restaurant_id:int,
        table_number:int,
        seats:int,
        is_active:bool=True
    ):
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return None,{"error":"Restaurant not found"},404
        
        existing_table = Table.query.filter_by(
            restaurant_id=restaurant_id,
            table_number=table_number
        ).first()
        if existing_table:
            return None,{"error":"Table with this number already exists in this restaurant"},409
        
        table = Table(
            restaurant_id=restaurant_id,
            table_number=table_number,
            seats=seats,
            is_active=is_active
        )

        try:
            db.session.add(table)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None,{"error":"Table with this number already exists in this restaurant"},409
        except Exception:
            db.session.rollback()
            return None,{"error":"Creation failed"},500
        
        return table,None,201
    @staticmethod
    def get_tables_by_restaurant(restaurant_id:int,page:int = 1,limit:int  = 10):
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return None,{"error":"Restaurant not found"},404
        
        if page < 1:
            return None,{"error":"Page must be greater than or equal to 1"},400
        if limit < 1:
            return None,{"error":"Limit must be greater than or equal to 1"},400
        
        max_limit = 50
        if limit > max_limit:
            limit = max_limit
        
        try:
            query = Table.query.filter_by(restaurant_id=restaurant_id).order_by(Table.table_number)
            total = query.count()
            tables = query.offset((page-1)*limit).limit(limit).all()
            final_tables = [table.to_dict() for table in tables]
            return {
                "tables":final_tables,
                "total":total,
                "page":page,
                "limit":limit
            },None,200
        except Exception:
            return None,{"error":"Failed to retrieve tables"},500
        
    @staticmethod
    def get_table(table_id:int):
        try:
            table = db.session.get(Table,table_id)
            if not table:
                return None,{"error":"Table not found"},404
            return table,None,200
        except Exception:
            return None,{"error":"Failed to retrieve table"},500
    
    @staticmethod
    def update_table(table_id:int,restaurant_id:int,data:dict):
        try:
            table = db.session.get(Table,table_id)
            if not table:
                return None,{"error":"Table not found"},404
            if table.restaurant_id != restaurant_id:
                return None,{"error":"Table does not belong to this restaurant"},404
            if "table_number" in data:
                new_table_number = data["table_number"]
                existing_table = Table.query.filter_by(
                    restaurant_id=table.restaurant_id,
                    table_number=new_table_number
                ).first()
                if existing_table and existing_table.id != table_id:
                    return None,{"error":"Table with this number already exists in this restaurant"},409
                table.table_number = new_table_number
            
            if "seats" in data:
                table.seats = data["seats"]
            
            if "is_active" in data:
                table.is_active = data["is_active"]
            
            db.session.commit()
            return table,None,200
        except IntegrityError:
            db.session.rollback()
            return None,{"error":"Table with this number already exists in this restaurant"},409
        except Exception:
            db.session.rollback()
            return None,{"error":"Failed to update table"},500
        
    @staticmethod
    def delete_table(table_id:int,restaurant_id:int):
        try:
            table = db.session.get(Table,table_id)
            if not table:
                return {"error":"Table not found"},404
            if table.restaurant_id != restaurant_id:
                return {"error":"Table does not belong to this restaurant"},404
            db.session.delete(table)
            db.session.commit()
            return None,200
        except Exception:
            db.session.rollback()
            return {"error":"Failed to delete table"},500
        
