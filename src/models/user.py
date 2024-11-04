from . import db
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

bcrypt = Bcrypt()
load_dotenv()

class User(db.Model):
    schema_name = os.getenv('Schema')
    __tablename__ = 'users'
    __table_args__ = {'schema': schema_name}
    id = db.Column(db.Integer, primary_key=True)
    id_Rol = db.Column(db.Integer, db.ForeignKey(f'{schema_name}.roles.id'), nullable=False)  # Especifica el esquema
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    role = db.relationship('Role', backref='users')

    def __init__(self, nombre, email, password, id_Rol):
        self.nombre = nombre
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.id_Rol = id_Rol

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.nombre}>'
