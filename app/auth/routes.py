from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/sign-up', methods=['POST'])
def sign_up():
    try:
        email = request.json['email']
        password = request.json['password']
        if not email or not password:
            return jsonify({'message': 'invalid input'})
        test_user = User.query.filter_by(email = email).first()
        if test_user:
            return jsonify({'message': 'email is in use'})
        user = User(email, password)
        db.session.add(user)
        db.session.commit()
        print(user.token)
        return jsonify({'token': user.token})
    except:
        print('failed')
        return jsonify({'message': 'failed'})

@auth.route('/sign-in', methods=['POST'])
def sign_in():
    try:
        email = request.json['email']
        password = request.json['password']
        if not email or not password:
            return jsonify({'message': 'invalid input'})
        user = User.query.filter_by(email = email).first()
        if user and check_password_hash(user.password, password):
            return jsonify({'token': user.token})
        else:
            return jsonify({'message': 'Login failed, invalid credentials'})
    except:
        return jsonify({'message': 'login failed'})
