"""
Google OAuth Authentication
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from datetime import timedelta
from app.database import get_db
from app.models.user import User
from app.auth import create_access_token, get_password_hash
from app.config import settings
import secrets

router = APIRouter(prefix="/api/auth/google", tags=["Google OAuth"])

class GoogleLoginRequest(BaseModel):
    token: str  # Google ID token from frontend

@router.post("/login")
async def google_login(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    """
    Login or register with Google OAuth
    
    Frontend sends Google ID token, backend verifies it and creates/logs in user
    """
    
    try:
        # Verify the Google token
        idinfo = id_token.verify_oauth2_token(
            request.token,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
        
        # Extract user info from Google
        email = idinfo.get('email')
        name = idinfo.get('name')
        google_id = idinfo.get('sub')
        email_verified = idinfo.get('email_verified', False)
        
        if not email:
            raise HTTPException(status_code=400, detail="Email not provided by Google")
        
        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        
        if user:
            # User exists - login
            if not user.is_active:
                raise HTTPException(status_code=403, detail="Account is inactive")
            
            # Update user info if needed
            if not user.full_name and name:
                user.full_name = name
            if not user.is_verified and email_verified:
                user.is_verified = True
            
            db.commit()
            db.refresh(user)
        else:
            # User doesn't exist - register
            # Generate a random password (user won't use it, only for OAuth)
            random_password = secrets.token_urlsafe(32)
            hashed_password = get_password_hash(random_password)
            
            user = User(
                email=email,
                hashed_password=hashed_password,
                full_name=name,
                is_verified=email_verified,
                notify_email="Y"
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create JWT token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user.to_dict()
        }
        
    except ValueError as e:
        # Invalid token
        raise HTTPException(
            status_code=401,
            detail=f"Invalid Google token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Google authentication failed: {str(e)}"
        )
