from werkzeug.security import check_password_hash,generate_password_hash
from flask_jwt_extended import create_access_token



from app.extensions import db
from app.models import User


class AuthService:
    @staticmethod
    def register(full_name:str,email:str,password:str):
        email = email.strip().lower()
        full_name = full_name.strip()
        password = password.strip()

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return None,{"message":"Email is already existed"},409
        
        password_hash = generate_password_hash(password)

        user = User(
            full_name=full_name,
            email=email,
            password_hash = password_hash
        )
        db.session.add(user)
        db.session.commit()

        return user, None ,201
    
    @staticmethod
    def login(email:str,password:str):
        email = email.strip().lower()
        password = password.strip()
        
        existing_user = User.query.filter_by(email=email).first()

        if not existing_user:
            return None,{"message":"Invalid email or password"},401
        if not check_password_hash(existing_user.password_hash,password):
            return None,{"message":"Invalid email or password"},401
        

        acces_token = create_access_token(identity=str(existing_user.id))

        return {
            "access_token":acces_token,
            "user":existing_user.to_dict(),
        },None,200
    


    @staticmethod
    def get_user_by_id(user_id: int):
        return User.query.get(user_id)
        


