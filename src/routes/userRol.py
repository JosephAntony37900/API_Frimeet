from flask import Blueprint, request
from src.controllers.userRol import crear_rol, obtener_roles, eliminar_rol
from flask_jwt_extended import jwt_required

roles_blueprint = Blueprint('usuarios', __name__)

@roles_blueprint.route('/roles', methods=['POST'])
def crear_rol_ruta():
    data = request.get_json()
    return crear_rol(data)

@roles_blueprint.route('/ver_roles', methods=['GET'])
@jwt_required()
def obtener_roles_ruta():
    return obtener_roles()

@roles_blueprint.route('/roles/<int:idRol>', methods=['DELETE'])
@jwt_required()
def eliminar_roles_ruta(idRol):
    return eliminar_rol(idRol)