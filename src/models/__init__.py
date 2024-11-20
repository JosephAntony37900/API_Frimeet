#from models import user
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .userRol import Role
from .user import User
from .tag import Tag
from .favorite import Favorite
from .outing import Outing