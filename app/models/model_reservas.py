from app.database import db
from datetime import datetime

class Reserva(db.Model):
    __tablename__ = "reservas"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, nullable=False)
    reservation_date = db.Column(db.Date, nullable=False)
    num_guests = db.Column(db.Integer, nullable=False)
    special_requests = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    
    def __init__(self, user_id, restaurant_id, reservation_date, num_guests, special_requests, status):
        self.user_id = user_id
        self.restaurant_id = restaurant_id
        self.reservation_date = reservation_date
        self.num_guests = num_guests
        self.special_requests = special_requests
        self.status = status
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self, reservation_date=None, num_guests=None, special_requests=None, status=None):
        if reservation_date is not None:
            self.reservation_date = reservation_date
        if num_guests is not None:
            self.num_guests = num_guests
        if special_requests is not None:
            self.special_requests = special_requests
        if status is not None:
            self.status = status
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @staticmethod
    def get_all():
        return Reserva.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Reserva.query.get(id)