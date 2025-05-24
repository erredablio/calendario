# repositories/user_repository.py
import uuid
from models import User
from extensions import db

class UserRepository:
    @staticmethod
    def create(username: str, password_hash: str, role: str = "common",
            full_name: str = None, gender: str = None, email: str = None,
            phone: str = None, profile_picture: str = None) -> User:
        """Cria um novo usuário no banco de dados."""
        user = User(
            id=str(uuid.uuid4()),  # Gera um UUID corretamente!
            username=username,
            password_hash=password_hash,
            role=role,
            full_name=full_name,
            gender=gender,
            email=email,
            phone=phone,
            profile_picture=profile_picture,
            active=True
        )
        
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def commit():
        db.session.commit()
    
    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(user_id: str) -> User:
        return User.query.filter_by(id=user_id).first()
    
    @staticmethod
    def get_by_username(username: str) -> User:
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_by_email(email: str) -> User:
        return User.query.filter_by(email=email).first()




