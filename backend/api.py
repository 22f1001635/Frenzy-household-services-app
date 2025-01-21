from models import *
from flask import Flask,jsonify,request

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
            return jsonify({'message': 'Login successful'}), 200
        
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