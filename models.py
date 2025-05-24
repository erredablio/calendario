# models.py
import uuid
from extensions import db

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Corrigido!
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default="common")  # 'admin' ou 'common'

    full_name = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(10), nullable=True)  # 'male', 'female', 'other'
    email = db.Column(db.String(100), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "full_name": self.full_name,
            "gender": self.gender,
            "email": self.email,
            "phone": self.phone,
            "profile_picture": self.profile_picture,
            "active": self.active
        }

class Task(db.Model):
    __tablename__ = 'task'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "event_date": self.event_date.isoformat(),
            "description": self.description,
            "created_by": self.created_by
        }
