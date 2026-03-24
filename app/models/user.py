from datetime import datetime,timezone
from app.extensions import db


class User(db.Model):
    __tablename__="users"

    id = db.Column(db.Integer,primary_key=True)
    full_name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(255),unique=True,nullable=False,index=True)
    password_hash = db.Column(db.String(255),nullable=False)
    created_at = db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc),nullable=False)
    role = db.Column(db.String(255),nullable=False,default="user")
    
    reservations = db.relationship(
        "Reservation",
        back_populates="users",
        cascade="all,delete-orphan"
        )
    def __repr__(self):
        return f"User {self.email}"
    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
        }
