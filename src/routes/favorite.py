from flask import Blueprint, request
from src.controllers.favorite import crear_favorito, obtener_favoritos, eliminar_favorito

favorito_blueprint = Blueprint('favoritos', __name__)

@favorito_blueprint.route('/favorite', methods=['POST'])
def crear_favorito_ruta():
    data = request.get_json()
    return crear_favorito()

@favorito_blueprint.route('/favorites', methods=['GET'])
def obtener_favoritos_ruta():
    return obtener_favoritos()

@favorito_blueprint.route('/favorites/<int:idFavorite>', methods=['DELETE'])
def eliminar_favorito_ruta(idFavorite):
    return eliminar_favorito(idFavorite)
