from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from app import db
from app.models.user import User, UserRole
from app.forms.auth_form import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data,
            role=UserRole.Student,
            department=form.department.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        # Log the user in directly after registration
        login_user(user)
        flash('Registration successful!', 'success')
        return redirect(url_for('events.student_dashboard'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Check if input is email or username
        user = User.query.filter((User.username == form.username.data) | (User.email == form.username.data)).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        
        from app.utils.ip_utils import get_client_ip
        from app.models.audit import AuditLog

        login_user(user, remember=form.remember.data)
        
        # Log the successful login (Audit)
        try:
            audit = AuditLog(
                user_id=user.id,
                action="User Login",
                details=f"Successful login for {user.username} as {user.role.value}",
                ip_address=get_client_ip(request)
            )
            db.session.add(audit)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Audit log failed: {str(e)}")

        # If user was redirected here from a protected page, redirect them back
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            # Priority Role-Based Redirection
            if user.role.value == 'Admin':
                next_page = url_for('admin.dashboard')
            elif user.role.value == 'Department Head':
                next_page = url_for('dept_head.dashboard')
            elif user.role.value == 'Faculty':
                next_page = url_for('faculty.dashboard')
            else: # Default to Student
                next_page = url_for('events.student_dashboard')
            
        flash(f'Logged in successfully as {user.role.value}.', 'success')
        return redirect(next_page)
        
    return render_template('auth/login.html', title='Sign In', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
