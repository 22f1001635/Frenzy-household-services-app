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
    image_file = db.Column(db.String(20), nullable=False, default='profile.png')
    role = db.Column(db.String(20), nullable=False, default='customer')
    is_blocked = db.Column(db.Boolean, default=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
        'polymorphic_on': role
    }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def validate_password(self,password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        return True, ""

class PaymentMethod(db.Model):
    """Payment Method model for storing customer payment information"""
    __tablename__ = 'payment_methods'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    method_type = db.Column(db.String(20), nullable=False)  # credit_card, upi, bank_account
    is_default = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime)
    
    # For Credit Cards (encrypted in production)
    card_last_four = db.Column(db.String(4))
    card_brand = db.Column(db.String(20))
    card_expiry = db.Column(db.String(7))
    
    # For UPI
    upi_id = db.Column(db.String(50))
    
    # For Bank Accounts
    bank_name = db.Column(db.String(100))
    account_last_four = db.Column(db.String(4))
    
    # Relationships
    payments = db.relationship('Payment', backref='payment_method', lazy=True)

class Professional(User):
    """Service Professional model inheriting from User"""
    __tablename__ = 'professionals'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    description = db.Column(db.Text)
    experience = db.Column(db.Integer)
    service_type = db.Column(db.Integer, db.ForeignKey('services.id'))
    is_verified = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Float, default=3)
    contact_number = db.Column(db.String(13))
    verification_status = db.Column(db.String(20))  # pending, verified, rejected
    verification_date = db.Column(db.DateTime)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='professional', lazy=True)
    service = db.relationship('Service', backref='professionals', lazy=True)
    reviews = db.relationship('Review', backref='professional', lazy=True)
    documents = db.relationship('ProfessionalDocument', backref='professional', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'professional',
        'inherit_condition': (id == User.id)  # Explicitly specify the inheritance condition
    }

class ProfessionalDocument(db.Model):
    """For storing professional verification documents"""
    __tablename__ = 'professional_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'))
    document_type = db.Column(db.String(50))
    document_url = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean, default=False)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    verified_at = db.Column(db.DateTime)

class Customer(User):
    """Customer model inheriting from User"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    address = db.Column(db.Text)
    pin_code = db.Column(db.String(10))
    phone_number = db.Column(db.String(15))
    
    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='customer', lazy=True)
    reviews = db.relationship('Review', backref='customer', lazy=True)
    payment_methods = db.relationship('PaymentMethod', backref='customer', lazy=True,
                                    cascade='all, delete-orphan')
    
    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }
    
    def get_default_payment_method(self):
        return PaymentMethod.query.filter_by(
            customer_id=self.id,
            is_default=True,
            is_active=True
        ).first()

class Service(db.Model):
    """Service model for different types of services offered"""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    base_price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer)  # Time in minutes
    is_active = db.Column(db.Boolean, default=True)
    category = db.Column(db.String(50))
    service_area = db.Column(db.String(100))   # General area description
    
    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='service', lazy=True)
    locations = db.relationship('ServiceLocation', backref='service', lazy=True,
                              cascade='all, delete-orphan')
    
    def add_location(self, pin_code):
        """Helper method to add a new service location"""
        location = ServiceLocation(service_id=self.id, pin_code=pin_code)
        db.session.add(location)
        return location
    
    def remove_location(self, pin_code):
        """Helper method to remove a service location"""
        location = ServiceLocation.query.filter_by(
            service_id=self.id, 
            pin_code=pin_code
        ).first()
        if location:
            db.session.delete(location)
    
    def get_active_locations(self):
        """Helper method to get all active service locations"""
        return [loc.pin_code for loc in self.locations if loc.is_active]

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
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'))
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    completion_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='requested')
    remarks = db.Column(db.Text)
    location_pin = db.Column(db.String(10))
    total_amount = db.Column(db.Float)
    
    # Relationships
    reviews = db.relationship('Review', backref='service_request', lazy=True)
    notifications = db.relationship('Notification', backref='service_request', lazy=True)
    payment = db.relationship('Payment', backref='service_request', uselist=False)

class Review(db.Model):
    """Review model for storing customer reviews and ratings"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    """Payment model for handling transactions"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'), nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default='pending')  # pending/success/failed
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

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