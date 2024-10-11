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
from bs4 import BeautifulSoup
from markupsafe import Markup  # Import from markupsafe
import bleach


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
    # print('userid,useriduserid,useriduserid,useriduserid,userid')
    # print(user_id)
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
    

# Define the custom filter
@app.template_filter('excerpt')
def excerpt_filter(html_content, max_length=100):
    # Strip HTML tags using BeautifulSoup
    soup = BeautifulSoup(html_content, 'lxml')
    plain_text = soup.get_text(separator=' ', strip=True)

    # Truncate the text
    if len(plain_text) > max_length:
        return plain_text[:max_length].rsplit(' ', 1)[0] + '...'
    return plain_text


@app.template_filter('decode_and_safe')
def decode_and_safe(blob):
    if isinstance(blob, bytes):
        decoded_str = blob.decode('utf-8')
        cleaned_str = bleach.clean(decoded_str)  # Clean the HTML for safety
        return Markup(cleaned_str)
    return blob

# Register the filter with the Jinja2 environment
app.jinja_env.filters['excerpt'] = excerpt_filter 
app.jinja_env.filters['decode_and_safe'] = decode_and_safe 
