"""
Authentication Middleware and Dependencies - HIPAA Compliant
"""
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import database
import security
from database import User, Session as DBSession, AuditLog, SecurityEvent

# HTTP Bearer token authentication
security_scheme = HTTPBearer()

# ==========================================
# Get Current User from Token
# ==========================================
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(database.get_db),
    request: Request = None
) -> User:
    """
    Verify token and return current authenticated user
    """
    token = credentials.credentials
    
    try:
        # Verify token
        payload = security.verify_token(token)
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        
        # Get user from database
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )
        
        # Check if account is locked
        if user.locked_until and user.locked_until > datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is temporarily locked due to failed login attempts",
            )
        
        # Verify session exists and is valid
        session = db.query(DBSession).filter(
            DBSession.token == token,
            DBSession.user_id == user_id,
            DBSession.is_active == True,
            DBSession.revoked == False
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session not found or expired",
            )
        
        # Check session expiration
        if session.expires_at < datetime.utcnow():
            session.is_active = False
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session has expired",
            )
        
        # Check session timeout due to inactivity
        if security.is_session_expired(session.last_activity):
            session.is_active = False
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session timeout due to inactivity",
            )
        
        # Update last activity
        session.last_activity = datetime.utcnow()
        db.commit()
        
        return user
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

# ==========================================
# Get Current Active User
# ==========================================
async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Ensure user is active"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user

# ==========================================
# Role-Based Access Control
# ==========================================
def require_role(*allowed_roles: str):
    """
    Dependency to check if user has required role
    Usage: dependencies=[Depends(require_role("ADMIN", "DOCTOR"))]
    """
    async def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker

def require_permission(permission: str):
    """
    Dependency to check if user has specific permission
    Usage: dependencies=[Depends(require_permission("can_view_phi"))]
    """
    async def permission_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if not security.check_permission(current_user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required permission: {permission}"
            )
        return current_user
    return permission_checker

# ==========================================
# Admin Only Access
# ==========================================
async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Require admin role"""
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# ==========================================
# Emergency Access (Break Glass)
# ==========================================
async def verify_emergency_access(
    current_user: User = Depends(get_current_active_user),
    justification: str = None
) -> User:
    """
    Verify emergency/break-glass access
    Requires justification and logs the access
    """
    if current_user.role != "EMERGENCY":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Emergency role required for break-glass access"
        )
    
    if not justification or len(justification.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emergency access requires detailed justification (minimum 10 characters)"
        )
    
    return current_user

# ==========================================
# Audit Logging Dependency
# ==========================================
async def log_access(
    action: str,
    resource_type: str,
    resource_id: str,
    patient_id: Optional[int] = None,
    status: str = "SUCCESS",
    details: dict = None,
    justification: str = None,
    current_user: User = Depends(get_current_active_user),
    request: Request = None,
    db: Session = Depends(database.get_db)
):
    """
    Create audit log entry
    This should be called after every PHI access
    """
    # Get client info
    ip_address = request.client.host if request else None
    user_agent = request.headers.get("user-agent") if request else None
    
    # Create audit log
    audit_entry = AuditLog(
        user_id=current_user.user_id,
        patient_id=patient_id,
        action=action,
        resource_type=resource_type,
        resource_id=str(resource_id),
        details=str(details) if details else None,
        ip_address=ip_address,
        user_agent=user_agent,
        status=status,
        justification=justification,
    )
    
    db.add(audit_entry)
    db.commit()
    
    return audit_entry

# ==========================================
# Security Event Logging
# ==========================================
def log_security_event(
    event_type: str,
    severity: str,
    description: str,
    user_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    details: dict = None,
    db: Session = None
):
    """Log security events for monitoring"""
    if not db:
        return
    
    event = SecurityEvent(
        event_type=event_type,
        severity=severity,
        user_id=user_id,
        ip_address=ip_address,
        description=description,
        details=str(details) if details else None
    )
    
    db.add(event)
    db.commit()

# ==========================================
# Optional User (for public endpoints)
# ==========================================
async def get_optional_user(
    request: Request,
    db: Session = Depends(database.get_db)
) -> Optional[User]:
    """
    Get user if authenticated, return None if not
    Used for endpoints that work with or without authentication
    """
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        token = auth_header.replace("Bearer ", "")
        payload = security.verify_token(token)
        user_id = payload.get("sub")
        
        if user_id:
            user = db.query(User).filter(User.user_id == user_id).first()
            return user
    except:
        pass
    
    return None
