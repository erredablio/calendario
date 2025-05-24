# routes/task_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from repositories.user_repository import UserRepository
from services.task_service import TaskService

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """
    Cria uma tarefa única.
    JSON esperado:
    {
        "event_date": "YYYY-MM-DD",
        "description": "Descrição do evento"
    }
    """
    data = request.get_json()
    event_date = data.get('event_date')
    description = data.get('description')
    if not event_date or not description:
        return jsonify({"msg": "event_date e description são obrigatórios"}), 400

    user_identity = get_jwt_identity()
    task = TaskService.create_single_task(event_date, description, user_identity)
    if not task:
        return jsonify({"msg": "Formato de data inválido"}), 400
    return jsonify({"msg": "Tarefa criada", "task_id": task.id}), 201

@task_bp.route('/tasks/bulk', methods=['POST'])
@jwt_required()
def create_bulk_tasks():
    """
    Cria tarefas em massa.
    JSON esperado:
    {
        "event_date": "YYYY-MM-DD",
        "final_event_date": "YYYY-MM-DD",
        "description": "Descrição do evento recorrente",
        "frequency": "D"  // Valores permitidos: D, S, Q, M, A
    }
    """
    data = request.get_json()
    event_date = data.get("event_date")
    final_event_date = data.get("final_event_date")
    description = data.get("description")
    frequency = data.get("frequency")

    if not all([event_date, final_event_date, description, frequency]):
        return jsonify({"msg": "Todos os campos são obrigatórios"}), 400

    user_identity = get_jwt_identity()
    task_ids = TaskService.create_bulk_tasks(
        event_date, final_event_date, description, frequency, user_identity
    )
    if task_ids is None:
        return jsonify({"msg": "Parâmetros inválidos ou data final anterior à data inicial"}), 400
    return jsonify({"msg": "Tarefas em massa criadas", "task_ids": task_ids}), 201

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def list_tasks():
    """
    Lista as tarefas:
      - Administradores veem todas;
      - Usuários comuns veem somente as suas.
    """
    user_identity = get_jwt_identity()
    tasks = TaskService.list_tasks(user_identity)
    return jsonify(tasks), 200

@task_bp.route('/tasks/<task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id: str):
    """
    Retorna os detalhes de uma tarefa específica.
    Apenas o criador ou um administrador pode acessar.
    """
    user_identity = get_jwt_identity()
    task = TaskService.get_task(task_id)
    if not task:
        return jsonify({"msg": "Tarefa não encontrada"}), 404

    user = UserRepository.get_by_id(user_identity)  # Recupera o objeto usuário pelo ID
    if user.role != 'admin' and task.created_by != user.id:
        return jsonify({"msg": "Acesso negado"}), 403
    return jsonify(task.to_dict()), 200

@task_bp.route('/tasks/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id: str):
    """
    Atualiza uma tarefa.
    JSON esperado (todos os campos são opcionais):
    {
        "event_date": "YYYY-MM-DD",
        "description": "Nova descrição",
        "created_by": "<novo_user_id>"  // Somente para administradores
    }
    """
    user_identity = get_jwt_identity()
    task = TaskService.get_task(task_id)
    if not task:
        return jsonify({"msg": "Tarefa não encontrada"}), 404

    data = request.get_json()
    success = TaskService.update_task(task, data, user_identity)
    if not success:
        return jsonify({"msg": "Erro na atualização ou acesso negado"}), 400
    return jsonify({"msg": "Tarefa atualizada"}), 200

@task_bp.route('/tasks/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id: str):
    """
    Deleta uma tarefa.
    Apenas o criador ou um administrador pode deletar a tarefa.
    """
    user_identity = get_jwt_identity()
    task = TaskService.get_task(task_id)
    if not task:
        return jsonify({"msg": "Tarefa não encontrada"}), 404
    success = TaskService.delete_task(task, user_identity)
    if not success:
        return jsonify({"msg": "Acesso negado"}), 403
    return jsonify({"msg": "Tarefa deletada"}), 200
