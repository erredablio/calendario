# services/auth_service.py
from models import User
from repositories.user_repository import UserRepository
from extensions import bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

class AuthService:
    @staticmethod
    def register_user(username: str, password: str, role: str = 'common', full_name: str = None, gender: str = None,
                      email: str = None, phone: str = None, profile_picture: str = None):
        """ Registra um novo usuário com senha criptografada e informações adicionais. """
        if UserRepository.get_by_username(username) or (email and UserRepository.get_by_email(email)):
            return None  # Usuário já existe

        # Gera hash da senha e decodifica para string
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        return UserRepository.create(username, password_hash, role, full_name, gender, email, phone, profile_picture)

    @staticmethod
    def authenticate(username: str, password: str):
        """ Autentica um usuário e retorna o objeto User, não o token. """
        user = UserRepository.get_by_username(username)
        if user and bcrypt.check_password_hash(user.password_hash, password):  # Correção na verificação de senha
            return user  # Retorna o objeto User

        return None  # Retorna None se a autenticação falhar

    @staticmethod
    def generate_token(user: User):
        """ Gera um token JWT válido para o usuário autenticado. """
        expires = timedelta(days=1)
        token = create_access_token(identity=str(user.id), expires_delta=expires)
        return token
