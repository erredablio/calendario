# services/task_service.py
from datetime import datetime, timedelta
from models import Task
from repositories.task_repository import TaskRepository
from repositories.user_repository import UserRepository
from utils.date_utils import parse_date

class TaskService:
    @staticmethod
    def create_single_task(event_date_str: str, description: str, user_id: str):
        event_date = parse_date(event_date_str)
        if not event_date:
            return None
        task = TaskRepository.create(event_date, description, user_id)
        TaskRepository.commit()
        return task

    @staticmethod
    def create_bulk_tasks(event_date_str: str, final_event_date_str: str, description: str, frequency: str, user_id: str):
        start_date = parse_date(event_date_str)
        final_date = parse_date(final_event_date_str)
        if not start_date or not final_date or final_date < start_date:
            return None

        freq_map = {'D': 1, 'S': 7, 'Q': 15, 'M': 30, 'A': 365}
        if frequency not in freq_map:
            return None

        delta_days = freq_map[frequency]
        created_task_ids = []
        current_date = start_date

        while current_date <= final_date:
            task = TaskRepository.create(current_date, description, user_id)
            created_task_ids.append(task.id)
            current_date += timedelta(days=delta_days)

        TaskRepository.commit()
        return created_task_ids

    @staticmethod
    def list_tasks(user_identity: str):
        """Lista as tarefas de acordo com a permissão do usuário."""
        user = UserRepository.get_by_id(user_identity)  # Recupera o usuário pelo ID armazenado no JWT
        if not user:
            return []  # Se o usuário não existir, retorna uma lista vazia

        tasks = TaskRepository.get_all() if user.role == "admin" else TaskRepository.get_by_user(user.id)

        return [task.to_dict() for task in tasks]  # Converte os objetos Task para dicionários


    @staticmethod
    def get_task(task_id: str):
        return TaskRepository.get_by_id(task_id)

    @staticmethod
    def update_task(task: Task, data: dict, current_user_identity: str) -> bool:
        """Atualiza uma tarefa, verificando permissões corretamente."""
        user = UserRepository.get_by_id(current_user_identity)  # Recupera o usuário pelo ID
        if not user:
            return False

        if user.role != "admin" and task.created_by != user.id:
            return False

        if "event_date" in data:
            new_date = parse_date(data["event_date"])
            if not new_date:
                return False
            task.event_date = new_date

        if "description" in data:
            task.description = data["description"]

        # Apenas administradores podem alterar o autor da tarefa
        if user.role == "admin" and "created_by" in data:
            new_user_id = data["created_by"]
            if not UserRepository.get_by_id(new_user_id):
                return False
            task.created_by = new_user_id

        TaskRepository.commit()
        return True

    @staticmethod
    def delete_task(task: Task, current_user_identity: str) -> bool:
        """Deleta uma tarefa verificando permissões corretamente."""
        user = UserRepository.get_by_id(current_user_identity)  # Recupera o usuário pelo ID
        if not user:
            return False

        if user.role != "admin" and task.created_by != user.id:
            return False

        TaskRepository.delete(task)
        return True
