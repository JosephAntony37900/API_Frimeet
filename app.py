from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import config
from src.routes.userRol import roles_blueprint
from src.routes.userRoutes import usuario_blueprint
from src.routes.tagRoutes import etiqueta_blueprint
from src.models import db

def create_app(): #error aqui
    app = Flask(__name__)
    app.config.from_object(config['development'])
    db.init_app(app)
    migrate= Migrate(app, db)
    jwt = JWTManager(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(roles_blueprint, name='usuario_blueprint')
    app.register_blueprint(usuario_blueprint, name='roles_blueprint')
    app.register_blueprint(etiqueta_blueprint, name='etiqueta_blueprint')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
