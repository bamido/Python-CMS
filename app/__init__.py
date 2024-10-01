from flask import Flask, render_template
from app.config import Config
from app.routes import create_routes
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import modelsref
from app.models.UserModel import UserModel
from app.models.PrivilegeModel import PrivilegeModel
from app.models.mydb import db
from flask_login import LoginManager
from app.middleware.AuthorizationMiddleware import AuthorizationMiddleware
from app.utils import load_user_from_session



def create_app():
    app = Flask(__name__)  # flask app object
    app.config.from_object(Config)  # application's configuration    
    db.init_app(app) # Initializing the database
    with app.app_context():
        print(db.engine.url)
    
    return app

app = create_app()  # Creating the app
create_routes(app) # Registering the blueprint
migrate = Migrate(app, db)  # Initializing the migration
login_manager = LoginManager(app)

# Wrap the app's WSGI app with the authorization middleware
authorization_middleware = AuthorizationMiddleware(app.wsgi_app)

@login_manager.user_loader
def load_user(user_id):
    #print(user_id)
    # Load and return a user instance based on user_id
    user = UserModel.query.get(user_id)
    user.module_tasks = UserModel.get_user_tasks(user.role_id)
    return user 

@login_manager.unauthorized_handler
def unauthorized():
    # Customize the unauthorized page here
    return render_template('auth/unauthorized.html'), 403  # You can customize the status code as well


@app.before_request
def before_request():    
    authorization_middleware.process_request()    
    