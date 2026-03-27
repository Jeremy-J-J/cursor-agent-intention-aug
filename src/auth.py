"""
Minimal authentication system with user registration, login, password hashing,
session management, and role-based access control.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import secrets
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import secrets
import os

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password.
    
    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password to compare against
        
    Returns:
        True if the passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password.
    
    Args:
        password: The plain text password to hash
        
    Returns:
        The hashed password string
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token.
    
    Args:
        data: Dictionary containing data to encode in the token
        expires_delta: Optional timedelta for token expiration
        
    Returns:
        The encoded JWT token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get the current authenticated user from the token.
    
    Args:
        token: The JWT token string from the authorization header
        
    Returns:
        The authenticated User object
        
    Raises:
        HTTPException: If the token is invalid or user not found
def authenticate_user(username: str, password: str) -> Optional[User]:
    """Authenticate a user by checking username and password.
    
    Args:
        username: The username to authenticate
        password: The password to verify
        
    Returns:
        The authenticated User object if successful, None otherwise
    """
    user = users_db.get(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(user_data: UserCreate) -> User:
    """Create a new user with hashed password.
    
    Args:
        user_data: UserCreate object containing user registration details
        
    Returns:
        The newly created User object
def create_session(username: str) -> str:
    """Create a session for a user.
    
    Args:
        username: The username to create a session for
        
    Returns:
        The session ID string
    """
    session_id = secrets.token_urlsafe(32)
    sessions_db[session_id] = {
        "username": username,
        "created_at": datetime.utcnow()
    }
    return session_id

def validate_session(session_id: str) -> Optional[str]:
    """Validate a session and return the associated username.
    
    Args:
        session_id: The session ID to validate
        
    Returns:
        The username associated with the session if valid, None otherwise
    """
    session = sessions_db.get(session_id)
    if not session:
        return None
    # Check if session is expired (simple 1-hour expiration)
    if datetime.utcnow() - session["created_at"] > timedelta(hours=1):
        del sessions_db[session_id]
        return None
    return session["username"]
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return user

def authenticate_user(username: str, password: str) -> Optional[User]:
    """Authenticate a user by checking username and password."""
    user = users_db.get(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(user_data: UserCreate) -> User:
    """Create a new user with hashed password."""
    if user_data.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    users_db[user_data.username] = user
    return user

def create_session(username: str) -> str:
    """Create a session for a user."""
    session_id = secrets.token_urlsafe(32)
    sessions_db[session_id] = {
        "username": username,
        "created_at": datetime.utcnow()
    }
    return session_id

def validate_session(session_id: str) -> Optional[str]:
    """Validate a session and return the associated username."""
    session = sessions_db.get(session_id)
    if not session:
        return None
    # Check if session is expired (simple 1-hour expiration)
    if datetime.utcnow() - session["created_at"] > timedelta(hours=1):
        del sessions_db[session_id]
        return None
    return session["username"]