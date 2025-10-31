"""
Authentication and Security Utilities - HIPAA Compliant
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from cryptography.fernet import Fernet
import secrets
import hashlib
import json

# Security Configuration
SECRET_KEY = secrets.token_urlsafe(32)  # In production, load from environment
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
SESSION_TIMEOUT_MINUTES = 30
MAX_FAILED_ATTEMPTS = 5
ACCOUNT_LOCKOUT_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Field-level encryption key (In production, use proper key management)
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# ==========================================
# Password Management
# ==========================================
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password meets HIPAA requirements:
    - At least 8 characters
    - Contains uppercase and lowercase
    - Contains numbers
    - Contains special characters
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"

# ==========================================
# JWT Token Management
# ==========================================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Dict[str, Any]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# ==========================================
# Field-Level Encryption (for PHI)
# ==========================================
def encrypt_field(data: str) -> str:
    """Encrypt sensitive field data"""
    if not data:
        return None
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_field(encrypted_data: str) -> str:
    """Decrypt sensitive field data"""
    if not encrypted_data:
        return None
    return cipher_suite.decrypt(encrypted_data.encode()).decode()

def encrypt_phi_fields(data: dict, fields_to_encrypt: list) -> dict:
    """Encrypt specified PHI fields in a dictionary"""
    encrypted_data = data.copy()
    for field in fields_to_encrypt:
        if field in encrypted_data and encrypted_data[field]:
            encrypted_data[field] = encrypt_field(str(encrypted_data[field]))
    return encrypted_data

def decrypt_phi_fields(data: dict, fields_to_decrypt: list) -> dict:
    """Decrypt specified PHI fields in a dictionary"""
    decrypted_data = data.copy()
    for field in fields_to_decrypt:
        if field in decrypted_data and decrypted_data[field]:
            try:
                decrypted_data[field] = decrypt_field(decrypted_data[field])
            except Exception:
                pass  # Field might not be encrypted
    return decrypted_data

# ==========================================
# Session Management
# ==========================================
def generate_session_id() -> str:
    """Generate unique session ID"""
    return secrets.token_urlsafe(32)

def is_session_expired(last_activity: datetime) -> bool:
    """Check if session has expired due to inactivity"""
    timeout = timedelta(minutes=SESSION_TIMEOUT_MINUTES)
    return datetime.utcnow() - last_activity > timeout

# ==========================================
# Role-Based Access Control (RBAC)
# ==========================================
ROLE_PERMISSIONS = {
    "ADMIN": {
        "can_view_phi": True,
        "can_edit_phi": True,
        "can_delete_phi": True,
        "can_manage_users": True,
        "can_view_audit_logs": True,
        "can_export_data": True,
        "can_access_all_patients": True,
    },
    "DOCTOR": {
        "can_view_phi": True,
        "can_edit_phi": True,
        "can_delete_phi": False,
        "can_manage_users": False,
        "can_view_audit_logs": False,
        "can_export_data": True,
        "can_access_all_patients": False,
    },
    "NURSE": {
        "can_view_phi": True,
        "can_edit_phi": True,
        "can_delete_phi": False,
        "can_manage_users": False,
        "can_view_audit_logs": False,
        "can_export_data": False,
        "can_access_all_patients": False,
    },
    "EMERGENCY": {
        "can_view_phi": True,
        "can_edit_phi": True,
        "can_delete_phi": False,
        "can_manage_users": False,
        "can_view_audit_logs": False,
        "can_export_data": False,
        "can_access_all_patients": True,
        "break_glass_access": True,
    },
    "PATIENT": {
        "can_view_phi": True,
        "can_edit_phi": False,
        "can_delete_phi": False,
        "can_manage_users": False,
        "can_view_audit_logs": True,  # Can view their own access logs
        "can_export_data": True,  # Can export their own data
        "can_access_all_patients": False,
    },
}

def check_permission(role: str, permission: str) -> bool:
    """Check if role has specific permission"""
    return ROLE_PERMISSIONS.get(role, {}).get(permission, False)

def get_role_permissions(role: str) -> dict:
    """Get all permissions for a role"""
    return ROLE_PERMISSIONS.get(role, {})

# ==========================================
# Data Masking
# ==========================================
def mask_ssn(ssn: str) -> str:
    """Mask SSN to show only last 4 digits"""
    if not ssn or len(ssn) < 4:
        return "***-**-****"
    return f"***-**-{ssn[-4:]}"

def mask_phone(phone: str) -> str:
    """Mask phone number to show only last 4 digits"""
    if not phone or len(phone) < 4:
        return "***-***-****"
    return f"***-***-{phone[-4:]}"

def mask_email(email: str) -> str:
    """Mask email address"""
    if not email or "@" not in email:
        return "***@***.***"
    parts = email.split("@")
    if len(parts[0]) > 2:
        return f"{parts[0][:2]}***@{parts[1]}"
    return f"***@{parts[1]}"

def apply_data_masking(data: dict, role: str) -> dict:
    """
    Apply data masking based on role
    Nurses and lower roles see masked sensitive data
    """
    if role in ["ADMIN", "DOCTOR", "EMERGENCY"]:
        return data  # Full access
    
    masked_data = data.copy()
    
    # Mask sensitive fields for NURSE and PATIENT roles
    if "ssn" in masked_data and masked_data["ssn"]:
        masked_data["ssn"] = mask_ssn(masked_data["ssn"])
    
    if "phone" in masked_data and masked_data["phone"]:
        masked_data["phone"] = mask_phone(masked_data["phone"])
    
    if "email" in masked_data and masked_data["email"]:
        masked_data["email"] = mask_email(masked_data["email"])
    
    # Patient role should only see their own full data
    if role == "PATIENT":
        # Additional restrictions can be applied
        pass
    
    return masked_data

# ==========================================
# Security Headers
# ==========================================
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}

# ==========================================
# Audit Log Helpers
# ==========================================
def create_audit_entry(
    user_id: str,
    action: str,
    resource_type: str,
    resource_id: str,
    status: str,
    details: dict = None,
    patient_id: int = None,
    ip_address: str = None,
    user_agent: str = None,
    session_id: str = None,
    justification: str = None,
) -> dict:
    """Create audit log entry structure"""
    return {
        "user_id": user_id,
        "patient_id": patient_id,
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "details": json.dumps(details) if details else None,
        "ip_address": ip_address,
        "user_agent": user_agent,
        "status": status,
        "timestamp": datetime.utcnow(),
        "session_id": session_id,
        "justification": justification,
    }

# ==========================================
# Rate Limiting Helpers
# ==========================================
def get_rate_limit_key(identifier: str, endpoint: str) -> str:
    """Generate rate limit key"""
    return f"rate_limit:{identifier}:{endpoint}"

# ==========================================
# Security Utilities
# ==========================================
def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    if not text:
        return text
    # Remove potentially dangerous characters
    dangerous_chars = ["<", ">", "&", "'", '"', ";", "--", "/*", "*/"]
    for char in dangerous_chars:
        text = text.replace(char, "")
    return text.strip()

def generate_api_key() -> str:
    """Generate secure API key"""
    return secrets.token_urlsafe(32)

def hash_api_key(api_key: str) -> str:
    """Hash API key for storage"""
    return hashlib.sha256(api_key.encode()).hexdigest()
