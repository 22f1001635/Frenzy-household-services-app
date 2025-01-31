from models import *
from flask import Flask,jsonify,request
from functools import wraps

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
    #get credentials 
    data = request.json
    username=data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password=data.get('confirm_password')

    if not email or not password or not username or not confirm_password:
        return jsonify({
            'message': 'Provide Complete Credentials'
        }), 400
    else:
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        elif(password==confirm_password):
            user = User(
                email=email,
                username=username,
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'Registration successful'}), 201
        return jsonify({
            'message': 'Password mismatch found'
        }), 401

@app.route('/api/current_user', methods=['GET'])
@login_required
def current_user_info():
    return jsonify({
        'user': {
            'id': current_user.id,
            'email': current_user.email,
            'username': current_user.username,
            'role': current_user.role
        }
    })

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({
        'message': 'Sign Out! Successful'
    }),200
    
@app.route('/api/data')
def get_data():
    return jsonify({
        'message': 'Successfully connected to Flask backend!'
    })


@app.route('/api/addservice', methods=['POST'])
@admin_required
@login_required
def add_service():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    time_required = data.get('time_required')
    service_pincodes = data.get('service_pincodes')
    price = data.get('price')

    # Validate input presence
    if not all([name, price, description, time_required, service_pincodes]):
        return jsonify({'message': 'All fields are required'}), 400

    try:

        service = Service(
            name=name,
            description=description,
            time_required=time_required,
            base_price=price,  
            service_area=service_pincodes 
        )

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