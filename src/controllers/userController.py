from flask import jsonify, request
from src.models.user import User, db
from src.models.userRol import Role
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token
from datetime import datetime, timedelta, timezone
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def crear_usuario(data):
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    # Busca el rol "usuarios"
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
    
    # Verifica el estado de la membresia premium antes de iniciar sesion
    user.verificar_premium()
    
    expires = timedelta(hours=4)
    access_token = create_access_token(
        identity=str(user.id),  # Aquí el sub debe ser un string
        additional_claims={"id_Rol": user.id_Rol, "nombre": user.nombre},
        expires_delta=expires
        )    
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

@jwt_required()
def actualizar_usuario(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    
    if nombre:
        user.nombre = nombre
    if email:
        user.email = email
    if password:
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    db.session.commit()
    
    return jsonify({"mensaje": "Usuario actualizado",
                    "id": user.id, 
                    "nombre": user.nombre, 
                    "email": user.email}), 200

@jwt_required()
def add_reminder(user_id):
    data = request.get_json()
    eventReminder = data.get('eventReminder')
    ContentReminder = data.get('ContentReminder')
    nameReminder = data.get('nameReminder')

    if not eventReminder or not ContentReminder or not nameReminder:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    # Asegúrate de que las listas están inicializadas
    if user.eventReminder is None:
        user.eventReminder = []
    if user.ContentReminder is None:
        user.ContentReminder = []
    if user.nameReminder is None:
        user.nameReminder = []

    print(f"Usuario encontrado: {user.email}")

    user.eventReminder.append(eventReminder)
    user.ContentReminder.append(ContentReminder)
    user.nameReminder.append(nameReminder)
    db.session.commit()

    return jsonify({"mensaje": "Recordatorio añadido exitosamente"}), 200

@jwt_required()
def obtener_recordatorios(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    # Crear una lista de recordatorios combinando los tres atributos
    recordatorios = [
        {
            "eventReminder": user.eventReminder[i],
            "contentReminder": user.ContentReminder[i],
            "nameReminder": user.nameReminder[i]
        }
        for i in range(len(user.eventReminder))
    ]

    return jsonify({"recordatorios": recordatorios}), 200


def verificar_token():
    try:
        data = request.get_json()
        token = data.get('token', None)

        if not token:
            return jsonify({"valid": False, "message": "No hay token"}), 401

        # Decodificar el token sin verificar su firma para obtener la información de expiración
        decoded_token = decode_token(token, allow_expired=True)
        exp = decoded_token.get("exp", None)

        if not exp:
            return jsonify({"valid": False, "message": "Token sin información de expiración"}), 401

        # Verificar si el token ha expirado
        if datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
            return jsonify({"valid": False, "message": "Token ha expirado"}), 401

        return jsonify({"valid": True, "message": "Token válido"}), 200
    except Exception as e:
        return jsonify({"valid": False, "message": f"Error al verificar token: {e}"}), 401

