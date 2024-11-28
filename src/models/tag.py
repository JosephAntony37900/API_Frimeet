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
    tagsEvent = db.Column(db.String(50), nullable=True)
    tagsPlace = db.Column(db.String(50), nullable=True)
    
    def __init__(self, tagsEvent=None, tagsPlace=None):
        self.tagsEvent = tagsEvent
        self.tagsPlace = tagsPlace

    def __repr__(self):
        return f'<Tag {self.id}>'
