from models import *
from flask import Flask,jsonify,request

@app.route('/api/login',request=['POST'])
def login():
    data=request.get_json()
    user=User.query.filter_by(email=data(['email']).first())
    if user and user.check_password(data(['password'])):
        login_user(user)
        return jsonify({
            'message':'Login Successful!',
            'user':
                    {
                        'id':user.id,
                        'username':user.username,
                        'email':user.email
                    }
            })
    return jsonify({'error': 'Invalid credentials'}), 401
@app.route('/api/register',request=['POST'])
def register():
    data=request.get_json()
    if User.query.filter_by(email=data(['email']).first()):
        return jsonify({'error': 'Email already registered'}), 400
    user = User(
        email=data['email'],
        name=data.get('name', '')
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Registration successful'}), 201

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})
