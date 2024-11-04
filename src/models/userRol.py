from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

bcrypt = Bcrypt()
load_dotenv()

class Role(db.Model):
    schema_name = os.getenv('Schema')
    __tablename__ = 'roles'
    __table_args__ = {'schema': schema_name}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    
    #user = db.relationship('User', backref='roles')
    
    def __init__(self, nombre):
        self.nombre = nombre