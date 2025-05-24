# app.py
from flask import Flask
from config import Config
from extensions import db, bcrypt, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializa as extensões
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Registra os blueprints
    from routes.auth_routes import auth_bp
    from routes.task_routes import task_bp
    from routes.user_routes import user_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(user_bp)
    
    # Cria as tabelas imediatamente após a criação do app, dentro de um app context
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
