from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.TaskModel import TaskModel, TaskForm
from app.models.ModuleModel import ModuleModel
from app.config import Config
from app.models.mydb import db
from flask_login import login_required
from flask_wtf.csrf import generate_csrf

bp_task = Blueprint('bp_task', __name__)

@bp_task.route('/tasks')
@login_required
def listtasks():
    csrf_token = generate_csrf()
    tasks = TaskModel.get_all_tasks()
    return render_template('rbac/listtasks.html', tasks=tasks, moduletitle="Access Control", title='Tasks', app_name=Config.APP_NAME, author=Config.AUTHOR, csrf_token=csrf_token)


@bp_task.route('/addtask', methods=['GET', 'POST'])
@login_required
def addtask():
    base_url = request.host_url
    form = TaskForm(request.form)
    modules = ModuleModel.get_all_modules()
    if request.method == 'POST':
        if form.validate():
            module_id = form.module_id.data
            task_label = form.task_label.data
            task_url = form.task_url.data
            task_route = form.task_route.data
            task_method = form.task_method.data
            task_icon = form.task_icon.data
            # Convert string values to boolean
            isdashboard = form.isdashboard.data.lower() not in ('false', '0')
            isnavbar = form.isnavbar.data.lower() not in ('false', '0')

            # print("isdashboard data:", form.isdashboard.data, type(form.isdashboard.data))
            # print("isnavbar data:", form.isnavbar.data, type(form.isnavbar.data))
            
            # Create a new TaskModel instance
            newtask = TaskModel(module_id=module_id, task_label=task_label, task_url=task_url, task_route=task_route, task_method=task_method, task_icon=task_icon, isdashboard=isdashboard, isnavbar=isnavbar)
            # Add the new task to the database session
            db.session.add(newtask)
            # Commit changes to the database
            db.session.commit()
            flash('Task added successfully.', 'success')             
            return jsonify({'success':True})
        else:
            errors = form.errors
            return jsonify({'errors':errors})

    return render_template('rbac/addtask.html', form=form, base_url=base_url, modules=modules)
 

@bp_task.route('/edittask/<int:id>', methods=['GET', 'POST'])
@login_required
def edittask(id):
    task = TaskModel.query.get_or_404(id)
    base_url = request.host_url
    modules = ModuleModel.get_all_modules()
    form = TaskForm(original_title=task.task_route, obj=task)
    if request.method == 'POST':
        if form.validate():
            task.module_id = form.module_id.data
            task.task_label = form.task_label.data
            task.task_url = form.task_url.data
            task.task_route = form.task_route.data
            task.task_method = form.task_method.data
            task.task_icon = form.task_icon.data
            # Convert string values to boolean
            task.isdashboard = form.isdashboard.data.lower() not in ('false', '0')
            task.isnavbar = form.isnavbar.data.lower() not in ('false', '0')                        
            # Commit changes to the database
            db.session.commit()
            flash('Task updated successfully.', 'success')            
            return jsonify({'success':True})
        else:
            errors = form.errors
            return jsonify({'errors':errors})
    return render_template('rbac/edittask.html', modules=modules, form=form, task=task, base_url=base_url)
    

@bp_task.route('/deletetask/<int:id>', methods=['GET','DELETE'])
@login_required
def deletetask(id):
    # Find the task record by ID
    task = TaskModel.query.get(id)
    if task:
        # Delete the task record from the database session
        db.session.delete(task)
        # Commit the session to permanently delete the record from the database
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'message': 'Task not found'}), 404

