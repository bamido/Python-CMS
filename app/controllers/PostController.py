from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.ThreadModel import ThreadModel
from app.models.PostModel import PostModel, PostForm
from app.config import Config
from app.models.mydb import db
from flask_login import login_required, current_user
from flask_wtf.csrf import generate_csrf
from slugify import slugify
from app.utils import allowed_file, resize_image, create_thumbnail
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
import os
import uuid


bp_post = Blueprint('bp_post', __name__)

@bp_post.route('/posts')
@login_required
def listposts():
    csrf_token = generate_csrf()
    # get all posts
    posts = PostModel.get_posts()
    return render_template('blog/listallposts.html', posts=posts, moduletitle="Blog(CMS)", title='Posts', app_name=Config.APP_NAME, author=Config.AUTHOR, csrf_token=csrf_token)


@bp_post.route('/addpost/<int:id>', methods=['GET', 'POST'])
@login_required
def addpost(id):
    base_url = request.host_url
    form = PostForm(request.form)
    threads = ThreadModel.get_all_threads()
    user_id = current_user.user_id
    if request.method == 'POST':
        if form.validate():
            thread_id = form.thread_id.data            
            posttitle = form.posttitle.data
            postslug = slugify(form.posttitle.data)
            postintro = form.postintro.data.encode('utf-8')
            postbody = form.postbody.data.encode('utf-8')
            postimageurl = form.imageurl.data
            postvideourl = form.postvideourl.data            
            poststatus = form.poststatus.data
            postview = form.postview.data
            sortorder = form.sortorder.data
            metakeyword = form.metakeyword.data
            metadesc = form.metadesc.data
            
            # process post image upload
            if 'imageurl' in request.files:
                file = request.files['imageurl']
                if file and allowed_file(file.filename):
                    # Generate a unique filename using UUID
                    file_extension = file.filename.rsplit('.', 1)[1].lower()
                    unique_filename = str(uuid.uuid4()) + '.' + file_extension

                    # Secure the filename and save it
                    original_path = os.path.join(Config.UPLOAD_PHOTO_DIR, secure_filename(unique_filename))
                    file.save(original_path)

                    # Resize the original image
                    resized_image_path = os.path.join(Config.UPLOAD_PHOTO_DIR, unique_filename)
                    resize_image(original_path, resized_image_path, base_width=800)  # Resize to 800px width

                    # Create a thumbnail
                    thumbnail_path = os.path.join(Config.UPLOAD_PHOTO_DIR, 'thumb_' + unique_filename)
                    create_thumbnail(resized_image_path, thumbnail_path, thumb_size=(450, 450))
            
                    # Create a new ThreadModel instance
                    thumbfilename = 'thumb_' + unique_filename
                    newpost = PostModel(thread_id=thread_id, user_id=user_id, posttitle=posttitle, postslug=postslug, postintro=postintro, postbody=postbody, postimageurl=thumbfilename, postvideourl=postvideourl, postview=1, poststatus=poststatus, sortorder=sortorder, metakeyword=metakeyword, metadesc=metadesc)
                    # Add the new post to the database session
                    db.session.add(newpost)
                    # Commit changes to the database
                    db.session.commit()
                    flash('Post added successfully.', 'success')  
                    return jsonify({'success':True})
        else:
            errors = form.errors
            return jsonify({'errors':errors})

    return render_template('blog/addpost.html', form=form, base_url=base_url, threads=threads, id=id)



@bp_post.route('/editpost/<int:id>', methods=['GET', 'POST'])
@login_required
def editpost(id):
    base_url = request.host_url    
    threads = ThreadModel.get_all_threads()
    post = PostModel.query.get(id)
    form = PostForm(original_title=post.posttitle, original_thread_id=post.thread_id, original_imageurl=post.postimageurl, is_update=True, formdata=request.form)
    if request.method == 'POST':
        if form.validate():
            
            # If validation passes, update the Post with the new values          
            post.thread_id = form.thread_id.data            
            post.posttitle = form.posttitle.data
            post.postslug = slugify(form.posttitle.data)
            post.postintro = form.postintro.data.encode('utf-8')
            post.postbody = form.postbody.data.encode('utf-8')
            post.postvideourl = form.postvideourl.data            
            post.poststatus = form.poststatus.data            
            post.sortorder = form.sortorder.data
            post.metakeyword = form.metakeyword.data
            post.metadesc = form.metadesc.data

            # process slide image upload
            if 'imageurl' in request.files and request.files['imageurl'].filename:
                file = request.files['imageurl']
                if file and allowed_file(file.filename):
                    # Remove the existing image if it exists
                    existing_image_path = os.path.join(Config.UPLOAD_PHOTO_DIR, post.postimageurl.replace("thumb_", ""))
                    existing_thumbnail_path = os.path.join(Config.UPLOAD_PHOTO_DIR, post.postimageurl)                    
                    # Delete the old image
                    if os.path.exists(existing_image_path):
                        os.remove(existing_image_path)  
                    if os.path.exists(existing_thumbnail_path):
                        os.remove(existing_thumbnail_path)
                                        
                    # Generate a unique filename using UUID
                    file_extension = file.filename.rsplit('.', 1)[1].lower()
                    unique_filename = str(uuid.uuid4()) + '.' + file_extension

                    # Secure the filename and save it
                    original_path = os.path.join(Config.UPLOAD_PHOTO_DIR, secure_filename(unique_filename))
                    file.save(original_path)

                    # Resize the original image
                    resized_image_path = os.path.join(Config.UPLOAD_PHOTO_DIR, unique_filename)
                    resize_image(original_path, resized_image_path, base_width=800)  # Resize to 800px width

                    # Create a thumbnail
                    thumbnail_path = os.path.join(Config.UPLOAD_PHOTO_DIR, 'thumb_' + unique_filename)
                    create_thumbnail(resized_image_path, thumbnail_path, thumb_size=(450, 450))
            
                    # new postimageurl
                    post.postimageurl = 'thumb_' + unique_filename                    
                    # Commit changes to the database                                          
                    db.session.commit()
                     
                    flash('Post updated successfully.', 'success')  
                    return jsonify({'success':True})
            else:
                db.session.commit()
                flash('Post updated successfully.', 'success')  
                return jsonify({'success':True})
        else:                  
            errors = form.errors
            return jsonify({'errors':errors})

    return render_template('blog/editpost.html', form=form, base_url=base_url, threads=threads, post=post)


@bp_post.route('/deletepost/<int:id>', methods=['GET', 'DELETE'])
def deletepost(id):
    # find post by id
    post = PostModel.query.get(id)
    if post:
        #db.session.delete(post)
        post.poststatus = 'Deleted'
        db.session.commit()
        return jsonify({'message': 'Post deleted successfully'}), 200
    else:
        return jsonify({'message': 'Post not found'}), 404
