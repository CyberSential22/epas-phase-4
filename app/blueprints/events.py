"""
Events Blueprint - Phase 2
Handles event creation, submission, and confirmation.
"""
from flask import (
    Blueprint, render_template, redirect,
    url_for, flash, current_app, request
)
from app import db
from app.models.event import Event, EventStatus
from app.forms.event_form import EventSubmissionForm
from flask_login import login_required, current_user
from app.utils.decorators import role_required

events_bp = Blueprint('events', __name__, template_folder='../templates')

@events_bp.route('/dashboard')
@login_required
@role_required('Student')
def student_dashboard():
    """List events created by the current student."""
    from app.models.event import Event
    events = Event.query.filter_by(created_by=current_user.id).order_by(Event.created_at.desc()).all()
    return render_template('main/dashboard.html', role='Student', events=events)


@events_bp.route('/create', methods=['GET'])
@login_required
@role_required('Student')
def create_event():
    """GET /events/create — Render the empty event submission form."""
    form = EventSubmissionForm()
    return render_template('events/create.html', form=form)


@events_bp.route('/submit', methods=['POST'])
@login_required
@role_required('Student')
def submit_event():
    """
    POST /events/submit — Validate and persist a new event.

    Workflow:
    1. Bind form data and validate.
    2. Instantiate Event model with form values.
    3. Commit inside a try/except (rollback on failure).
    4. Log the action and flash a user-facing message.
    5. Redirect to the confirmation page on success.
    """
    form = EventSubmissionForm()

    if form.validate_on_submit():
        try:
            from datetime import datetime
            event = Event(
                # Basic Info
                title=form.title.data.strip(),
                description=form.description.data.strip(),
                event_type=form.event_type.data,
                venue=form.venue.data.strip(),
                event_date=form.event_date.data,
                start_time=datetime.combine(form.event_date.data, form.start_time.data),
                end_time=datetime.combine(form.event_date.data, form.end_time.data),
                # Audience
                audience_type=form.audience_type.data,
                audience_size=form.audience_size.data,
                is_external_audience=form.is_external_audience.data,
                # Technical
                requires_projector=form.requires_projector.data,
                requires_microphone=form.requires_microphone.data,
                requires_live_streaming=form.requires_live_streaming.data,
                technical_requirements=(
                    form.technical_requirements.data.strip()
                    if form.technical_requirements.data else None
                ),
                # Security
                requires_security=form.requires_security.data,
                security_requirements=(
                    form.security_requirements.data.strip()
                    if form.security_requirements.data else None
                ),
                # Budget
                budget=form.budget.data,
                budget_breakdown=(
                    form.budget_breakdown.data.strip()
                    if form.budget_breakdown.data else None
                ),
                # Status & Ownership
                status=EventStatus.Pending_Faculty,
                created_by=current_user.id
            )

            db.session.add(event)
            db.session.commit()

            current_app.logger.info(
                'Event submitted successfully: "%s" (ID: %d, Ref: %s)',
                event.title, event.id, event.reference_id
            )
            flash(
                f'Your event proposal "{event.title}" has been submitted '
                f'successfully! Reference: {event.reference_id}',
                'success'
            )
            return redirect(url_for('events.confirmation', event_id=event.id))

        except Exception as exc:
            db.session.rollback()
            current_app.logger.error(
                'Database error while submitting event: %s', str(exc)
            )
            flash(
                'An unexpected error occurred while saving your event. '
                'Please try again.',
                'danger'
            )

    else:
        # Form validation failed — log field errors for debugging
        current_app.logger.warning(
            'Event form validation failed: %s', form.errors
        )

    # Re-render with validation errors intact
    return render_template('events/create.html', form=form)


@events_bp.route('/confirmation/<int:event_id>')
def confirmation(event_id):
    """GET /events/confirmation/<id> — Show submission success details."""
    event = Event.query.get_or_404(event_id)
    return render_template('events/confirmation.html', event=event)

@events_bp.route('/edit/<int:event_id>', methods=['GET'])
@login_required
@role_required('Student')
def edit_event(event_id):
    """GET /events/edit/<id> — Render the form to edit an event."""
    event = Event.query.get_or_404(event_id)
    
    # Ownership and Status check
    if event.created_by != current_user.id:
        flash("You do not have permission to edit this event.", "danger")
        return redirect(url_for('main.index'))
    
    if event.status not in [EventStatus.Draft, EventStatus.Changes_Requested]:
        flash(f"Events in '{event.status.value}' status cannot be edited.", "warning")
        return redirect(url_for('main.index'))
    
    form = EventSubmissionForm(obj=event)
    return render_template('events/edit.html', form=form, event=event)

@events_bp.route('/update/<int:event_id>', methods=['POST'])
@login_required
@role_required('Student')
def update_event(event_id):
    """POST /events/update/<id> — Update an existing event."""
    event = Event.query.get_or_404(event_id)
    
    if event.created_by != current_user.id:
        flash("You do not have permission to update this event.", "danger")
        return redirect(url_for('main.index'))
    
    if event.status not in [EventStatus.Draft, EventStatus.Changes_Requested]:
        flash(f"Events in '{event.status.value}' status cannot be updated.", "warning")
        return redirect(url_for('main.index'))
    
    form = EventSubmissionForm()
    if form.validate_on_submit():
        try:
            form.populate_obj(event)
            
            # Workflow Logic: Revert to previous approver level if it was 'Changes Requested'
            if event.status == EventStatus.Changes_Requested:
                # Find the last approval level that requested changes
                from app.models.approval import Approval, ApprovalDecision, ApprovalLevel
                last_approval = Approval.query.filter_by(event_id=event.id).order_by(Approval.timestamp.desc()).first()
                
                if last_approval and last_approval.level == ApprovalLevel.DepartmentHead:
                    # If Dept Head requested changes, it might go back to Dept Head or Faculty.
                    # Usually, if it's "Changes Requested", it goes back to the one who asked.
                    event.status = EventStatus.Pending_Head
                    event.current_approver_role = 'Department Head'
                else:
                    # Default: go back to Faculty
                    event.status = EventStatus.Pending_Faculty
                    event.current_approver_role = 'Faculty'
            else:
                # If it was Draft, now it's submitted
                event.status = EventStatus.Pending_Faculty
                event.current_approver_role = 'Faculty'
            
            db.session.commit()
            flash("Event updated and resubmitted successfully.", "success")
            return redirect(url_for('events.confirmation', event_id=event.id))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating event: {str(e)}", "danger")
    
    return render_template('events/edit.html', form=form, event=event)
