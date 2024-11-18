from flask import jsonify, request
from src.models.favorite import Favorite, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import MongoClient
import os
from bson.objectid import ObjectId

# Configuración para MongoDB
mongo_client = MongoClient(os.getenv('MONGODB_URI'))
mongo_db = mongo_client[os.getenv('MONGO_DB_NAME')]
place_collection = mongo_db['places']

@jwt_required()
def crear_favorito():
    data = request.get_json()
    idPlace = data.get('idPlace')
    user_id = get_jwt_identity()

    if isinstance(user_id, dict) and 'sub' in user_id:
        user_id = user_id['sub']

    if not idPlace:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    nuevo_favorito = Favorite(idUser=user_id, idPlace=idPlace)
    db.session.add(nuevo_favorito)
    db.session.commit()

    return jsonify({
        "mensaje": "Favorito creado exitosamente",
        "idFavorite": nuevo_favorito.idFavorite,
        "idPlace": idPlace,
        "idUser": nuevo_favorito.idUser
    }), 201

@jwt_required()
def obtener_favoritos():
    user_id = get_jwt_identity()

    if isinstance(user_id, dict) and 'sub' in user_id:
        user_id = user_id['sub']

    favoritos = Favorite.query.filter_by(idUser=user_id).all()
    print("Favoritos encontrados:", favoritos)
    
    places = []
    for favorito in favoritos:
        print("Consultando MongoDB para idPlace:", favorito.idPlace)
        try:
            place = place_collection.find_one({"_id": ObjectId(favorito.idPlace)})
            if place:
                # Convertir ObjectId a cadena
                place["_id"] = str(place["_id"])
                places.append({
                    "idFavorite": favorito.idFavorite,
                    "idPlace": favorito.idPlace,
                    "place": place,
                    "idUser": favorito.idUser
                })
            else:
                print("No se encontró el lugar en MongoDB para idPlace:", favorito.idPlace)
        except Exception as e:
            print(f"Error al consultar MongoDB: {e}")
    
    print("Lugares encontrados:", places)
    return jsonify(places), 200

@jwt_required()
def eliminar_favorito(idFavorite):
    user_id = get_jwt_identity()

    if isinstance(user_id, dict) and 'sub' in user_id:
        user_id = user_id['sub']

    favorito = Favorite.query.filter_by(idFavorite=idFavorite, idUser=user_id).first()
    
    if not favorito:
        return jsonify({"mensaje": "Favorito no encontrado"}), 404

    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"mensaje": "Favorito eliminado exitosamente"}), 200
