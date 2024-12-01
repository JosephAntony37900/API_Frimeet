from flask import Blueprint, request
from src.controllers.tagController import crear_etiquetas, obtener_eventos_por_etiqueta, eliminar_tags, obtener_todas_las_etiquetas, obtener_lugares_por_etiqueta, obtener_tags_event, obtener_tags_place, obtener_lugar_por_tipo_y_etiquetas
from flask_jwt_extended import jwt_required

etiqueta_blueprint = Blueprint('etiquetas', __name__)

@etiqueta_blueprint.route('/tags', methods=['POST'])
def crear_etiquetas_ruta():
    data = request.get_json()
    return crear_etiquetas(data)

@etiqueta_blueprint.route('/tags/<int:tag_id>/places', methods=['GET']) 
@jwt_required() 
def obtener_lugares_por_etiqueta_ruta(tag_id): 
    return obtener_lugares_por_etiqueta(tag_id)

@etiqueta_blueprint.route('/tags/<int:tag_id>/events', methods=['GET'])
@jwt_required()
def obtener_eventos_por_etiqueta_ruta(tag_id):
    return obtener_eventos_por_etiqueta(tag_id)

@etiqueta_blueprint.route('/tags/<int:tag_id>/delete', methods=['DELETE'])
@jwt_required()
def eliminar_tag_ruta(tag_id):
    return eliminar_tags(tag_id)

@etiqueta_blueprint.route('/tags', methods=['GET'])
@jwt_required()
def obtener_todas_las_etiquetas_ruta():
    return obtener_todas_las_etiquetas()

@etiqueta_blueprint.route('/tags/events', methods=['GET'])
@jwt_required()
def obtener_tags_event_ruta():
    return obtener_tags_event()

@etiqueta_blueprint.route('/tags/places', methods=['GET'])
@jwt_required()
def obtener_tags_place_ruta():
    return obtener_tags_place()

@etiqueta_blueprint.route('/tags/places/filter', methods=['POST'])
@jwt_required()
def obtener_lugar_por_tipo_y_etiquetas_ruta():
    return obtener_lugar_por_tipo_y_etiquetas()
