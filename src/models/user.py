from . import db
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
from datetime import datetime
from src.models.userRol import Role
from sqlalchemy.dialects.postgresql import ARRAY  # Importar ARRAY para listas

bcrypt = Bcrypt()
load_dotenv()

class User(db.Model):
    schema_name = os.getenv('Schema')
    __tablename__ = 'users'
    __table_args__ = {'schema': schema_name}
    id = db.Column(db.Integer, primary_key=True)
    id_Rol = db.Column(db.Integer, db.ForeignKey(f'{schema_name}.roles.id'), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    premium_expiration = db.Column(db.DateTime, nullable=True)  # Para premium
    # Pa recordatorios
    eventReminder = db.Column(ARRAY(db.String), default=[])
    ContentReminder = db.Column(ARRAY(db.String), default=[])
    nameReminder = db.Column(ARRAY(db.String), default=[])

    role = db.relationship('Role', backref='users')

    def __init__(self, nombre, email, password, id_Rol):
        self.nombre = nombre
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.id_Rol = id_Rol
        self.eventReminder = []
        self.ContentReminder = []
        self.nameReminder = []

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def verificar_premium(self):
        if self.premium_expiration and datetime.utcnow() > self.premium_expiration:
            rol_nombre = "Usuarios"
            rol = Role.query.filter_by(nombre=rol_nombre).first()
            if rol:
                self.id_Rol = rol.id
                self.premium_expiration = None
                db.session.commit()

    def __repr__(self):
        return f'<User {self.nombre}>'
