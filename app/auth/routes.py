from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required
from ..models import User, db

auth = Blueprint('auth', __name__)

from flask import render_template, request, redirect, url_for

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  
    
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
    else:
        
        email = request.form.get('email')
        password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(password):
        login_user(user)
        if request.is_json:
            return jsonify({'message': 'Logged in successfully'}), 200
        return redirect(url_for('files.list_files'))  

    if request.is_json:
        return jsonify({'error': 'Invalid credentials'}), 401
    return render_template('login.html', error='Invalid credentials')


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged Out'}), 200

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email already registered'}), 400

    new_user = User(
        username=data.get('username'),
        email=data.get('email')
    )
    new_user.set_password(data.get('password'))

    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201
