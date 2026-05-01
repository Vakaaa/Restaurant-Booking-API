from app.extensions import db
from datetime import datetime,timezone

class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id",ondelete="CASCADE"),
        nullable =False
    )
    table_id = db.Column(
        db.Integer,
        db.ForeignKey("tables.id",ondelete="CASCADE"),
        nullable = False
    )

    guest_name = db.Column(db.String(255), nullable=False)
    guests_count = db.Column(db.Integer, nullable=False)

    reservation_start = db.Column(db.DateTime,nullable=False,index=True)
    reservation_end = db.Column(db.DateTime,nullable=False,index=True)

    status = db.Column(db.String(20), nullable=False, default="confirmed")
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    users = db.relationship("User", back_populates="reservations")
    tables = db.relationship("Table", back_populates="reservations")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "table_id": self.table_id,
            "guest_name": self.guest_name,
            "guests_count": self.guests_count,
            "reservation_start": self.reservation_start.isoformat(),
            "reservation_end": self.reservation_end.isoformat(),
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<Reservation {self.id} table={self.table_id}>"
