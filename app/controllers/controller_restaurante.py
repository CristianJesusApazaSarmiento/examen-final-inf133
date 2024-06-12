from flask import Blueprint, jsonify, request
from app.utils.decorators import jwt_required, roles_required
from app.models.model_restaurante import Restaurante
from app.views.view_restaurante import render_restaurante_detail, render_restaurante_list

restaurante_bp = Blueprint("restaurante", __name__)

@restaurante_bp.route("/restaurantes", methods=["GET"])
@jwt_required
@roles_required(roles=["Admin", "Customer"])
def get_restaurantes():
    restaurantes = Restaurante.get_all()
    return jsonify(render_restaurante_list(restaurantes))

@restaurante_bp.route("/restaurantes/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["Admin", "Customer"])
def get_restaurante(id):
    restaurante = Restaurante.get_by_id(id)
    if restaurante:
        return jsonify(render_restaurante_detail(restaurante))
    return jsonify({"error": " no encontrada"}), 404

@restaurante_bp.route("/restaurantes", methods=["POST"])
@jwt_required
@roles_required(roles=["Admin"])
def create_restaurante():
    data = request.json
    name = data.get("name")
    address = data.get("address")
    city = data.get("city")
    phone = data.get("phone")
    description = data.get("description")
    rating = data.get("rating")
    
    if not name or not address or not city or not phone or not description or rating is None:
        return jsonify({"error": "Faltan datos requeridos"}), 400
    
    restaurante = Restaurante(name=name, address=address, city=city, phone=phone, description=description, rating=rating)
    restaurante.save()
    
    return jsonify(render_restaurante_detail(restaurante)), 201

@restaurante_bp.route("/restaurantes/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["Admin"])
def update_restaurante(id):
    restaurante = Restaurante.get_by_id(id)
    
    if not restaurante:
        return jsonify({"error": "Restaurante no encontrada"}), 404
    
    data = request.json
    name = data.get("name")
    address = data.get("address")
    city = data.get("city")
    phone = data.get("phone")
    description = data.get("description")
    rating = data.get("rating")
    
    restaurante.update(name=name, address=address, city=city, phone=phone, description=description, rating=rating)
    
    return jsonify(render_restaurante_detail(restaurante))
    
@restaurante_bp.route("/restaurantes/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_restaurante(id):
    restaurante = Restaurante.get_by_id(id)
    
    if not restaurante:
        return jsonify({"error": "Restaurante no encontrada"}), 404
    
    restaurante.delete()
    return "", 204