from app.extensions import db
from datetime import datetime,timezone

class Table(db.Model):
    __tablename__ = "tables"

    id = db.Column(db.Integer,primary_key=True)
    restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False
    )
    table_number = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    restaurant = db.relationship("Restaurant",back_populates="tables")
    reservations = db.relationship("Reservation",back_populates="tables",cascade="all,delete-orphan")

    __table_args__ = (
        db.UniqueConstraint(
            "restaurant_id",
            "table_number",
            name="uq_restaurant_table_number"
        ),
    )
    def to_dict(self):
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "table_number": self.table_number,
            "seats": self.seats,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<Table {self.table_number} in restaurant {self.restaurant_id}>"
    


    
