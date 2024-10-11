import os
import uuid
from flask import session
from werkzeug.utils import secure_filename
from PIL import Image
from app.config import Config

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

    # Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_IMG_EXTENSIONS

# Resize image function
def resize_image(image_path, output_path, base_width):
    img = Image.open(image_path)
    w_percent = (base_width / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)
    img.save(output_path)

# Create a thumbnail function
def create_thumbnail(image_path, thumbnail_path, thumb_size=(150, 150)):
    img = Image.open(image_path)
    img.thumbnail(thumb_size)
    img.save(thumbnail_path)
    