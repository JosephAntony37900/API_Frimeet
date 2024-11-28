from flask import jsonify, request
from src.models.tag import Tag, db
from flask_jwt_extended import jwt_required
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

# Configuración para MongoDB
mongo_client = MongoClient(os.getenv('MONGODB_URI'))
mongo_db = mongo_client[os.getenv('MONGO_DB_NAME')]
event_collection = mongo_db['events']
place_collection = mongo_db['places']

def crear_etiquetas(data):
    if not isinstance(data, list):
        return jsonify({"mensaje": "Se espera una lista de etiquetas"}), 400

    etiquetas_creadas = []
    for item in data:
        tagsEvent = item.get('tagsEvent')
        tagsPlace = item.get('tagsPlace')

        if not tagsEvent and not tagsPlace:
            return jsonify({"mensaje": "Al menos una de tagsEvent o tagsPlace es requerida"}), 400

        nueva_etiqueta = Tag(tagsEvent=tagsEvent, tagsPlace=tagsPlace)
        db.session.add(nueva_etiqueta)
        db.session.commit()
        etiquetas_creadas.append({"mensaje": "Etiqueta creada", "idTag": nueva_etiqueta.id})

    return jsonify(etiquetas_creadas), 201

# Obtener eventos por etiqueta consultando en MongoDB
@jwt_required()
def obtener_eventos_por_etiqueta(tag_id):
    etiqueta = Tag.query.get(tag_id)
    
    if not etiqueta:
        return jsonify({"mensaje": "Etiqueta no encontrada"}), 404

    # Obtener eventos desde MongoDB con la etiqueta
    try:
        eventos = event_collection.find({"tag": etiqueta.tagsEvent})
        eventos_list = []
        for evento in eventos:
            evento["_id"] = str(evento["_id"])
            eventos_list.append(evento)
        return jsonify({"etiqueta": etiqueta.tagsEvent, "eventos": eventos_list}), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error al consultar eventos: {e}"}), 500

# Obtener lugares por etiqueta consultando en MongoDB
@jwt_required()
def obtener_lugares_por_etiqueta(tag_id):
    etiqueta = Tag.query.get(tag_id)
    
    if not etiqueta:
        return jsonify({"mensaje": "Etiqueta no encontrada"}), 404

    # Obtener lugares desde MongoDB con la etiqueta
    try:
        lugares = place_collection.find({"tag": etiqueta.tagsPlace})
        lugares_list = []
        for lugar in lugares:
            lugar["_id"] = str(lugar["_id"])
            lugares_list.append(lugar)
        return jsonify({"etiqueta": etiqueta.tagsPlace, "lugares": lugares_list}), 200
    except Exception as e:
        return jsonify({"mensaje": f"Error al consultar lugares: {e}"}), 500


@jwt_required()
def eliminar_tags(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({"mensaje": "Tag no encontrado"}), 404
    db.session.delete(tag)
    db.session.commit()
    return jsonify({"mensaje": "Tag eliminado"}), 200

@jwt_required()
def obtener_todas_las_etiquetas():
    etiquetas = Tag.query.all()
    etiquetas_list = [{"idTag": etiqueta.id, "nombre": etiqueta.nombre} for etiqueta in etiquetas]
    return jsonify({"etiquetas": etiquetas_list}), 200