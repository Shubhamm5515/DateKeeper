from sqlalchemy import Column, String, Date, DateTime, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.database import Base

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    document_name = Column(String(255), nullable=False)
    document_type = Column(String(50), nullable=False)
    expiry_date = Column(Date, nullable=False, index=True)
    reminder_sent = Column(JSON, default={})
    status = Column(String(20), default="valid")
    
    # Notification preferences
    email = Column(String(255), nullable=True)  # User email for notifications
    phone = Column(String(20), nullable=True)   # User phone for SMS (E.164 format)
    notify_email = Column(String(1), default="Y")  # Y/N
    notify_sms = Column(String(1), default="N")    # Y/N
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "document_name": self.document_name,
            "document_type": self.document_type,
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "reminder_sent": self.reminder_sent,
            "status": self.status,
            "email": self.email,
            "phone": self.phone,
            "notify_email": self.notify_email,
            "notify_sms": self.notify_sms,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
