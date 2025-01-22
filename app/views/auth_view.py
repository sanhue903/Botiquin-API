from app.models import User, Role
from app.extensions import db
from flask import jsonify, abort
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from datetime import timedelta

def sign_up_view(email: str, password: str):
    new_user = User(email, password)
    
    role_name = "admin" if not db.session.scalar(db.select(User)) else "default"
    role = db.session.scalar(db.select(Role).where(Role.name == role_name))
    
    if not role:
        abort(500, "No existe los roles correspondientes") 
    
    new_user.role_id = role.id
    
    db.session.add(new_user)
    db.session.commit()     
    
    return jsonify({"message": f"User {new_user.email} created"}), 201

def log_in_view(user: User):
    access_token = create_access_token(identity=user.id,
                                       expires_delta=timedelta(days=365))
    
    response = jsonify({"message": "login successful"})
    set_access_cookies(response, access_token)
    
    return response, 201

def log_out_view():
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    
    return response, 201

def profile_view(user):
    return jsonify({"email": user.email, "role": user.role.name}), 200
    