# services/user_service.py
from repositories.user_repository import UserRepository
from extensions import bcrypt

class UserService:
    @staticmethod
    @staticmethod
    def update_user(user_id: str, data: dict, current_user_role: str = "common") -> bool:
        """Atualiza informações de um usuário, garantindo que apenas admin possa modificar roles."""
        user = UserRepository.get_by_id(user_id)
        if not user:
            return False

        # Usuários comuns podem atualizar apenas suas próprias informações pessoais e senha
        allowed_fields = ["full_name", "gender", "email", "phone", "profile_picture", "password"]
        if current_user_role == "admin":
            allowed_fields.append("role")  # Apenas admin pode modificar roles

        for field in allowed_fields:
            if field in data:
                if field == "password":
                    user.password_hash = bcrypt.generate_password_hash(data[field]).decode("utf-8")
                else:
                    setattr(user, field, data[field])

        UserRepository.commit()
        return True
    
    @staticmethod
    def list_users():
        """Retorna todos os usuários cadastrados."""
        return UserRepository.get_all()

    @staticmethod
    def get_user_by_id(user_id: str):
        """Retorna um usuário pelo ID."""
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def deactivate_user(user_id: str) -> bool:
        """Desativa um usuário (define 'active' como False)."""
        user = UserRepository.get_by_id(user_id)
        if not user:
            return False

        user.active = False
        UserRepository.commit()
        return True
