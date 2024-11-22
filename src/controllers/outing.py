from flask import jsonify
from pymongo import MongoClient
from src.models.outing import Outing, db
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from bson.objectid import ObjectId


mongo_client = MongoClient(os.getenv('MONGODB_URI'))
mongo_db = mongo_client[os.getenv('MONGO_DB_NAME')]
place_collection = mongo_db['places']


@jwt_required()
def crear_salida(data):
   # idPlace = data.get('idPlace')
    description = data.get('description')
    user_id = get_jwt_identity()

   # if not idPlace:
    #    return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    nueva_salida = Outing(idUser=user_id, description=description)
    # Comentado por ahora
    # nueva_salida.idPlace = idPlace
    
    db.session.add(nueva_salida)
    db.session.commit()
    return jsonify({
        "mensaje": "Salida creada exitosamente",
        "idOuting": nueva_salida.idOuting,
        # "idPlace": idPlace,
        "idUser": nueva_salida.idUser,
        "description": nueva_salida.description
    }), 201

@jwt_required()
def obtener_salidas():
    user_id = get_jwt_identity()
    salidas = Outing.query.filter_by(idUser=user_id).all()
    return jsonify([{
        "idOuting": salida.idOuting,
        # "idPlace": salida.idPlace,
        "idUser": salida.idUser,
        "description": salida.description
    } for salida in salidas]), 200

@jwt_required()
def eliminar_salida(idOuting):
    user_id = get_jwt_identity()
    salida = Outing.query.filter_by(idOuting=idOuting, idUser=user_id).first()
    
    if not salida:
        return jsonify({"mensaje": "Salida no encontrada"}), 404

    db.session.delete(salida)
    db.session.commit()
    return jsonify({"mensaje": "Salida eliminada exitosamente"}), 200

@jwt_required()
def obtener_salida_por_id(idOuting):
    user_id = get_jwt_identity()
    salida = Outing.query.filter_by(idOuting=idOuting, idUser=user_id).first()

    if not salida:
        return jsonify({"mensaje": "Salida no encontrada o no autorizada"}), 404

    return jsonify({
        "idOuting": salida.idOuting,
        # "idPlace": salida.idPlace,
        "idUser": salida.idUser,
        "description": salida.description
    }), 200
