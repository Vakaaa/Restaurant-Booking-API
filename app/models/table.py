from app.extensions import db


class table(db.Model):
    __tablename__ = "tables"

    id = db.Cloumn(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    location = db.Column(db.String(255),nullable=False)
    is_active = db.Column(db.Boolean,nullable=False,defaut=True)
