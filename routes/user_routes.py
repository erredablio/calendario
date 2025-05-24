# routes/user_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from repositories.user_repository import UserRepository
from services.user_service import UserService

user_bp = Blueprint("users", __name__)

@user_bp.route("/users/<user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    """Permite que usuários alterem suas próprias informações, mas só admins podem mudar roles."""
    current_user_id = get_jwt_identity()
    current_user = UserRepository.get_by_id(current_user_id)

    if not current_user or (current_user.role != "admin" and current_user.id != user_id):
        return jsonify({"msg": "Acesso negado"}), 403

    data = request.get_json()

    # Usuários comuns podem atualizar apenas suas próprias informações
    allowed_fields = ["full_name", "gender", "email", "phone", "profile_picture", "password"]
    if current_user.role == "admin":
        allowed_fields.append("role")  # Apenas admin pode modificar roles

    updates = {key: data[key] for key in allowed_fields if key in data}

    success = UserService.update_user(user_id, data, current_user.role)

    return jsonify({"msg": "Usuário atualizado"}), 200 if success else ({"msg": "Erro na atualização"}, 400)

@user_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    """Lista todos os usuários do sistema. Apenas admins podem acessar."""
    current_user_id = get_jwt_identity()
    current_user = UserRepository.get_by_id(current_user_id)

    if not current_user or current_user.role != "admin":
        return jsonify({"msg": "Acesso negado"}), 403

    users = UserService.list_users()
    return jsonify([user.to_dict() for user in users]), 200


