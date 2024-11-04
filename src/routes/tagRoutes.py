from flask import Blueprint, request
from src.controllers.tagController import crear_etiqueta, asignar_etiqueta_a_lugar, obtener_lugares_por_etiqueta, eliminar_tags, obtener_todas_las_etiquetas
from flask_jwt_extended import jwt_required

etiqueta_blueprint = Blueprint('etiquetas', __name__)

@etiqueta_blueprint.route('/tags', methods=['POST'])
def crear_etiqueta_ruta():
    data = request.get_json()
    return crear_etiqueta(data)

@etiqueta_blueprint.route('/tags/<int:tag_id>/places/<string:place_id>', methods=['POST'])
@jwt_required()
def asignar_etiqueta_a_lugar_ruta(tag_id, place_id):
    return asignar_etiqueta_a_lugar(tag_id, place_id)

@etiqueta_blueprint.route('/tags/<int:tag_id>/places', methods=['GET'])
@jwt_required()
def obtener_lugares_por_etiqueta_ruta(tag_id):
    return obtener_lugares_por_etiqueta(tag_id)

@etiqueta_blueprint.route('/tags/<int:tag_id>/delete', methods=['DELETE'])
@jwt_required()
def eliminar_tag_ruta(tag_id):
    return eliminar_tags(tag_id)

@etiqueta_blueprint.route('/tags', methods=['GET'])
@jwt_required()
def obtener_todas_las_etiquetas_ruta():
    return obtener_todas_las_etiquetas()