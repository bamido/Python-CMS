from flask import session

def load_user_from_session(environ):
  # Extract user ID from session (replace with your logic)
  user_id = session.get('user_id')
  if user_id:
    # Load user object from database based on user ID
    from app.models.UserModel import UserModel  # Import user model
    user = UserModel.query.get(user_id)
    return user
  else:
    return None


from functools import wraps

# def unprotected_route(func):
#   @wraps(func)
#   def decorated_view(*args, **kwargs):
#     # No authentication or authorization checks here
#     return func(*args, **kwargs)
#   return decorated_view

def unprotected_route(view_func):
    # Decorator for routes that should be exempt from process_request logic
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view._unprotected_route = True
    return wrapped_view  