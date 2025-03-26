from flask import Flask,render_template
from app.models.user import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .routes import main as main_blueprint
from flask_migrate import Migrate
import os
bcrypt = Bcrypt()
jwt = JWTManager()
def create_app():
    app = Flask(__name__,template_folder=os.path.abspath('templates'),static_folder=os.path.abspath('static'))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8904%40qwnmDjkiqabhi@localhost:5432/caterpillar'
    app.config['SECRET_KEY'] = 'your_secret_key'
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    app.register_blueprint(main_blueprint)
    migrate = Migrate(app,db)
    with app.app_context():
        db.create_all()
        
    return app