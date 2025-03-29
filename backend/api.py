from models import *
from flask import Flask,jsonify,request,session,send_from_directory
from functools import wraps
from werkzeug.utils import secure_filename
import os,secrets
import uuid

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/signin', methods=['POST'])
def signin():
    # Get credentials from request
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Validate input presence
    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    # Check if user is blocked
    if user and user.is_blocked:
        return jsonify({'message': 'Your account has been blocked. Please contact support.'}), 403

    # Check if user exists and password is correct
    if user and user.check_password(password):
        login_user(user)
        session.permanent = False
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'role': user.role,
                'is_blocked': user.is_blocked 
            }
        }), 200

    return jsonify({'message': 'Invalid email or password'}), 401
    
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

@app.route('/profile_pictures/<filename>')
def serve_profile_picture(filename):
    return send_from_directory(app.config['PROFILE_PIC_FOLDER'], filename)

@app.route('/api/current_user', methods=['GET'])
@login_required
def current_user_info():
    # Check if the user is blocked
    if current_user.is_blocked:
        logout_user()
        return jsonify({'message': 'Your account has been blocked. Please contact support.'}), 403

    user_data = {
        'id': current_user.id,
        'email': current_user.email,
        'username': current_user.username,
        'role': current_user.role,
        'image_file': current_user.image_file,
        'is_blocked': current_user.is_blocked 
    }

    if current_user.role in ['professional', 'user']:
        professional = Professional.query.get(current_user.id)
        if professional:
            user_data['verification_status'] = professional.verification_status

    # Fetch default address for phone number
    default_address = Address.query.filter_by(
        user_id=current_user.id,
        is_default=True
    ).first()

    if default_address:
        user_data['phone_number'] = default_address.phone_number
        user_data['address'] = {
            'id': default_address.id,
            'address_line1': default_address.address_line1,
            'address_line2': default_address.address_line2,
            'city': default_address.city,
            'state': default_address.state,
            'pincode': default_address.pincode,
            'is_default': default_address.is_default
        }

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

def save_service_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Create a unique filename using random hex
        unique_filename = f"{secrets.token_hex(8)}_{filename}"
        # Create service upload folder if it doesn't exist
        os.makedirs(app.config['SERVICE_UPLOAD_FOLDER'], exist_ok=True)
        # Save the file
        file_path = os.path.join(app.config['SERVICE_UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return unique_filename
    return None

def delete_service_image(filename):
    if filename and filename != 'service-default.png':
        try:
            file_path = os.path.join(app.config['SERVICE_UPLOAD_FOLDER'], filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            print(f"Error deleting file: {e}")
    return False

@app.route('/api/services', methods=['GET', 'POST'])
@admin_required
@login_required
def handle_services():
    if request.method == 'GET':
        # List all services with category info
        services = Service.query.all()
        return jsonify([{
            'id': s.id,
            'name': s.name,
            'is_active': s.is_active,
            'category': s.category_info.name if s.category_info else None,
            'category_id': s.category_id,
            'image_file': s.image_file
        } for s in services])
    
    elif request.method == 'POST':
        # Handle form data
        name = request.form.get('name')
        description = request.form.get('description')
        time_required = request.form.get('time_required')
        service_pincodes = request.form.get('service_pincodes')
        base_price = request.form.get('base_price')
        category_id = request.form.get('category_id')
        
        # Handle file upload
        image_file = 'service-default.png'  # Default image
        if 'service_image' in request.files:
            file = request.files['service_image']
            if file.filename:
                saved_filename = save_service_image(file)
                if saved_filename:
                    image_file = saved_filename

        # Validate input presence
        if name is None or description is None or time_required is None or base_price is None:
            return jsonify({'message': 'Required fields are missing'}), 400

        try:
            service = Service(
                name=name,
                description=description,
                time_required=int(time_required),
                base_price=float(base_price),
                service_area=service_pincodes if service_pincodes else "",
                category_id=int(category_id) if category_id else None,
                image_file=image_file
            )
            db.session.add(service)
            db.session.commit()
            
            # Create ServiceLocation entries for each pincode
            if service_pincodes:
                pincodes = [p.strip() for p in service_pincodes.split(',') if p.strip()]
                for pincode in pincodes:
                    loc = ServiceLocation(service_id=service.id, pin_code=pincode)
                    db.session.add(loc)
                db.session.commit()
            
            return jsonify({
                'message': 'Service added successfully',
                'service_id': service.id
            }), 201

        except Exception as e:
            db.session.rollback()
            # Clean up the uploaded file if there was an error
            if image_file != 'service-default.png':
                delete_service_image(image_file)
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
            'description': service.description,
            'time_required': service.time_required,
            'base_price': service.base_price,
            'service_pincodes': service.service_area,
            'category_id': service.category_id,
            'image_file': service.image_file
        })
    
    elif request.method == 'PUT':
        # Handle form data for update
        name = request.form.get('name')
        description = request.form.get('description')
        time_required = request.form.get('time_required')
        service_pincodes = request.form.get('service_pincodes', '')
        base_price = request.form.get('base_price')
        category_id = request.form.get('category_id')
        
        # Validate name field
        if name and name.strip() == '':
            return jsonify({'message': 'Service name cannot be empty'}), 400
        
        if name:
            service.name = name
        if description:
            service.description = description
        if time_required:
            service.time_required = int(time_required)
        if base_price:
            service.base_price = float(base_price)
        if category_id:
            service.category_id = int(category_id)
        
        # Handle file upload for update
        old_image = service.image_file
        if 'service_image' in request.files:
            file = request.files['service_image']
            if file.filename:
                saved_filename = save_service_image(file)
                if saved_filename:
                    service.image_file = saved_filename
                    # Delete old image after updating database entry
                    if old_image != 'service-default.png':
                        delete_service_image(old_image)
        
        # Update service locations if pincodes have changed
        if service_pincodes != service.service_area:
            service.service_area = service_pincodes
            
            # Delete existing locations
            ServiceLocation.query.filter_by(service_id=service.id).delete()
            
            # Create new locations
            if service_pincodes:
                pincodes = [p.strip() for p in service_pincodes.split(',') if p.strip()]
                for pincode in pincodes:
                    loc = ServiceLocation(service_id=service.id, pin_code=pincode)
                    db.session.add(loc)
        
        try:
            db.session.commit()
            return jsonify({'message': 'Service updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error updating service', 'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            # Delete the service image if it's not the default
            if service.image_file != 'service-default.png':
                delete_service_image(service.image_file)
            
            # Service locations will be deleted due to cascade
            db.session.delete(service)
            db.session.commit()
            return jsonify({'message': 'Service deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error deleting service', 'error': str(e)}), 500
    
    elif request.method == 'PATCH':
        service.is_active = not service.is_active
        db.session.commit()
        return jsonify({'message': 'Service status updated', 'is_active': service.is_active}), 200
    
    elif request.method == 'DELETE':
        try:
            # Delete the service image if it's not the default
            if service.image_file != 'service-default.png':
                delete_service_image(service.image_file)
            
            # Service locations will be deleted due to cascade
            db.session.delete(service)
            db.session.commit()
            return jsonify({'message': 'Service deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error deleting service', 'error': str(e)}), 500
    
    elif request.method == 'PATCH':
        service.is_active = not service.is_active
        db.session.commit()
        return jsonify({'message': 'Service status updated', 'is_active': service.is_active}), 200


@app.route('/api/categories', methods=['GET', 'POST'])
@admin_required
@login_required
def handle_categories():
    if request.method == 'GET':
        # List all categories
        categories = ServiceCategory.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'is_active': c.is_active
        } for c in categories])
    
    elif request.method == 'POST':
        data = request.json
        name = data.get('name')
        description = data.get('description')
        
        # Validate input
        if not name:
            return jsonify({'message': 'Category name is required'}), 400
        
        # Check if category with this name already exists
        existing_category = ServiceCategory.query.filter_by(name=name).first()
        if existing_category:
            return jsonify({'message': 'A category with this name already exists'}), 400
        
        try:
            category = ServiceCategory(
                name=name,
                description=description
            )
            db.session.add(category)
            db.session.commit()
            
            return jsonify({
                'message': 'Category added successfully',
                'category_id': category.id
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'message': 'Error adding category',
                'error': str(e)
            }), 500

@app.route('/api/categories/<int:category_id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
@admin_required
@login_required
def handle_single_category(category_id):
    category = ServiceCategory.query.get_or_404(category_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'is_active': category.is_active
        })
    
    elif request.method == 'PUT':
        data = request.json
        name = data.get('name')
        description = data.get('description')
        
        if name:
            # Check if another category already has this name
            existing = ServiceCategory.query.filter(
                ServiceCategory.name == name, 
                ServiceCategory.id != category_id
            ).first()
            if existing:
                return jsonify({'message': 'A category with this name already exists'}), 400
            category.name = name
            
        if description is not None:
            category.description = description
        
        try:
            db.session.commit()
            return jsonify({'message': 'Category updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error updating category', 'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        # Check if the category has any services
        if category.services:
            return jsonify({
                'message': 'Cannot delete category with associated services. Reassign or delete those services first.'
            }), 400
            
        try:
            db.session.delete(category)
            db.session.commit()
            return jsonify({'message': 'Category deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error deleting category', 'error': str(e)}), 500
    
    elif request.method == 'PATCH':
        category.is_active = not category.is_active
        db.session.commit()
        return jsonify({
            'message': 'Category status updated', 
            'is_active': category.is_active
        }), 200

@app.route('/api/categories/active', methods=['GET'])
def get_active_categories():
    """Get all active categories - available to all users"""
    try:
        categories = ServiceCategory.query.filter_by(is_active=True).all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
        } for c in categories])
    except Exception as e:
        return jsonify({'message': 'Error fetching categories', 'error': str(e)}), 500


@app.route('/api/services/active', methods=['GET'])
def get_active_services():
    try:
        services = Service.query.filter_by(is_active=True).all()
        return jsonify([{
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'time_required': service.time_required,
            'base_price': service.base_price,
            'image_file': service.image_file,
            'category_id': service.category_id,
            'service_pincodes': [loc.pin_code for loc in service.locations]
        } for service in services])
    except Exception as e:
        return jsonify({'message': 'Error fetching services', 'error': str(e)}), 500
    
@app.route('/service_images/<filename>')
def serve_service_image(filename):
    return send_from_directory(app.config['SERVICE_UPLOAD_FOLDER'], filename)

@app.route('/api/service-actions', methods=['POST'])
@login_required
def handle_service_action():
    data = request.json
    try:
        action_type = data['action_type']
        service_id = data['service_id']
        quantity = data.get('quantity', 1)

        # For cart, update quantity if exists
        if action_type == 'cart':
            existing = UserServiceAction.query.filter_by(
                user_id=current_user.id,
                service_id=service_id,
                action_type='cart'
            ).first()

            if existing:
                # Update existing cart item quantity
                existing.quantity += quantity
                db.session.commit()
                return jsonify({
                    'message': 'Cart quantity updated',
                    'new_quantity': existing.quantity
                }), 200
                
        # Handle buy_now - remove existing entry if exists
        elif action_type == 'buy_now':
            # Delete any existing buy_now entry for this service
            UserServiceAction.query.filter_by(
                user_id=current_user.id,
                service_id=service_id,
                action_type='buy_now'
            ).delete()
            db.session.commit()

        # Create new entry
        action = UserServiceAction(
            user_id=current_user.id,
            service_id=service_id,
            action_type=action_type,
            quantity=quantity
        )
        
        db.session.add(action)
        db.session.commit()        
        return jsonify({'message': 'Action completed successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

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
        
        required_fields = ['service_id', 'experience', 'phone_number', 'pincode']

        # Validate input for required fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        if current_user.role != 'user':
            return jsonify({'message': 'Already a professional/admin'}), 400
        if len(data.get('phone_number')) > 13:
            return jsonify({'message': 'Phone number too long'}), 400

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

        # Handle Address data instead of Customer data
        # Check if the user already has an address
        existing_address = Address.query.filter_by(user_id=user.id, is_default=True).first()
        
        address_data = {
            'user_id': user.id,
            'address_line1': data.get('address_line1'),
            'address_line2': data.get('address_line2'),
            'city': data.get('city'),
            'state': data.get('state'),
            'pincode': data.get('pincode'),
            'phone_number': data.get('phone_number'),
            'is_default': True
        }
        
        if existing_address:
            # Update existing address
            for key, value in address_data.items():
                if key != 'user_id':  # Don't update user_id
                    setattr(existing_address, key, value)
        else:
            # Create new address
            new_address = Address(**address_data)
            db.session.add(new_address)

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
                contact_number=data.get('phone_number', ''),
                verification_status='pending',
                is_available=True,
                rating=3.0
            )
            db.session.execute(stmt)
        else:
            # Get the existing professional to update
            professional = Professional.query.get(user.id)
            if professional:
                professional.experience = experience_value
                professional.service_type = service_id
                professional.contact_number = data.get('phone_number', '')
                professional.verification_status = 'pending'
                professional.is_available = True
                professional.rating = 3.0

        # Handle file upload if a file was provided
        if has_file:
            document_file = request.files['document']
            
            # Generate a secure filename
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
                    is_verified=False,
                    verified_by=None,
                    verified_at=None
                )
                db.session.add(new_document)

        db.session.commit()

        return jsonify({'message': 'Registration submitted for verification'}), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error in registration: {str(e)}")
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500

@app.route('/api/service-actions/<action_type>', methods=['GET'])
@login_required
def get_service_actions(action_type):
    actions = UserServiceAction.query.filter_by(
        user_id=current_user.id,
        action_type=action_type,
    ).join(Service).all()
    
    return jsonify([{
        'id': action.id,
        'quantity': action.quantity,
        'service': {
            'id': action.service.id,
            'name': action.service.name,
            'image_file': action.service.image_file,
            'base_price': action.service.base_price
        }
    } for action in actions])

@app.route('/api/service-actions/<int:action_id>', methods=['PATCH', 'DELETE'])
@login_required
def update_service_action(action_id):
    action = UserServiceAction.query.get_or_404(action_id)
    
    # Verify the action belongs to the current user
    if action.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403

    if request.method == 'PATCH':
        # Handle quantity updates
        data = request.json
        if 'quantity' in data:
            try:
                quantity = int(data['quantity'])
                if quantity < 1:
                    return jsonify({'message': 'Quantity must be at least 1'}), 400
                
                action.quantity = quantity
                db.session.commit()
                return jsonify({
                    'message': 'Quantity updated successfully',
                    'new_quantity': action.quantity
                })
            except ValueError:
                return jsonify({'message': 'Invalid quantity value'}), 400
        else:
            return jsonify({'message': 'No quantity provided'}), 400

    elif request.method == 'DELETE':
        try:
            db.session.delete(action)
            db.session.commit()
            return jsonify({
                'message': 'Item removed successfully',
                'removed_item_id': action_id
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'message': 'Failed to remove item',
                'error': str(e)
            }), 500
    
@app.route('/api/addresses', methods=['POST'])
@login_required
def add_address():
    data = request.json
    required_fields = ["address_line1", "address_line2", "city", "state", "pincode", "phone_number"]
    
    # Validate fields
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    # Unset existing default address if needed
    if data.get("is_default"):
        Address.query.filter_by(user_id=current_user.id).update({"is_default": False})

    new_address = Address(
        user_id=current_user.id,
        phone_number=data["phone_number"],
        address_line1=data["address_line1"],
        address_line2=data.get("address_line2", ""),
        city=data["city"],
        state=data["state"],
        pincode=data["pincode"],
        is_default=data.get("is_default", False)
    )
    db.session.add(new_address)
    try:
        db.session.commit()
        return jsonify({
            "message": "Address added",
            "address": {
                "id": new_address.id,
                "address_line1": new_address.address_line1,
                "address_line2": new_address.address_line2,
                "city": new_address.city,
                "state": new_address.state,
                "pincode": new_address.pincode,
                "phone_number": new_address.phone_number,
                "is_default": new_address.is_default
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error adding address", "error": str(e)}), 500
    
@app.route('/api/addresses', methods=['GET'])
@login_required
def get_addresses():
    addresses = Address.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        "id": addr.id,
        "address_line1": addr.address_line1,
        "address_line2": addr.address_line2,
        "city": addr.city,
        "state": addr.state,
        "pincode": addr.pincode,
        "phone_number": addr.phone_number,
        "is_default": addr.is_default
    } for addr in addresses])

@app.route('/api/block-user', methods=['POST'])
@admin_required
@login_required
def block_user():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'message': 'Email is required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Prevent blocking admins
    if user.role == 'admin':
        return jsonify({'message': 'Admins cannot be blocked'}), 400

    if user.id == current_user.id:
        return jsonify({'message': 'Cannot block yourself'}), 400

    user.is_blocked = not user.is_blocked
    db.session.commit()

    # If the user is blocked, log them out immediately
    if user.is_blocked:
        logout_user()

    return jsonify({
        'message': 'User status updated',
        'is_blocked': user.is_blocked,
        'email': user.email
    }), 200

@app.route('/api/pending-professionals', methods=['GET'])
@admin_required
def get_pending_professionals():
    pending_pros = Professional.query.filter_by(verification_status='pending').all()
    result = []
    
    for pro in pending_pros:
        user = User.query.get(pro.id)
        service = Service.query.get(pro.service_type)
        document = ProfessionalDocument.query.filter_by(professional_id=pro.id).first()
        default_address = Address.query.filter_by(user_id=user.id, is_default=True).first()
        
        result.append({
            'id': pro.id,
            'username': user.username,
            'experience': pro.experience,
            'service_name': service.name if service else 'N/A',
            'document_url': document.document_url if document else None,
            'pincode': default_address.pincode if default_address else 'N/A',
            'user_address': (
                f"{default_address.address_line1}, {default_address.city}, {default_address.state}"
                if default_address else "Address not available"
            ),
            'is_available': pro.is_available,
            'rating': pro.rating,
            'document_verified': document.is_verified if document else False
        })
    
    return jsonify(result), 200

@app.route('/api/update-professional-status/<int:pro_id>', methods=['PATCH'])
@admin_required
def update_professional_status(pro_id):
    data = request.json
    new_status = data.get('status')
    
    if new_status not in ['verified', 'rejected']:
        return jsonify({'message': 'Invalid status'}), 400
    
    professional = Professional.query.get_or_404(pro_id)
    professional.verification_status = new_status
    professional.verification_date = datetime.utcnow()
    professional.verified_by = current_user.id
    
    # Update ProfessionalDocument if the status is 'verified'
    if new_status == 'verified':
        user = User.query.get(pro_id)
        user.role = 'professional'
        
        # Update the associated ProfessionalDocument
        document = ProfessionalDocument.query.filter_by(professional_id=pro_id).first()
        if document:
            document.is_verified = True
            document.verified_by = current_user.id
            document.verified_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({'message': 'Status updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@app.route('/documents/<filename>')
@admin_required
def serve_document(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/orders/<int:order_id>', methods=['GET'])
@login_required
def get_order_details(order_id):
    order = ServiceRequest.query.get_or_404(order_id)
    
    if order.user_id != current_user.id and current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Get all service requests for this order (if grouped) or just this one
    items = ServiceRequest.query.filter(
        ServiceRequest.user_id == current_user.id,
        ServiceRequest.id == order_id  
    ).join(Service).all()
    
    # Calculate total correctly with quantity
    total = sum(item.total_amount for item in items)
    
    return jsonify({
        'order': {
            'id': order.id,
            'status': order.status,
            'scheduled_date': order.scheduled_date.isoformat(),
            'total_amount': total
        },
        'items': [{
            'id': item.id,
            'quantity': item.quantity,
            'service': {
                'id': item.service.id,
                'name': item.service.name,
                'base_price': item.service.base_price
            },
            'item_total': item.total_amount
        } for item in items],
        'total': total
    })

@app.route('/api/service-requests', methods=['POST'])
@login_required
def create_service_request():
    """Handle creation of service requests from both cart and buy-now flows"""
    try:
        # 1. Validate and parse input
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        required_fields = ['addressId', 'scheduledDate', 'orderType']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        # 2. Fetch address and parse datetime
        address = Address.query.get(data['addressId'])
        if not address:
            return jsonify({'error': 'Address not found'}), 404

        try:
            scheduled_date = datetime.fromisoformat(data['scheduledDate'])
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400

        # 3. Prepare items based on order type
        items = []
        if data['orderType'] == 'cart':
            # Get all cart items
            cart_items = UserServiceAction.query.filter_by(
                user_id=current_user.id,
                action_type='cart'
            ).join(Service).all()

            for item in cart_items:
                items.append({
                    'service_id': item.service_id,
                    'quantity': item.quantity or 1
                })

            # Delete all cart items
            UserServiceAction.query.filter_by(
                user_id=current_user.id,
                action_type='cart'
            ).delete()
        else:
            # Buy now flow - single item
            service_id = data.get('serviceId')
            if not service_id:
                return jsonify({'error': 'serviceId required for buy_now'}), 400

            quantity = data.get('quantity', 1)
            items.append({
                'service_id': service_id,
                'quantity': quantity
            })

            # Delete buy_now entry if exists
            UserServiceAction.query.filter_by(
                user_id=current_user.id,
                action_type='buy_now',
                service_id=service_id
            ).delete()

        # Create service requests
        created_requests = []
        for item in items:
            # Get the service details
            service = Service.query.get(item['service_id'])
            if not service:
                return jsonify({'error': f'Service {item["service_id"]} not found'}), 404

            total_amount = float(service.base_price or 0) * int(item['quantity'] or 1)

            service_request = ServiceRequest(
                service_id=item['service_id'],
                user_id=current_user.id,
                professional_id=None,
                scheduled_date=scheduled_date,
                location_pin=address.pincode,
                total_amount=total_amount,
                quantity=item['quantity'],
                status='pending'
            )
            db.session.add(service_request)
            created_requests.append(service_request.id)

        db.session.commit()

        return jsonify({
            'message': 'Service requests created successfully',
            'requests': created_requests
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/service-actions/cart', methods=['GET'])
@login_required
def get_cart_items():
    cart_items = UserServiceAction.query.filter_by(
        user_id=current_user.id,
        action_type='cart'
    ).join(Service).all()

    return jsonify([{
        'id': item.id,
        'quantity': item.quantity,
        'service': {
            'id': item.service.id,
            'name': item.service.name,
            'base_price': item.service.base_price,
            'image_file': item.service.image_file
        }
    } for item in cart_items]), 200

@app.route('/api/professional/service-requests', methods=['GET'])
@login_required
def get_professional_requests():
    try:
        if current_user.role != 'professional':
            return jsonify({'message': 'Access denied'}), 403

        # Get professional's service type
        service_type = db.session.query(Professional.service_type).filter(
            Professional.id == current_user.id
        ).scalar()

        # Get professional's default address pincode
        address = Address.query.filter_by(
            user_id=current_user.id, 
            is_default=True
        ).first()

        if not service_type or not address:
            return jsonify([]), 200

        # Query matching service requests
        requests = ServiceRequest.query.filter(
            ServiceRequest.service_id == service_type,
            ServiceRequest.location_pin == address.pincode,
            ServiceRequest.status == 'pending',
            ServiceRequest.professional_id.is_(None)
        ).all()

        response_data = []
        for req in requests:
            # Explicitly fetch user and address
            user = User.query.get(req.user_id)
            user_address = Address.query.filter_by(
                user_id=user.id, 
                is_default=True
            ).first() if user else None

            address_str = (
                f"{user_address.address_line1}, {user_address.city}" 
                if user_address else "Address not available"
            )

            response_data.append({
                'id': req.id,
                'service_name': Service.query.get(req.service_id).name,
                'scheduled_date': req.scheduled_date.isoformat(),
                'user_address': address_str,
                'quantity': req.quantity,
                'total_amount': req.total_amount
            })

        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error in get_professional_requests: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/professional/service-requests/<int:request_id>', methods=['PATCH'])
@login_required
def handle_service_request(request_id):
    if current_user.role != 'professional':
        return jsonify({'message': 'Access denied'}), 403

    req = ServiceRequest.query.get_or_404(request_id)
    data = request.get_json()

    if req.professional_id is not None:
        return jsonify({'message': 'Request already handled'}), 400

    if data.get('action') == 'accept':
        # Check for existing bookings at this time
        existing_booking = ServiceRequest.query.filter(
            ServiceRequest.professional_id == current_user.id,
            ServiceRequest.scheduled_date == req.scheduled_date,
            ServiceRequest.status.in_(['accepted', 'pending'])
        ).first()

        if existing_booking:
            return jsonify({
                'message': 'You already have a booking scheduled at this time',
                'conflicting_request': {
                    'id': existing_booking.id,
                    'service': existing_booking.service.name,
                    'scheduled_date': existing_booking.scheduled_date.isoformat()
                }
            }), 409

        req.professional_id = current_user.id
        req.status = 'accepted'
    elif data.get('action') == 'reject':
        req.status = 'rejected'
    else:
        return jsonify({'message': 'Invalid action'}), 400

    try:
        db.session.commit()
        return jsonify({
            'message': f'Request {data["action"]}ed successfully',
            'request': {
                'id': req.id,
                'status': req.status,
                'professional_id': req.professional_id,
                'scheduled_date': req.scheduled_date.isoformat()
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error updating request',
            'error': str(e)
        }), 500

def serialize_request(request):
    """Serialize a ServiceRequest object to JSON"""
    service = Service.query.get(request.service_id)
    professional = Professional.query.get(request.professional_id) if request.professional_id else None
    user = User.query.get(request.user_id) if request.user_id else None
    address = Address.query.filter_by(user_id=user.id, is_default=True).first() if user else None
    if address:
        address_parts = [
            address.address_line1,
            address.address_line2 if address.address_line2 else None,
            f"{address.city}, {address.state}",
            address.pincode
        ]
        full_address = ", ".join(filter(None, address_parts))
    else:
        full_address = "Address not available"
    
    # Get review if exists
    review = Review.query.filter_by(service_request_id=request.id).first()
    
    return {
        'id': request.id,
        'service_id': request.service_id,
        'service_name': service.name if service else 'Service not available',
        'user_id': request.user_id,
        'professional_id': request.professional_id,
        'professional_name': professional.username if professional else 'Not assigned',
        'request_date': request.request_date.isoformat() if request.request_date else None,
        'scheduled_date': request.scheduled_date.isoformat() if request.scheduled_date else None,
        'completion_date': request.completion_date.isoformat() if request.completion_date else None,
        'status': request.status,
        'location_pin': request.location_pin,
        'total_amount': request.total_amount,
        'quantity': request.quantity,
        'rating': review.rating if review else None,
        'review_comment': review.comment if review else None,
        'user_address': full_address,
        'scheduled_date': request.scheduled_date.isoformat() if request.scheduled_date else None,
    }

# Add these new routes to your existing api.py
@app.route('/api/professional/accepted-requests', methods=['GET'])
@login_required
def get_accepted_requests():
    if current_user.role != 'professional':
        return jsonify({'error': 'Access denied'}), 403
    
    requests = ServiceRequest.query.filter_by(
        professional_id=current_user.id,
        status='accepted'
    ).all()
    return jsonify([serialize_request(req) for req in requests])

@app.route('/api/professional/completed-requests', methods=['GET'])
@login_required
def get_completed_pro_requests():
    if current_user.role != 'professional':
        return jsonify({'error': 'Access denied'}), 403
    
    requests = ServiceRequest.query.filter_by(
        professional_id=current_user.id,
        status='completed'
    ).all()
    return jsonify([serialize_request(req) for req in requests])

@app.route('/api/user/current-requests', methods=['GET'])
@login_required
def get_user_requests():
    if current_user.role != 'user':
        return jsonify({'error': 'Access denied'}), 403
    
    requests = ServiceRequest.query.filter_by(
        user_id=current_user.id
    ).filter(ServiceRequest.status.in_(['pending', 'accepted'])).all()
    return jsonify([serialize_request(req) for req in requests])

@app.route('/api/user/completed-requests', methods=['GET'])
@login_required
def get_completed_user_requests():
    if current_user.role != 'user':
        return jsonify({'error': 'Access denied'}), 403
    
    requests = ServiceRequest.query.filter_by(
        user_id=current_user.id,
        status='completed'
    ).all()
    return jsonify([serialize_request(req) for req in requests])

@app.route('/api/service-requests/<int:req_id>/unassign', methods=['PATCH'])
@login_required
def unassign_request(req_id):
    req = ServiceRequest.query.get_or_404(req_id)
    
    if current_user.role != 'professional' or req.professional_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    req.professional_id = None
    req.status = 'pending'
    db.session.commit()
    return jsonify({'message': 'Request unassigned'})

@app.route('/api/service-requests/<int:req_id>/cancel', methods=['PATCH'])
@login_required
def cancel_request(req_id):
    req = ServiceRequest.query.get_or_404(req_id)
    
    if current_user.role != 'user' or req.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    req.status = 'cancelled'
    db.session.commit()
    return jsonify({'message': 'Request cancelled'})

@app.route('/api/service-requests/<int:req_id>/complete', methods=['PATCH'])
@login_required
def complete_request(req_id):
    req = ServiceRequest.query.get_or_404(req_id)
    
    if current_user.role != 'user' or req.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    req.status = 'completed'
    req.completion_date = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Request marked as completed'})

@app.route('/api/reviews', methods=['GET', 'POST'])
@login_required
def handle_reviews():
    if request.method == 'GET':
        request_id = request.args.get('request_id')
        if not request_id:
            return jsonify({'error': 'request_id parameter is required'}), 400
        
        review = Review.query.filter_by(service_request_id=request_id).first()
        if not review:
            return jsonify({}), 404
        
        return jsonify({
            'id': review.id,
            'rating': review.rating,
            'comment': review.comment,
            'date_created': review.date_created.isoformat()
        })

    elif request.method == 'POST':
        data = request.json
        request_id = data.get('request_id')
        
        if not request_id:
            return jsonify({'error': 'request_id is required'}), 400
        
        # Get professional_id from service request
        service_request = ServiceRequest.query.get(request_id)
        if not service_request:
            return jsonify({'error': 'Service request not found'}), 404
            
        existing = Review.query.filter_by(
            service_request_id=request_id,
            user_id=current_user.id
        ).first()
        
        if existing:
            return jsonify({'message': 'Review already exists'}), 400
            
        review = Review(
            service_request_id=request_id,
            professional_id=service_request.professional_id,
            user_id=current_user.id,
            rating=data['rating'],
            comment=data.get('comment', '')
        )
        
        try:
            db.session.add(review)
            db.session.commit()
            update_professional_rating(review.professional_id)
            return jsonify({'message': 'Review created'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@app.route('/api/reviews/<int:review_id>', methods=['PUT'])
@login_required
def update_review(review_id):
    review = Review.query.get(review_id)
    
    if not review or review.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
            
    data = request.json
    review.rating = data['rating']
    review.comment = data.get('comment', '')
    
    try:
        db.session.commit()
        update_professional_rating(review.professional_id)
        return jsonify({'message': 'Review updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/service-requests/<int:req_id>', methods=['GET', 'PATCH'])
@login_required
def service_request(req_id):
    req = ServiceRequest.query.get_or_404(req_id)
    
    if request.method == 'GET':
        # Authorization check
        if current_user.role not in ['admin', 'professional'] and req.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        return jsonify(serialize_request(req))

    elif request.method == 'PATCH':
        # Authorization check
        if current_user.role != 'admin' and req.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()
        
        # Update scheduled date
        if 'scheduled_date' in data:
            try:
                req.scheduled_date = datetime.fromisoformat(data['scheduled_date'])
            except ValueError:
                return jsonify({'error': 'Invalid date format'}), 400
        
        # Update quantity and recalculate total
        if 'quantity' in data:
            req.quantity = int(data['quantity'])
            service = Service.query.get(req.service_id)
            if service:
                req.total_amount = service.base_price * req.quantity

        try:
            db.session.commit()
            return jsonify(serialize_request(req)), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

def update_professional_rating(professional_id):
    professional = Professional.query.get(professional_id)
    if not professional:
        return
    
    reviews = Review.query.filter_by(professional_id=professional_id).all()
    if not reviews:
        professional.rating = 3.0
    else:
        total = sum(review.rating for review in reviews)
        professional.rating = round(total / len(reviews), 1)
    
    db.session.commit()

@app.route('/api/professionals/worst-performing')
@admin_required
@login_required
def get_worst_performers():
    try:
        performers = db.session.query(
            User.username,
            Professional.rating,
            Service.name.label('service_name')
        ).select_from(User
        ).join(Professional, User.id == Professional.id
        ).join(Service, Professional.service_type == Service.id
        ).filter(User.role == 'professional'
        ).distinct().order_by(Professional.rating.asc()
        ).limit(5).all()

        return jsonify([{
            'username': pro.username,
            'rating': float(pro.rating),
            'service_name': pro.service_name
        } for pro in performers]), 200

    except Exception as e:
        print(f"Error fetching worst performers: {str(e)}")
        return jsonify({'error': 'Failed to fetch performance data'}), 500
    
@app.route('/api/admin/service-requests', methods=['GET'])
@admin_required
def get_all_service_requests():
    requests = ServiceRequest.query.all()
    return jsonify([serialize_request(req) for req in requests])