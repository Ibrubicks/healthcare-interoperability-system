"""
Pydantic Models for Request/Response Validation
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# ==========================================
# Enums
# ==========================================
class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    NURSE = "NURSE"
    EMERGENCY = "EMERGENCY"
    PATIENT = "PATIENT"

class ActionEnum(str, Enum):
    VIEW = "VIEW"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    EXPORT = "EXPORT"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"

class SeverityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

# ==========================================
# Authentication Models
# ==========================================
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1, max_length=100)
    role: RoleEnum
    department: Optional[str] = None
    hospital_id: Optional[int] = None
    
    @validator('password')
    def validate_password(cls, v):
        from security import validate_password_strength
        is_valid, message = validate_password_strength(v)
        if not is_valid:
            raise ValueError(message)
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[str] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# ==========================================
# User Models
# ==========================================
class UserResponse(BaseModel):
    user_id: str
    username: str
    email: str
    full_name: str
    role: str
    department: Optional[str]
    hospital_id: Optional[int]
    is_active: bool
    created_date: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    department: Optional[str] = None
    hospital_id: Optional[int] = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def validate_password(cls, v):
        from security import validate_password_strength
        is_valid, message = validate_password_strength(v)
        if not is_valid:
            raise ValueError(message)
        return v

# ==========================================
# Audit Log Models
# ==========================================
class AuditLogResponse(BaseModel):
    log_id: int
    user_id: str
    patient_id: Optional[int]
    action: str
    resource_type: Optional[str]
    resource_id: Optional[str]
    details: Optional[str]
    ip_address: Optional[str]
    status: str
    timestamp: datetime
    justification: Optional[str]
    
    class Config:
        from_attributes = True

class AuditLogQuery(BaseModel):
    user_id: Optional[str] = None
    patient_id: Optional[int] = None
    action: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(default=100, le=1000)

# ==========================================
# Emergency Access Models
# ==========================================
class BreakGlassRequest(BaseModel):
    patient_id: int
    justification: str = Field(..., min_length=10)
    emergency_type: str

class BreakGlassResponse(BaseModel):
    access_id: int
    user_id: str
    patient_id: int
    justification: str
    emergency_type: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

# ==========================================
# Consent Models
# ==========================================
class ConsentCreate(BaseModel):
    patient_id: int
    consent_type: str
    granted: bool
    granted_to_role: Optional[str] = None
    scope: Optional[Dict[str, Any]] = None
    expires_at: Optional[datetime] = None

class ConsentResponse(BaseModel):
    consent_id: int
    patient_id: int
    consent_type: str
    granted: bool
    granted_date: Optional[datetime]
    expires_at: Optional[datetime]
    scope: Optional[str]
    
    class Config:
        from_attributes = True

# ==========================================
# Session Models
# ==========================================
class SessionResponse(BaseModel):
    session_id: str
    user_id: str
    ip_address: Optional[str]
    created_at: datetime
    expires_at: datetime
    last_activity: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

# ==========================================
# Security Event Models
# ==========================================
class SecurityEventResponse(BaseModel):
    event_id: int
    event_type: str
    severity: str
    user_id: Optional[str]
    ip_address: Optional[str]
    description: str
    timestamp: datetime
    resolved: bool
    
    class Config:
        from_attributes = True

# ==========================================
# Response Models
# ==========================================
class MessageResponse(BaseModel):
    message: str
    status: str = "success"

class ErrorResponse(BaseModel):
    detail: str
    status: str = "error"

# ==========================================
# Patient Data Models (for HIPAA compliance)
# ==========================================
class PatientAccessRequest(BaseModel):
    patient_id: int
    purpose: str = Field(..., min_length=5)
    justification: Optional[str] = None

class PatientDataExport(BaseModel):
    patient_id: int
    format: str = Field(default="json", pattern="^(json|pdf|csv)$")
    include_audit_trail: bool = False

# ==========================================
# Permission Models
# ==========================================
class PermissionCheck(BaseModel):
    role: str
    permission: str

class PermissionResponse(BaseModel):
    has_permission: bool
    role: str
    permission: str

# ==========================================
# Statistics Models
# ==========================================
class SystemStats(BaseModel):
    total_users: int
    active_sessions: int
    total_audit_logs: int
    failed_login_attempts: int
    security_events_last_24h: int
    break_glass_accesses_last_24h: int
