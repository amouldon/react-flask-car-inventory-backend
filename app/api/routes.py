from flask import Blueprint, request, jsonify
from functools import wraps
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api', __name__, template_folder='api_templates', url_prefix='/api')

def token_required(flask_function):
    @wraps(flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'No token found'}), 401
        
        try:
            current_user_token = User.query.filter_by(token = token).first()
            if not current_user_token:
                return jsonify({'message': 'token is invalid'})      
        except:
            return jsonify({'message': 'Token is invalid'})
        return flask_function(current_user_token, *args, **kwargs)
    return decorated

@api.route('/add-car', methods=['POST'])
@token_required
def add_car(current_user_token):
    brand = request.json['brand']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    user_token = current_user_token.token

    car = Car(brand, model, year, color, user_token)
    db.session.add(car)
    db.session.commit()
    return jsonify({'message': 'A car has been added to your collection'})


@api.route('/view-collection', methods=['GET'])
@token_required
def view_collection(current_user_token):
    all_cars = Car.query.filter_by(user_token = current_user_token.token).all()
    if all_cars:
        output = cars_schema.dump(all_cars)
        return jsonify(output)
    else:
        return jsonify({'message': 'no cars found'})

@api.route('/view-car/<id>', methods=['GET'])
@token_required
def view_car(current_user_token, id):
    car = Car.query.filter_by(user_token = current_user_token.token, id = id ).first()
    if car:
        output = car_schema.dump(car)
        return jsonify(output)
    else:
        return jsonify({'message': 'no car found'})


@api.route('/delete/<id>', methods=['DELETE'])
@token_required
def delete_car(current_user_token, id):
    deleted_car = Car.query.filter_by(user_token = current_user_token.token, id = id).first()
    if deleted_car:
        db.session.delete(deleted_car)    
        db.session.commit()
        return jsonify({'message': 'Car has been removed from collection'})
    else:
        return jsonify({'message': 'Invalid Car ID'})

@api.route('/update/<id>', methods=['POST', 'PATCH'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.filter_by(user_token = current_user_token.token, id = id).first()
    if car and request.json['model'] and request.json['brand'] and request.json['year']:
        car.model = request.json['model']
        print(car.model)
        car.color = request.json['color']
        car.year = request.json['year']
        car.brand = request.json['brand']
        db.session.commit()
        return jsonify({'message': 'Car data has been updated'})
    else:
        print('invalid')
        return jsonify({'message': 'invalid'})