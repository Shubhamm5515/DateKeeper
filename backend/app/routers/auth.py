"""
Authentication routes - Register, Login, User Profile, Google OAuth
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import timedelta
from authlib.integrations.starlette_client import OAuth
from app.database import get_db
from app.models.user import User
from app.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_active_user
)
from app.config import settings
import secrets

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Initialize OAuth
oauth = OAuth()

# Configure Google OAuth
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Pydantic schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    phone: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str | None
    phone: str | None
    notify_email: str
    notify_sms: str
    is_active: bool
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    notify_email: str | None = None
    notify_sms: str | None = None

class ReminderSettings(BaseModel):
    alternate_email: str | None = None
    reminder_intervals: dict | None = None
    notify_email: str | None = None
    notify_sms: str | None = None

@router.post("/register", response_model=Token)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    
    - Email will be used for login and notifications
    - Password must be at least 6 characters
    - Returns JWT token for immediate login
    """
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate password
    if len(user_data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        phone=user_data.phone,
        notify_email="Y",  # Enable email notifications by default
        notify_sms="N" if not user_data.phone else "Y"  # Enable SMS if phone provided
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_user.to_dict()
    }

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password
    
    Returns JWT token for authentication
    """
    
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Create access token
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

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """
    Get current user profile
    
    Requires authentication
    """
    return current_user

@router.put("/me", response_model=UserResponse)
def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile
    
    Can update: full_name, phone, notification preferences
    """
    
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    
    if user_update.phone is not None:
        current_user.phone = user_update.phone
    
    if user_update.notify_email is not None:
        current_user.notify_email = user_update.notify_email
    
    if user_update.notify_sms is not None:
        current_user.notify_sms = user_update.notify_sms
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

@router.post("/logout")
def logout(current_user: User = Depends(get_current_active_user)):
    """
    Logout (client should delete token)
    
    JWT tokens are stateless, so logout is handled client-side
    """
    return {"message": "Successfully logged out"}

@router.get("/settings")
def get_reminder_settings(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get user's reminder settings
    
    Returns:
    - alternate_email: Optional alternate email for reminders
    - reminder_intervals: Which reminder intervals are enabled
    - notify_email: Email notification preference
    - notify_sms: SMS notification preference
    """
    return {
        "alternate_email": current_user.alternate_email,
        "reminder_intervals": current_user.reminder_intervals or {
            "6_months": True,
            "3_months": True,
            "1_month": True,
            "7_days": True
        },
        "notify_email": current_user.notify_email,
        "notify_sms": current_user.notify_sms
    }

@router.put("/settings")
def update_reminder_settings(
    settings: ReminderSettings,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update user's reminder settings
    
    Can update:
    - alternate_email: Send reminders to this email instead of primary
    - reminder_intervals: Enable/disable specific reminder intervals
    - notify_email: Enable/disable email notifications
    - notify_sms: Enable/disable SMS notifications
    """
    
    if settings.alternate_email is not None:
        current_user.alternate_email = settings.alternate_email
    
    if settings.reminder_intervals is not None:
        current_user.reminder_intervals = settings.reminder_intervals
    
    if settings.notify_email is not None:
        current_user.notify_email = settings.notify_email
    
    if settings.notify_sms is not None:
        current_user.notify_sms = settings.notify_sms
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "Settings updated successfully",
        "settings": {
            "alternate_email": current_user.alternate_email,
            "reminder_intervals": current_user.reminder_intervals,
            "notify_email": current_user.notify_email,
            "notify_sms": current_user.notify_sms
        }
    }

# Google OAuth Routes
@router.get("/google/login")
async def google_login(request: Request):
    """
    Initiate Google OAuth login
    
    Redirects user to Google login page
    """
    redirect_uri = f"{settings.FRONTEND_URL}/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """
    Handle Google OAuth callback
    
    Creates or logs in user with Google account
    Returns JWT token for frontend
    """
    try:
        # Get token from Google
        token = await oauth.google.authorize_access_token(request)
        
        # Get user info from Google
        user_info = token.get('userinfo')
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from Google"
            )
        
        email = user_info.get('email')
        full_name = user_info.get('name')
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not provided by Google"
            )
        
        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Create new user
            # Generate random password (user won't use it, only Google OAuth)
            random_password = secrets.token_urlsafe(32)
            hashed_password = get_password_hash(random_password)
            
            user = User(
                email=email,
                hashed_password=hashed_password,
                full_name=full_name,
                notify_email="Y",
                is_verified=True  # Google accounts are pre-verified
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=access_token_expires
        )
        
        # Redirect to frontend with token
        frontend_url = f"{settings.FRONTEND_URL}/auth/google/success?token={access_token}&user={user.email}"
        return RedirectResponse(url=frontend_url)
        
    except Exception as e:
        # Redirect to frontend with error
        error_url = f"{settings.FRONTEND_URL}/login?error=google_auth_failed"
        return RedirectResponse(url=error_url)
