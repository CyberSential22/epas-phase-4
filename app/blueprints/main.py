from flask import Blueprint, render_template, current_app, redirect, url_for, request
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """System Home Page."""
    return render_template('main/index.html', status="Operational")

@main_bp.route('/get-started')
def get_started():
    """Dynamic starting point redirection."""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login', next=request.path))
    
    # Redirection based on role
    if current_user.role.name == 'Student':
        return redirect(url_for('events.student_dashboard'))
    elif current_user.role.name == 'Faculty':
        return redirect(url_for('faculty.dashboard'))
    elif current_user.role.name == 'DeptHead':
        return redirect(url_for('dept_head.dashboard'))
    elif current_user.role.name == 'Admin':
        return redirect(url_for('admin.dashboard'))
    
    return redirect(url_for('main.index'))

@main_bp.route('/about')
def about():
    """Project Information Page."""
    return render_template('main/about.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Generic dashboard entry point - redirects to role-specific dashboard."""
    return redirect(url_for('main.get_started'))
