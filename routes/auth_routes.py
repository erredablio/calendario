# routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from services.auth_service import AuthService
from repositories.user_repository import UserRepository

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    """Registra um novo usuário com mais informações."""
    data = request.get_json()
    username, password = data.get("username"), data.get("password")
    full_name, gender, email, phone, profile_picture = (
        data.get("full_name"), data.get("gender"), data.get("email"),
        data.get("phone"), data.get("profile_picture")
    )
    role = data.get("role", "common")  # Apenas admin pode alterar role depois

    if not username or not password:
        return jsonify({"msg": "Username e password são obrigatórios"}), 400
    if role not in ["admin", "common"]:
        return jsonify({"msg": "Role inválida! Use 'admin' ou 'common'"}), 400

    user = AuthService.register_user(username, password, role, full_name, gender, email, phone, profile_picture)
    if not user:
        return jsonify({"msg": "Usuário já existe"}), 400

    return jsonify({"msg": "Usuário registrado com sucesso", "role": role}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Autentica o usuário e retorna um token JWT válido.
    JSON esperado:
    {
      "username": "usuario",
      "password": "senha123"
    }
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = AuthService.authenticate(username, password)

    if not user:
        return jsonify({"msg": "Credenciais inválidas"}), 401

    # Agora armazenamos apenas o ID do usuário como string no token JWT
    token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": token}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Obtém as informações do usuário autenticado.
    """
    user_identity = get_jwt_identity()
    user = UserRepository.get_by_id(user_identity)

    if not user:
        return jsonify({"msg": "Usuário não encontrado"}), 404

    return jsonify(user.to_dict()), 200
