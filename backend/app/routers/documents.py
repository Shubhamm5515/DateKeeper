from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date
from pydantic import BaseModel
from app.database import get_db
from app.models import Document
from app.models.user import User
from app.auth import get_current_user

router = APIRouter(prefix="/api/documents", tags=["Documents"])

# Pydantic schemas
class DocumentCreate(BaseModel):
    document_name: str
    document_type: str
    expiry_date: date
    # Email and phone come from user profile now

class DocumentUpdate(BaseModel):
    document_name: str | None = None
    document_type: str | None = None
    expiry_date: date | None = None
    status: str | None = None

class DocumentResponse(BaseModel):
    id: str
    user_id: str
    document_name: str
    document_type: str
    expiry_date: date
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/", response_model=DocumentResponse)
def create_document(
    document: DocumentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new document (requires authentication)"""
    
    # Calculate status based on expiry date
    today = datetime.now().date()
    days_until_expiry = (document.expiry_date - today).days
    
    if days_until_expiry < 0:
        status = "expired"
    elif days_until_expiry <= 7:
        status = "expiring_soon"
    elif days_until_expiry <= 30:
        status = "expiring_this_month"
    else:
        status = "valid"
    
    # Create document linked to current user
    db_document = Document(
        user_id=current_user.id,
        document_name=document.document_name,
        document_type=document.document_type,
        expiry_date=document.expiry_date,
        status=status,
        # Use user's email and phone from profile
        email=current_user.email,
        phone=current_user.phone,
        notify_email=current_user.notify_email,
        notify_sms=current_user.notify_sms
    )
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return db_document

@router.get("/", response_model=List[DocumentResponse])
def get_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all documents for current user (requires authentication)"""
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    return documents

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific document (requires authentication)"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id  # Ensure user owns this document
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document

@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: str,
    document_update: DocumentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a document (requires authentication)"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id  # Ensure user owns this document
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Update fields
    if document_update.document_name:
        document.document_name = document_update.document_name
    if document_update.document_type:
        document.document_type = document_update.document_type
    if document_update.expiry_date:
        document.expiry_date = document_update.expiry_date
    if document_update.status:
        document.status = document_update.status
    
    document.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(document)
    
    return document

@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a document (requires authentication)"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id  # Ensure user owns this document
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}

@router.get("/stats/summary")
def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get document statistics for current user (requires authentication)"""
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    
    total = len(documents)
    expired = sum(1 for d in documents if d.status == "expired")
    expiring_soon = sum(1 for d in documents if d.status in ["expiring_soon", "expiring_this_month"])
    valid = sum(1 for d in documents if d.status == "valid")
    
    return {
        "total": total,
        "expired": expired,
        "expiring_soon": expiring_soon,
        "valid": valid
    }
