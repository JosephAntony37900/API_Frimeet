from flask import jsonify
from src.models.user import User, db
from src.models.userRol import Role
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

def crear_rol(data):
    nombre = data.get('nombre')
    
    if not nombre:
        return jsonify({ "mensaje": "El nombre no puede esta vacio"}), 400
    nuevo_rol = Role(nombre=nombre)
    db.session.add(nuevo_rol)
    db.session.commit()
    return jsonify({
        "mensaje": "Rol de usuario creado correctamente",
        "nombre": nuevo_rol.nombre
    }), 201
    
@jwt_required()
def obtener_roles():
    roles= Role.query.all()
    if not roles:
        return jsonify({"mensaje": "Roles no encontrado"}), 404
    roles_list = [{"id": rol.id, "nombre": rol.nombre} for rol in roles]
    
    return jsonify(roles_list), 200
    
@jwt_required()
def eliminar_rol(idRol):
    rol = Role.query.get(idRol)
    if not rol:
        return jsonify({"mensaje": "Rol no encontrado"}), 404
    db.session.delete(rol)
    db.session.commit()
    return jsonify({"mensaje": "Rol eliminado :p"}), 200