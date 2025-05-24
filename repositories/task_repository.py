# repositories/task_repository.py
from models import Task
from extensions import db

class TaskRepository:
    @staticmethod
    def create(event_date, description, created_by):
        task = Task(event_date=event_date, description=description, created_by=created_by)
        db.session.add(task)
        db.session.flush()  # Garante que o ID esteja disponível antes do commit
        return task

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def get_all():
        return Task.query.all()

    @staticmethod
    def get_by_user(user_id: str):
        return Task.query.filter_by(created_by=user_id).all()

    @staticmethod
    def get_by_id(task_id: str):
        return Task.query.filter_by(id=task_id).first()

    @staticmethod
    def delete(task):
        db.session.delete(task)
        db.session.commit()
