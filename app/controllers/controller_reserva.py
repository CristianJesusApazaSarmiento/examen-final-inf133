from flask import Blueprint, jsonify, request
from app.utils.decorators import jwt_required, roles_required
from app.models.model_reservas import Reserva
from app.views.view_reserva import render_reserva_detail, render_reserva_list
from app.models.model_user import User
from app.models.model_restaurante import Restaurante

reserva_bp = Blueprint("reserva", __name__)

@reserva_bp.route("/reservas", methods=["GET"])
@jwt_required
@roles_required(roles=["Admin", "Customer"])
def get_restaurantes():
    reservas = Reserva.get_all()
    return jsonify(render_reserva_list(reservas))

@reserva_bp.route("/reservas/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["Admin", "Customer"])
def get_restaurante(id):
    reserva = Reserva.get_by_id(id)
    if reserva:
        return jsonify(render_reserva_detail(reserva))
    return jsonify({"error": "Reserva no encontrada"}), 404

@reserva_bp.route("/reservas", methods=["POST"])
@jwt_required
@roles_required(roles=["Admin", "Customer"])
def create_restaurante():
    data = request.json
    user_id = User.id
    restaurant_id = Restaurante.id
    reservation_date = data.get("reservation_date")
    num_guests = data.get("num_guests")
    special_requests = data.get("special_requests")
    status = data.get("status")
    
    if user_id is None or restaurant_id is None or not reservation_date or not num_guests or not special_requests or not status:
        return jsonify({"error": "Faltan datos requeridos"}), 400
    
    reserva = Reserva(user_id=user_id, restaurant_id=restaurant_id, reservation_date=reservation_date, num_guests=num_guests, special_requests=special_requests, status=status)
    reserva.save()
    
    return jsonify(render_reserva_detail(reserva)), 201

@reserva_bp.route("/reservas/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["Admin", "Customer"])
def update_restaurante(id):
    reserva = Reserva.get_by_id(id)
    
    if not reserva:
        return jsonify({"error": "Reserva no encontrada"}), 404
    
    data = request.json
    reservation_date = data.get("reservation_date")
    num_guests = data.get("num_guests")
    special_requests = data.get("special_requests")
    status = data.get("status")
    
    reserva.update(reservation_date=reservation_date, num_guests=num_guests, special_requests=special_requests, status=status)
    
    return jsonify(render_reserva_detail(reserva))
    
@reserva_bp.route("/reservas/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["Admin", "Customer"])
def delete_restaurante(id):
    reserva = Reserva.get_by_id(id)
    
    if not reserva:
        return jsonify({"error": "Reserva no encontrada"}), 404
    
    reserva.delete()
    return "", 204


