from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.ThreadModel import ThreadModel, ThreadForm
from app.models.PostModel import PostModel
from app.config import Config
from app.models.mydb import db
from flask_login import login_required
from flask_wtf.csrf import generate_csrf
from slugify import slugify

bp_thread = Blueprint('bp_thread', __name__)


@bp_thread.route('/threads')
@login_required
def listthreads():
    csrf_token = generate_csrf()
    # get all threads
    threads = ThreadModel.get_threads_with_post_count()
    
    return render_template('blog/listthreads.html', threads=threads, moduletitle="Blog(CMS)", title='Threads', app_name=Config.APP_NAME, author=Config.AUTHOR, csrf_token=csrf_token)

@bp_thread.route('/addthread', methods=['GET', 'POST'])
@login_required
def addthread():
    base_url = request.host_url
    form = ThreadForm(request.form)
    if request.method == 'POST':
        if form.validate():
            threadname = form.threadname.data
            threadslug = slugify(form.threadname.data)
            threadstatus = form.threadstatus.data
            sortorder = form.sortorder.data
            
            # Create a new ThreadModel instance
            newthread = ThreadModel(threadname=threadname, threadslug=threadslug,  threadstatus=threadstatus, sortorder=sortorder)
            # Add the new thread to the database session
            db.session.add(newthread)
            # Commit changes to the database
            db.session.commit()
            flash('Thread added successfully.', 'success')  
            return jsonify({'success':True})
        else:
            errors = form.errors
            return jsonify({'errors':errors})

    return render_template('blog/addthread.html', form=form, base_url=base_url)



@bp_thread.route('/editthread/<int:id>', methods=['GET', 'POST'])
@login_required
def editthread(id):
    thread = ThreadModel.query.get_or_404(id)
    base_url = request.host_url
    form = ThreadForm(original_title=thread.threadname, obj=thread)    
    if request.method == 'POST':
        if form.validate():
            thread.threadname = form.threadname.data
            thread.threadslug = slugify(form.threadname.data)            
            thread.threadstatus = form.threadstatus.data
            thread.sortorder = form.sortorder.data                       
            # Commit changes to the database
            db.session.commit()
            flash('Thread updated successfully.', 'success')            
            return jsonify({'success':True})
        else:
            errors = form.errors
            return jsonify({'errors':errors})
    return render_template('blog/editthread.html', form=form, thread=thread, base_url=base_url)


@bp_thread.route('/deletethread/<int:id>', methods=['GET', 'DELETE'])
@login_required
def deletethread(id):
    # find thread by id
    thread = ThreadModel.query.get(id)
    if thread:
        #db.session.delete(thread)
        thread.threadstatus = 'Deleted'
        db.session.commit()
        return jsonify({'message': 'Thread deleted successfully'}), 200
    else:
        return jsonify({'message': 'Thread not found'}), 404


@bp_thread.route('/threadposts/<int:id>', methods=['GET'])
@login_required
def listthreadposts(id):
    csrf_token = generate_csrf()
    # get thread posts
    threadposts = ThreadModel.get_thread_posts(id)
    thread = ThreadModel.query.get(id)
    title = thread.threadname + ' Thread Posts'

    return render_template('blog/listposts.html', threadposts=threadposts, moduletitle="Blog(CMS)", title=title, app_name=Config.APP_NAME, author=Config.AUTHOR, csrf_token=csrf_token, id=id, thread=thread)
