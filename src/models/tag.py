from . import db
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

class Tag(db.Model):
    schema_name = os.getenv('Schema')
    __tablename__ = 'tags'
    __table_args__ = {'schema': schema_name}
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    
    def __init__(self, nombre):
        self.nombre = nombre
        
    def __repr__(self):
        return f'<Tag {self.name}>'