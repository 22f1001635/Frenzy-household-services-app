from models import *
from flask import Flask,jsonify,request,session,send_from_directory
from functools import wraps
from werkzeug.utils import secure_filename
import os,secrets

@app.before_request
def make_session_temporary():
    if current_user.is_authenticated:
        session.permanent = False

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            return jsonify({"error": "Access denied"}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/signin', methods=['POST'])
def signin():
    # Get credentials from request
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Validate input presence
    if not email or not password:
        return jsonify({
            'message': 'Email and password are required'
        }), 400
        
    else:
        # Query user from database
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(password):
            login_user(user)
            session.permanent = False
            print(current_user)
            return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'role': user.role  
            }}), 200
        
        # Invalid credentials
        return jsonify({
            'message': 'Invalid email or password'
        }), 401
    
@app.route('/api/signup', methods=['POST'])
def register():
    # get credentials 
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    # Check if all required fields are provided
    if not email or not password or not username or not confirm_password:
        return jsonify({
            'message': 'Provide Complete Credentials'
        }), 400
    
    else:
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered! Please try a different email or login to your existing account'}), 400
    
        elif(password==confirm_password):
            user = User(
                email=email,
                username=username,
            )
            is_valid, error_msg = user.validate_password(password)
            if not is_valid:
                return jsonify({'message': error_msg}), 401
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'Registration successful'}), 201


@app.route('/api/change-password', methods=['POST'])
@login_required
def change_password():
    data = request.json
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    
    # Validate input presence
    if not all([current_password, new_password, confirm_password]):
        return jsonify({
            'message': 'All password fields are required'
        }), 400
    
    # Verify current password
    if not current_user.check_password(current_password):
        return jsonify({
            'message': 'Current password is incorrect'
        }), 401
    
    # Check if new passwords match
    if new_password != confirm_password:
        return jsonify({
            'message': 'New passwords do not match'
        }), 400
        
    if current_user.check_password(new_password):
        return jsonify({'message': 'New password cannot be the same as the current password'}), 400
    
    # Validate new password requirements
    is_valid, error_message = current_user.validate_password(new_password)
    if not is_valid:
        return jsonify({
            'message': error_message
        }), 400
    
    # Update password
    try:
        current_user.set_password(new_password)
        db.session.commit()
        return jsonify({
            'message': 'Password updated successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        print("Error updating password:", str(e))  # Log the actual error
        return jsonify({
            'message': 'Error updating password',
            'error': str(e)  # Ensure the error is included in the response
        }), 500

@app.route('/api/upload-profile-picture', methods=['POST'])
@login_required
def upload_profile_picture():
    if 'profile_picture' not in request.files:
        return jsonify({'message': 'No file uploaded'}), 400

    file = request.files['profile_picture']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'message': 'Invalid file type'}), 400

    # Ensure profile pictures folder exists
    if not os.path.exists(app.config['PROFILE_PIC_FOLDER']):
        os.makedirs(app.config['PROFILE_PIC_FOLDER'])

    # Delete old profile picture if not default
    if current_user.image_file != 'profile.png':
        old_path = os.path.join(app.config['PROFILE_PIC_FOLDER'], current_user.image_file)
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except:
                pass

    # Generate unique filename using user ID and random hex string
    random_hex = secrets.token_hex(8)
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"user_{current_user.id}_{random_hex}.{ext}"
    filepath = os.path.join(app.config['PROFILE_PIC_FOLDER'], filename)

    try:
        file.save(filepath)
        current_user.image_file = filename  # Store only filename in DB
        db.session.commit()
        return jsonify({'message': 'Profile picture updated', 'filename': filename}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error saving profile picture', 'error': str(e)}), 500

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/profile_pictures/<filename>')
def serve_profile_picture(filename):
    return send_from_directory(app.config['PROFILE_PIC_FOLDER'], filename)

@app.route('/api/current_user', methods=['GET'])
@login_required
def current_user_info():
    user_data = {
            'id': current_user.id,
            'email': current_user.email,
            'username': current_user.username,
            'role': current_user.role,    
            'image_file': current_user.image_file
    }
    # Add customer-specific fields
    if current_user.role == 'customer':
        customer = Customer.query.get(current_user.id)
        if customer:
            user_data.update({
                'address': customer.address,
                'pin_code': customer.pin_code,
                'phone_number': customer.phone_number
            })
    
    return jsonify({'user': user_data}), 200

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    session.clear() #clear all session data
    return jsonify({
        'message': 'Sign Out! Successful'
    }),200
    
@app.route('/api/data')
def get_data():
    return jsonify({
        'message': 'Successfully connected to Flask backend!'
    })


@app.route('/api/services', methods=['GET', 'POST'])
@admin_required
@login_required
def handle_services():
    if request.method == 'GET':
        # List all services
        services = Service.query.all()
        return jsonify([{
            'id': s.id,
            'name': s.name,
            'is_active': s.is_active
        } for s in services])
    
    elif request.method == 'POST':
        data = request.json
        name = data.get('name')
        description = data.get('description')
        time_required = data.get('time_required')
        service_pincodes = data.get('service_pincodes')
        base_price = data.get('base_price')

        # Validate input presence
        if name is None or description is None or time_required is None or service_pincodes is None or base_price is None:
            print(name, base_price, description, time_required, service_pincodes)
            return jsonify({'message': 'All fields are required'}), 400

        try:
            service = Service(
                name=name,
                description=description,
                time_required=time_required,
                base_price=base_price,  
                service_area=service_pincodes 
            )
            print(name, base_price, description, time_required, service_pincodes)
            db.session.add(service)
            db.session.commit()
            
            return jsonify({
                'message': 'Service added successfully',
                'service_id': service.id
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'message': 'Error adding service',
                'error': str(e)
            }), 500

@app.route('/api/services/<int:service_id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
@admin_required
@login_required
def handle_single_service(service_id):
    service = Service.query.get_or_404(service_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': service.id,
            'name': service.name,
            'time_required': service.time_required,
            'base_price': service.base_price,
            'service_pincodes': service.service_area
        })
    
    elif request.method == 'PUT':
        data = request.json
        
        service.name = data.get('name', service.name)
        service.description = data.get('description', service.description)
        service.time_required = data.get('time_required', service.time_required)
        service.base_price = data.get('base_price', service.base_price)
        service.service_pincodes = data.get('service_pincodes', service.service_area)
        
        
        db.session.commit()
        return jsonify({'message': 'Service updated successfully'})
    
    elif request.method == 'DELETE':
        db.session.delete(service)
        db.session.commit()
        return jsonify({'message': 'Service deleted successfully'})
    
    elif request.method == 'PATCH':
        service.is_active = not service.is_active
        db.session.commit()
        return jsonify({'message': 'Service status updated', 'is_active': service.is_active}),200

@app.route('/api/services/active', methods=['GET'])
def get_active_services():
    try:
        services = Service.query.filter_by(is_active=True).all()
        return jsonify([{
            'id': service.id,
            'name': service.name
        } for service in services])
    except Exception as e:
        return jsonify({'message': 'Error fetching services', 'error': str(e)}), 500
    
@app.route('/api/register-professional', methods=['POST'])
@login_required
def register_professional():
    try:
        # Get the current user from the database
        user = User.query.get(current_user.id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Check if user already has a professional record
        existing_professional = (
                db.session.query(Professional.verification_status)
                .filter(Professional.id == current_user.id)  # Ensure correct field reference
                .scalar()  # Fetch a single value instead of an object
            )
        if existing_professional == 'pending':
                return jsonify({'message': 'Application already pending. Please wait for review.'}), 400
        elif existing_professional == 'verified':
                return jsonify({'message': 'You are already a verified professional.'}), 400
        elif existing_professional == 'rejected':
                pass  # Allow reapplication

        # Check if the request has the file part
        has_file = 'document' in request.files and request.files['document'].filename != ''

        # Get JSON data from form data instead of request.json
        data = request.form.to_dict()
        
        required_fields = ['service_id', 'experience', 'contact_number', 'pin_code']

        # Validate input for required fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        if current_user.role != 'user':
            return jsonify({'message': 'Already a professional/admin'}), 400
        if len(data.get('contact_number', '')) > 13:
            return jsonify({'message': 'Contact number too long'}), 400

        # File validation if file is uploaded
        if has_file:
            document_file = request.files['document']
            
            # Validate file type (PDF only)
            if not document_file.filename.lower().endswith('.pdf'):
                return jsonify({'message': 'Only PDF files are allowed'}), 400
            
            # Check file size (20MB limit)
            MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB in bytes
            document_file.seek(0, os.SEEK_END)
            file_size = document_file.tell()
            document_file.seek(0)  # Reset file pointer to beginning
            
            if file_size > MAX_FILE_SIZE:
                return jsonify({'message': 'File size exceeds 20MB limit'}), 400

        # Address handling
        address_value = data.get('address')
        if not address_value or not isinstance(address_value, str):
            address_value = "Address not provided"

        # Handle Customer data - Check if exists with a direct query to avoid ORM issues
        customer_exists = db.session.query(db.exists().where(Customer.id == user.id)).scalar()

        if not customer_exists:
            # Insert into customers table
            stmt = db.insert(Customer.__table__).values(
                id=user.id,
                address=address_value,
                phone_number=data.get('contact_number', ''),
                pin_code=data.get('pin_code', '')
            )
            db.session.execute(stmt)
        else:
            # Get the existing customer to update (Minimal Fix Applied Here)
            customer = db.session.query(Customer).filter_by(id=user.id).first()
            if customer:
                customer.address = address_value
                customer.phone_number = data.get('contact_number', '')
                customer.pin_code = data.get('pin_code', '')

        # Handle Professional data
        service_id = int(data.get('service_id')) if str(data.get('service_id', '')).isdigit() else None
        experience_value = int(data.get('experience')) if str(data.get('experience', '')).isdigit() else 0

        # Check if professional exists with a direct query
        professional_exists = db.session.query(db.exists().where(Professional.id == user.id)).scalar()

        if not professional_exists:
            # Insert directly into professionals table
            stmt = db.insert(Professional.__table__).values(
                id=user.id,
                experience=experience_value,
                service_type=service_id,
                contact_number=data.get('contact_number', ''),
                verification_status='pending'
            )
            db.session.execute(stmt)
        else:
            # Get the existing professional to update
            professional = Professional.query.get(user.id)
            if professional:
                professional.experience = experience_value
                professional.service_type = service_id
                professional.contact_number = data.get('contact_number', '')
                professional.verification_status = 'pending'

        # Handle file upload if a file was provided
        if has_file:
            document_file = request.files['document']
            
            # Generate a secure filename
            import uuid
            secure_filename = f"{uuid.uuid4()}_{document_file.filename}"
            
            # Save file to upload folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename)
            document_file.save(file_path)
            
            # Check if document already exists for this professional
            existing_document = ProfessionalDocument.query.filter_by(professional_id=user.id).first()
            
            if existing_document:
                # Remove old file from filesystem if it exists
                if existing_document.document_url:
                    try:
                        old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], existing_document.document_url)
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)
                    except Exception as e:
                        print(f"Error removing old document: {str(e)}")
                
                # Update existing document record
                existing_document.document_type = '.pdf'
                existing_document.document_url = secure_filename
                existing_document.is_verified = False
                existing_document.verified_at = None
                existing_document.verified_by = None
            else:
                # Create new document record
                new_document = ProfessionalDocument(
                    professional_id=user.id,
                    document_type='.pdf',
                    document_url=secure_filename,
                    is_verified=False
                )
                db.session.add(new_document)

        db.session.commit()

        return jsonify({'message': 'Registration submitted for verification'}), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error in registration: {str(e)}")  # Add detailed logging
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500
