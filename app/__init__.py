from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configurações do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpdesk.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
    
    db.init_app(app)
    
    # Registrar blueprints
    from app.routes import main_bp
    from app.routes.usuarios import usuarios_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(usuarios_bp)
    
    return app
