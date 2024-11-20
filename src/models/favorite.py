from . import db
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

class Favorite(db.Model):
    schema_name = os.getenv('Schema')
    __tablename__ = 'favorite'
    __table_args__ = {'schema': schema_name}

    idFavorite = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idPlace = db.Column(db.String, nullable=False)  # ID del lugar en MongoDB
    idUser = db.Column(db.Integer, db.ForeignKey(f'{schema_name}.users.id'), nullable=False)

    def __init__(self, idUser, idPlace):
        self.idPlace = idPlace
        self.idUser = idUser

    def __repr__(self):
        return f'<Favorite {self.idFavorite}>'
