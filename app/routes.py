from flask import Blueprint

main_blueprint = Blueprint('main', __name__)

# import from controllers
from app.controllers.AuthController import bp_authcontroller
from app.controllers.RoleController import bp_role
from app.controllers.UserController import bp_user
from app.controllers.HomeController import bp_home
from app.controllers.ModuleController import bp_module
from app.controllers.TaskController import bp_task
from app.controllers.PageController import bp_page
from app.controllers.SectionController import bp_section
from app.controllers.SliderController import bp_slider


# Define your routes and map them to controllers
# Registering the blueprint
def create_routes(app):
    app.register_blueprint(bp_authcontroller)
    app.register_blueprint(bp_role)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_home)
    app.register_blueprint(bp_module)
    app.register_blueprint(bp_task)
    app.register_blueprint(bp_page)
    app.register_blueprint(bp_section)
    app.register_blueprint(bp_slider)

