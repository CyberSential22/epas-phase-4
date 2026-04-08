"""
Audit Log Model - Phase 4.x
Tracks all critical actions taken in the system for security and compliance.
"""
from datetime import datetime, timezone
from app import db

class AuditLog(db.Model):
    """Stores security auditing information for all user actions."""
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(200), nullable=False) # e.g. "Event Submitted", "Member Approved"
    target_id = db.Column(db.Integer, nullable=True)     # e.g. ID of the Event or User
    target_type = db.Column(db.String(100), nullable=True) # e.g. "Event", "User"
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    user = db.relationship('User', backref=db.backref('audit_logs', lazy=True))

    def __repr__(self):
        return f'<AuditLog {self.id} - {self.action} by User {self.user_id}>'
