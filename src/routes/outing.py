from flask import Blueprint, request
from src.controllers.outing import crear_salida, obtener_salidas, eliminar_salida, obtener_salida_por_id

salida_blueprint = Blueprint('salidas', __name__)

@salida_blueprint.route('/outings', methods=['POST'])
def crear_salida_ruta():
    data = request.get_json()
    return crear_salida(data)

@salida_blueprint.route('/outings', methods=['GET'])
def obtener_salidas_ruta():
    return obtener_salidas()

@salida_blueprint.route('/outings/<int:idOuting>', methods=['GET'])
def obtener_salida_por_id_ruta(idOuting):
    return obtener_salida_por_id(idOuting)

@salida_blueprint.route('/outings/<int:idOuting>', methods=['DELETE'])
def eliminar_salida_ruta(idOuting):
    return eliminar_salida(idOuting)
