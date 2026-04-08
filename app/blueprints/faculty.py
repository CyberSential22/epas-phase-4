"""
Faculty Blueprint - Phase 4
Handles Faculty Advisor review and decision logic.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.event import Event, EventStatus
from app.utils.decorators import role_required
from app.utils.workflow import transition_status

faculty_bp = Blueprint('faculty', __name__)

@faculty_bp.route('/dashboard')
@login_required
@role_required('Faculty')
def dashboard():
    """List events pending faculty approval."""
    pending_events = Event.query.filter_by(status=EventStatus.Pending_Faculty).all()
    return render_template('faculty/dashboard.html', events=pending_events)

@faculty_bp.route('/review/<int:event_id>', methods=['GET'])
@login_required
@role_required('Faculty')
def review(event_id):
    """View details and decision form for an event."""
    event = Event.query.get_or_404(event_id)
    if event.status != EventStatus.Pending_Faculty:
        flash("This event is not awaiting your review.", "warning")
        return redirect(url_for('faculty.dashboard'))
    return render_template('faculty/review.html', event=event)

@faculty_bp.route('/decide/<int:event_id>', methods=['POST'])
@login_required
@role_required('Faculty')
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
        return redirect(url_for('faculty.review', event_id=event.id))

    return redirect(url_for('faculty.dashboard'))
