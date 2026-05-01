from app.models.reservation import Reservation
from app.models.table import Table
from app.extensions import db

class ReservationService:
    @staticmethod
    def create_reservation(user_id, table_id, guest_name, guests_count, reservation_start, reservation_end):
        table = Table.query.get(table_id)
        if not table:
            return None, {"message": "Table not found"}, 404
        
        if not table.is_active:
            return None, {"message": "Table is inactive"}, 400

        
        if reservation_start >= reservation_end:
            return None, {"message": "Reservation start time must be before end time"}, 400
        
        if guests_count > table.seats:
            return None, {"message": "Guests count exceeds table capacity"}, 400

        overlapping_reservations = Reservation.query.filter(
            Reservation.table_id == table_id,
            Reservation.reservation_start < reservation_end,
            Reservation.reservation_end > reservation_start
        ).all()
        
        if overlapping_reservations:
            return None, {"message": "The table is already reserved for the selected time slot"}, 400
        
        # Create the reservation
        new_reservation = Reservation(
            user_id=user_id,
            table_id=table_id,
            guest_name=guest_name,
            guests_count=guests_count,
            reservation_start=reservation_start,
            reservation_end=reservation_end
        )
        try:
            db.session.add(new_reservation)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return None, {"message": "Failed to create reservation"}, 500

        return new_reservation, None, 201
    @staticmethod
    def get_reservations_by_user(user_id, page=1, limit=10):
        if page < 1:
            return None, {"message": "Page must be greater than or equal to 1"}, 400
        if limit < 1:
            return None, {"message": "Limit must be greater than or equal to 1"}, 400
        
        max_limit = 50
        if limit > max_limit:
            limit = max_limit
        
        query = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.reservation_start.desc())
        total = query.count()
        reservations = query.offset((page - 1) * limit).limit(limit).all()
        result = {
            "reservations": [reservation.to_dict() for reservation in reservations],
            "total": total,
            "page": page,
            "limit": limit
        }
        return result, None, 200
    