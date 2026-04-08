"""
Admin Blueprint - Phase 4.5
Handles administrative tasks and system-wide overview.
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from app.models.user import User
from app.models.event import Event

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@role_required('Admin')
def dashboard():
    """System-wide overview for Administrators."""
    from app.models.event import EventStatus
    from app.models.approval import Approval
    
    user_count = User.query.count()
    event_count = Event.query.count()
    
    # Global pending approvals
    pending_global = Event.query.filter(Event.status.in_([EventStatus.Pending_Faculty, EventStatus.Pending_Head])).count()
    
    # Recent Activity (last 5 approvals)
    recent_activity = Approval.query.order_by(Approval.timestamp.desc()).limit(5).all()
    
    users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                           user_count=user_count, 
                           event_count=event_count,
                           pending_global=pending_global,
                           recent_activity=recent_activity,
                           users=users)
