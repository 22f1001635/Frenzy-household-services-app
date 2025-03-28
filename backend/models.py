from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """Base user model that other user types inherit from"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    image_file = db.Column(db.String(255), nullable=False, default='profile.png')
    role = db.Column(db.String(20), nullable=False, default='user') # admin, professional, user
    is_blocked = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def validate_password(self,password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        return True, ""


class Professional(User):
    """Service Professional model inheriting from User"""
    __tablename__ = 'professionals'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    experience = db.Column(db.Integer)
    service_type = db.Column(db.Integer, db.ForeignKey('services.id'))
    is_verified = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Float, default=3)
    contact_number = db.Column(db.String(13))
    verification_status = db.Column(db.String(20), default='pending')  # pending, verified, rejected
    verification_date = db.Column(db.DateTime)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='professional', lazy=True)
    service = db.relationship('Service', backref='professionals', lazy=True)
    reviews = db.relationship('Review', backref='professional', lazy=True)
    documents = db.relationship('ProfessionalDocument', backref='professional', lazy=True)

    __mapper_args__ = {
        'inherit_condition': (id == User.id),
        'polymorphic_identity': 'professional'
    }

class ProfessionalDocument(db.Model):
    """For storing professional verification documents"""
    __tablename__ = 'professional_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'))
    document_type = db.Column(db.String(10),default='.pdf')
    document_url = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean, default=False)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    verified_at = db.Column(db.DateTime)

class Address(db.Model):
    """Address model for storing user addresses"""
    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Updated: customer_id → user_id
    address_line1 = db.Column(db.String(255), nullable=False)
    address_line2 = db.Column(db.String(255))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    phone_number = db.Column(db.String(15))  # Added field
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ServiceCategory(db.Model):
    """Model for service categories"""
    __tablename__ = 'service_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with services
    services = db.relationship('Service', backref='category_info', lazy=True)

class Service(db.Model):
    """Service model for different types of services offered"""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    base_price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer)  # Time in minutes
    is_active = db.Column(db.Boolean, default=True)
    service_area = db.Column(db.String(100))   # location pincodes seperated by comma
    image_file = db.Column(db.String(255), default='service-default.png')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key relationship with category
    category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=True)
    
    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='service', lazy=True)
    locations = db.relationship('ServiceLocation', backref='service', lazy=True, cascade='all, delete-orphan')

class ServiceLocation(db.Model):
    """Model for storing service area pin codes"""
    __tablename__ = 'service_locations'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Add unique constraint to prevent duplicate pin codes for same service
    __table_args__ = (
        db.UniqueConstraint('service_id', 'pin_code', name='unique_service_location'),
    )

class ServiceRequest(db.Model):
    """Service Request model for tracking service bookings"""
    __tablename__ = 'service_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'),nullable=True)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    quantity = db.Column(db.Integer, default=1)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    completion_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='requested')
    remarks = db.Column(db.Text)
    location_pin = db.Column(db.String(10))
    total_amount = db.Column(db.Float)
    
    # Relationships
    reviews = db.relationship('Review', backref='service_request', lazy=True)
    notifications = db.relationship('Notification', backref='service_request', lazy=True)

    __table_args__ = (
        db.UniqueConstraint(
            'professional_id', 
            'scheduled_date',
            name='unique_professional_scheduling'
        ),
    )

class Review(db.Model):
    """Review model for storing user reviews and ratings"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    """Notification model for reminders and alerts"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String(50))  # reminder, alert, etc.
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

class UserServiceAction(db.Model):
    """Model to track user actions: cart, wishlist, or immediate purchases."""
    __tablename__ = 'user_service_actions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id', ondelete='CASCADE'), nullable=False)
    action_type = db.Column(db.String(20), nullable=False)  # Values: 'cart', 'wishlist', 'buy_now'
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='service_actions')
    service = db.relationship('Service', backref='user_actions')

    # Ensure unique entries per user-service-action type (e.g., avoid duplicate cart items)
    __table_args__ = (
        db.UniqueConstraint('user_id', 'service_id', 'action_type', name='unique_user_service_action'),
    )