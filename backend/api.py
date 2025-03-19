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
    action = UserServiceAction(
        user_id=current_user.id,
        service_id=data['service_id'],
        action_type=data['action_type'],
        quantity=data.get('quantity', 1)
    )
    
    try:
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

@app.route('/api/service-actions/<action_type>', methods=['GET'])
@login_required
def get_service_actions(action_type):
    actions = UserServiceAction.query.filter_by(
        user_id=current_user.id,
        action_type=action_type,
        is_active=True
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

@app.route('/api/service-actions/<int:action_id>', methods=['DELETE'])
@login_required
def delete_service_action(action_id):
    action = UserServiceAction.query.get_or_404(action_id)
    if action.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    try:
        db.session.delete(action)
        db.session.commit()
        return jsonify({'message': 'Item removed successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500