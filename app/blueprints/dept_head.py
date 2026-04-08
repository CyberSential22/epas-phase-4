"""
Department Head Blueprint - Phase 4
Handles Department Head final approval and decision logic.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.event import Event, EventStatus
from app.utils.decorators import role_required
from app.utils.workflow import transition_status

dept_head_bp = Blueprint('dept_head', __name__)

@dept_head_bp.route('/dashboard')
@login_required
@role_required('Department Head')
def dashboard():
    """List events pending department head approval and show stats."""
    from datetime import datetime, timedelta, timezone
    from app.models.approval import Approval, ApprovalDecision, ApprovalLevel

    pending_events = Event.query.filter_by(status=EventStatus.Pending_Head).all()
    
    # Calculate stats
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)
    
    # Approved this week (by this user)
    approved_this_week = Approval.query.filter(
        Approval.approver_id == current_user.id,
        Approval.level == ApprovalLevel.DepartmentHead,
        Approval.decision == ApprovalDecision.Approved,
        Approval.timestamp >= week_ago
    ).count()

    # Rejected this week (by this user)
    rejected_count = Approval.query.filter(
        Approval.approver_id == current_user.id,
        Approval.level == ApprovalLevel.DepartmentHead,
        Approval.decision == ApprovalDecision.Rejected
    ).count()

    return render_template('dept_head/dashboard.html', 
                           events=pending_events,
                           pending_count=len(pending_events),
                           approved_count=approved_this_week,
                           rejected_count=rejected_count)

@dept_head_bp.route('/review/<int:event_id>', methods=['GET'])
@login_required
@role_required('Department Head')
def review(event_id):
    """View details and decision form for an event."""
    event = Event.query.get_or_404(event_id)
    if event.status != EventStatus.Pending_Head:
        flash("This event is not awaiting your review.", "warning")
        return redirect(url_for('dept_head.dashboard'))
    
    # In Dept Head view, we should show history (Faculty's comments)
    # The Approval model's relationships allow this via event.approvals
    return render_template('dept_head/review.html', event=event)

@dept_head_bp.route('/decide/<int:event_id>', methods=['POST'])
@login_required
@role_required('Department Head')
def decide(event_id):
    """Process the approval decision."""
    event = Event.query.get_or_404(event_id)
    decision = request.form.get('decision')
    comments = request.form.get('comments')

    success, message = transition_status(event, decision, current_user, comments)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
        return redirect(url_for('dept_head.review', event_id=event.id))

    return redirect(url_for('dept_head.dashboard'))
