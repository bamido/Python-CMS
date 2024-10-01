from flask import request, url_for, abort, redirect, render_template
from flask_login import login_required, current_user, login_user
from app.models.TaskModel import TaskModel
from app.models.UserModel import UserModel
from app.models.PrivilegeModel import PrivilegeModel
from app.models.mydb import db
import sys
#from app.controllers.AuthController import forbidden_handler


class AuthorizationMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        
        return self.app(environ, start_response)
      
    def process_request(self):
        
        user_role = get_user_role()
        current_route = request.path
        
        #print(current_user.role_id)
        # if not current_user.is_authenticated:
        #     # Redirect to login page or handle unauthenticated access (e.g., 401 Unauthorized)
        #     return redirect(url_for('bp_authcontroller.login')) 
        # if not self.is_exempt_route(request.endpoint):
        #     return False
        if current_user.is_authenticated:
            #print(current_user.role_id)
            if has_privilege(current_user.role_id, current_route):
                return True
            elif current_route in ['/', '/login', '/register', '/logout']:
                return True
            else:
                #return False
                #abort(403)
                abort(403, description="You are not authorized to access this resource.")
                
        

    def is_exempt_route(self, endpoint):
        print('inside exempt route')
        # Check if the route is associated with the current request
        if request.endpoint is not None:
            # Check if the route is decorated with the unprotected_route decorator
            view_func = self.app.view_functions.get(endpoint)
            if hasattr(view_func, '_unprotected_route') and view_func._unprotected_route:
                return True
        # If no endpoint is associated with the current request, or if the endpoint
        # is not decorated with @unprotected_route, consider it not exempt
        return False

def has_privilege(user_role, route):
    # Check if the requested route is a static file
    if route.startswith('/static/'):
        return True  # Allow access to static files without checking privileges

    # Query to check if the user's role has access to the current route
    theroute = remove_last_part(route)
    #print(theroute)
    task_route = db.session.query(TaskModel.task_route).join(PrivilegeModel, TaskModel.task_id == PrivilegeModel.task_id).filter(PrivilegeModel.role_id == user_role, TaskModel.task_route == theroute).scalar()
    # print('################ Route ********')
    # print(route)  
    # print('The query output')
    # print(task_route)
    if task_route is None:
        return False
    else:
        return True

def remove_last_part(url):
    # Split the string by the last '/' into three parts
    head, sep, tail = url.rpartition('/')
    # If there's something after the last '/', return the part before it
    if head and tail:
        return head
    # Otherwise, return the original string (if it doesn't need modification)
    return url


def get_user_role():
    return "admin"  # Placeholder, replace with actual logic


def forbidden_handler():
    errors = "You are not authorized to access this resource. Contact the Super Admin!"
    return render_template('errors/403.html', title="Forbidden", errors=errors), 403  # Render a custom template

