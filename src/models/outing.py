from . import db
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

class Outing(db.Model):
    schema_name = os.getenv('Schema')
    __tablename__ = 'outing'
    __table_args__ = {'schema': schema_name}
    idOuting = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # idPlace = db.Column(db.String, nullable=True)  # Comentado por ahora. Será obtenido de MongoDB
    idUser = db.Column(db.Integer, db.ForeignKey(f'{schema_name}.users.id'), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __init__(self, idUser, description):  # idPlace=None,
        # self.idPlace = idPlace
        self.idUser = idUser
        self.description = description

    def __repr__(self):
        return f'<Outing {self.idOuting}>'
