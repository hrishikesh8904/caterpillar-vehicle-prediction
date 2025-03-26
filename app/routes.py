from flask import Blueprint, jsonify, request, redirect,render_template,session
from app.models.user import User, db,Data
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
import re
from datetime import datetime
from flask_migrate import Migrate
from app.mlmodels.model import RiskPredictor
import json
main = Blueprint('main', __name__)
bcrypt = Bcrypt()
jwt = JWTManager()
def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex,email)):
        return True
    else:
        return False
@main.route('/')
def home():
    if 'user_id' in session:
        return render_template('/dashboard.html',logged_in = True)
    return render_template('/dashboard.html',logged_in = False)

@main.route('/login')
def login_page():
    return render_template('login.html')

@main.route('/signup')
def signup_page():
    return render_template('signup.html')
@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html')
@main.route('/predict')
def predict():
    return render_template('predict.html')
@main.route('/signup',methods = ['POST'])
def signup_post():
    email = request.form['email']
    password = request.form['password']
    if(not check_email(email)):
        return jsonify({'message':'Invalid email'})
    user = User.query.filter_by(email=email).first()
    if (user):
        return jsonify({'message': 'User already exists'})
    hashed_password = bcrypt.generate_password_hash(password, 10).decode('utf-8')
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/login')


@main.route('/login',methods = ['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return render_template('login.html')
    session['user_id'] = user.id
    access_token = create_access_token(identity=user.id)
    return render_template('/dashboard.html',logged_in = True)

@main.route('/submit-form',methods = ['POST'])
def submit_form():
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    current_time = datetime.now()
    machine = request.form['machine']
    component = request.form['component']
    parameter = request.form['parameter']
    value = request.form['value']
    new_record = Data(id = user_id,time = current_time,machine = machine,component = component,parameter = parameter,value = value)
    db.session.add(new_record)
    db.session.commit()
    return redirect('/dashboard')
@main.route('/predict',methods = ['POST'])
def predict_post():
    if 'user_id' not in session:
        return redirect('/login')
    machine = request.form['machine']
    results = Data.query.filter_by(id = id,machine = machine).all()
    data = [{
        'id': result.id,
        'time': result.time,
        'machine': result.machine,
        'component': result.component,
        'parameter': result.parameter,
        'value': result.value
    } for result in results]
    
    predictor = RiskPredictor()
    predictions = predictor.predict(data)
    return render_template('/predict.html',results = predictions)

@main.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect('/')