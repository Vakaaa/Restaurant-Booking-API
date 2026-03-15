from app.extensions import db
from datetime import datetime,timezone

class Restaurant(db.Model):
    __tablename__ = "restaurants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    open_time = db.Column(db.Time, nullable=False)
    close_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    tables = db.relationship(
    "Table",
    back_populates="restaurant",
    cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Restaraunt {self.name}"