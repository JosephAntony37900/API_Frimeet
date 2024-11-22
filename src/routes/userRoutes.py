from flask import Blueprint, request
from src.controllers.userController import crear_usuario, crear_usuario_base, login_usuario, obtener_usuario,eliminar_usuario, actualizar_rol_premium, actualizar_usuario, add_reminder, obtener_recordatorios
from flask_jwt_extended import jwt_required

usuario_blueprint = Blueprint('usuarios', __name__)

@usuario_blueprint.route('/users', methods=['POST'])
def crear_usuario_ruta():
    data = request.get_json()
    return crear_usuario(data)

@usuario_blueprint.route('/users_base', methods=['POST'])
def crear_usuario_base_ruta():
    data = request.get_json()
    return crear_usuario_base(data)

@usuario_blueprint.route('/login', methods=['POST'])
def login_ruta():
    data = request.get_json()
    return login_usuario(data)

@usuario_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def obtener_usuario_ruta():
    return obtener_usuario()

@usuario_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def eliminar_usuario_ruta(user_id):
    return eliminar_usuario(user_id)

@usuario_blueprint.route('/users/<int:user_id>/premium', methods=['POST'])
@jwt_required()
def actualizar_rol_premium_ruta(user_id):
    data = request.get_json()
    activar = data.get('activar')
    return actualizar_rol_premium(user_id, activar)

@usuario_blueprint.route('/users/<int:user_id>/edit', methods=['PUT']) 
@jwt_required() 
def actualizar_usuario_ruta(user_id): 
    return actualizar_usuario(user_id)

@usuario_blueprint.route('/users/<int:user_id>/addReminder', methods=['PATCH']) 
@jwt_required()
def add_reminder_ruta(user_id): 
    return add_reminder(user_id)

@usuario_blueprint.route('/users/<int:user_id>/reminders', methods=['GET']) 
@jwt_required() 
def obtener_recordatorios_ruta(user_id): 
    return obtener_recordatorios(user_id)