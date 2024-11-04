from flask import jsonify
from src.models.tag import Tag, db
from flask_jwt_extended import jwt_required
import os

# Configurar la conexión a MongoDB
# from pymongo import MongoClient
# mongo_client = MongoClient(os.getenv('MONGO_URI'))
# mongo_db = mongo_client[os.getenv('MONGO_DB_NAME')]
# place_collection = mongo_db['places']

# Crear una nueva etiqueta
def crear_etiqueta(data):
    nombre = data.get('nombre')
    if not nombre:
        return jsonify({"mensaje": "Nombre de etiqueta es requerido"}), 400

    if Tag.query.filter_by(nombre=nombre).first():
        return jsonify({"mensaje": "La etiqueta ya existe"}), 400

    nueva_etiqueta = Tag(nombre=nombre)
    db.session.add(nueva_etiqueta)
    db.session.commit()
    
    return jsonify({"mensaje": "Etiqueta creada", "idTag": nueva_etiqueta.id}), 201

# Asignar un lugar a una etiqueta (se agrega el ID del lugar de MongoDB)
@jwt_required()
def asignar_etiqueta_a_lugar(tag_id, place_id):
    etiqueta = Tag.query.get(tag_id)
    
    if not etiqueta:
        return jsonify({"mensaje": "Etiqueta no encontrada"}), 404
    
    # Comentado por ahora
    # if place_id in etiqueta.place_ids:
    #    return jsonify({"mensaje": "El lugar ya tiene esta etiqueta"}), 400

    # etiqueta.place_ids.append(place_id)
    db.session.commit()
    
    return jsonify({"mensaje": "Etiqueta asignada al lugar"}), 200

# Obtener lugares por etiqueta consultando en MongoDB
@jwt_required()
def obtener_lugares_por_etiqueta(tag_id):
    etiqueta = Tag.query.get(tag_id)
    
    if not etiqueta:
        return jsonify({"mensaje": "Etiqueta no encontrada"}), 404
    
    # Comentado por ahora
    # Obtener los lugares de MongoDB usando los ids guardados en `place_ids`
    # lugares = list(place_collection.find({"_id": {"$in": etiqueta.place_ids}}))

    # Formatear la respuesta
    # lugares_formateados = [{"idPlace": lugar["_id"], "nombre": lugar["nombre"]} for lugar in lugares]
    
    return jsonify({"etiqueta": etiqueta.nombre, "lugares": []}), 200

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