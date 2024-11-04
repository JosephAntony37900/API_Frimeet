from flask import jsonify
from src.models.user import User, db
from src.models.userRol import Role
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta

def crear_usuario(data):
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    
    # Busca el rol "Usuarios"
    rol_nombre = "Usuarios"
    rol = Role.query.filter_by(nombre=rol_nombre).first()
    
    if not rol:
        return jsonify({"mensaje": "Rol 'Usuarios' no encontrado"}), 400
    
    if not nombre or not email or not password:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"mensaje": "El email ya está registrado"}), 400

    nuevo_usuario = User(nombre=nombre, email=email, password=password, id_Rol=rol.id)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({
        "mensaje": "Usuario creado con bcrypt",
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre,
        "email": nuevo_usuario.email,
        "rol": rol.nombre
    }), 201

def crear_usuario_base(data):
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    
    # Busca el rol "Usuarios"
    rol_nombre = "Usuarios"
    rol = Role.query.filter_by(nombre=rol_nombre).first()

    if not rol:
        return jsonify({"mensaje": "Rol 'Usuarios' no encontrado"}), 400
    
    if not nombre or not email or not password:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"mensaje": "El email ya está registrado"}), 400

    nuevo_usuario = User(nombre=nombre, email=email, password=password, id_Rol=rol.id)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({
        "mensaje": "Usuario creado sin bcrypt",
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre,
        "email": nuevo_usuario.email,
        "rol": rol.nombre
    }), 201

def login_usuario(data):
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401
    if not user.check_password(password):
        return jsonify({"mensaje": "Credenciales inválidas"}), 401
    
    # Verifica el estado de la membresía premium antes de iniciar sesión
    user.verificar_premium()
    
    access_token = create_access_token(identity=user.id)
    return jsonify({"mensaje": "Inicio de sesión exitoso", "token": access_token}), 200

@jwt_required()
def obtener_usuario():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    rol= Role.query.get(user.id_Rol)
    return jsonify({
        "id": user.id,
        "nombre": user.nombre,
        "email": user.email,
        "rol": rol.nombre
    }), 200

@jwt_required()
def eliminar_usuario(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"mensaje": "Usuario eliminado"}), 200

@jwt_required()
def actualizar_rol_premium(user_id, activar):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    
    if activar:
        rol_nombre = "Premium"
        rol = Role.query.filter_by(nombre=rol_nombre).first()
        if not rol:
            return jsonify({"mensaje": "Rol 'Premium' no encontrado"}), 400
        user.id_Rol = rol.id
        user.premium_expiration = datetime.utcnow() + timedelta(days=30)
    else:
        rol_nombre = "Usuarios"
        rol = Role.query.filter_by(nombre=rol_nombre).first()
        if not rol:
            return jsonify({"mensaje": "Rol 'Usuarios' no encontrado"}), 400
        user.id_Rol = rol.id
        user.premium_expiration = None

    db.session.commit()
    return jsonify({"mensaje": f"Rol de usuario actualizado a {rol.nombre}"}), 200
