"""
SQLite Database Configuration for Authentication & Security Tables
Separate from Oracle database for patient records
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# SQLite Database for authentication and security
SQLALCHEMY_DATABASE_URL = "sqlite:///./security.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ==========================================
# Users Table - HIPAA Compliant
# ==========================================
class User(Base):
    __tablename__ = "users"
    
    user_id = Column(String(50), primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)  # ADMIN, DOCTOR, NURSE, EMERGENCY, PATIENT
    department = Column(String(100))
    hospital_id = Column(Integer)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(100))
    created_date = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    password_changed_date = Column(DateTime)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)
    
    # Relationships
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")

# ==========================================
# Roles & Permissions Table
# ==========================================
class Role(Base):
    __tablename__ = "roles"
    
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    permissions = Column(Text)  # JSON string of permissions
    can_view_phi = Column(Boolean, default=False)
    can_edit_phi = Column(Boolean, default=False)
    can_delete_phi = Column(Boolean, default=False)
    can_export_data = Column(Boolean, default=False)
    requires_justification = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.utcnow)

# ==========================================
# Sessions Table - JWT Session Management
# ==========================================
class Session(Base):
    __tablename__ = "sessions"
    
    session_id = Column(String(100), primary_key=True, index=True)
    user_id = Column(String(50), ForeignKey("users.user_id"), nullable=False)
    token = Column(Text, nullable=False)
    refresh_token = Column(Text)
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    last_activity = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    revoked = Column(Boolean, default=False)
    revoked_at = Column(DateTime)
    
    # Relationship
    user = relationship("User", back_populates="sessions")

# ==========================================
# Audit Logs - HIPAA Compliant Logging
# ==========================================
class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), ForeignKey("users.user_id"), nullable=False)
    patient_id = Column(Integer, index=True)
    action = Column(String(100), nullable=False)  # VIEW, CREATE, UPDATE, DELETE, EXPORT, LOGIN, LOGOUT
    resource_type = Column(String(50))  # PATIENT, RECORD, ALERT, etc.
    resource_id = Column(String(100))
    details = Column(Text)  # JSON details
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    status = Column(String(20))  # SUCCESS, FAILED, UNAUTHORIZED
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    session_id = Column(String(100))
    justification = Column(Text)  # Required for break-glass access
    data_accessed = Column(Text)  # List of fields accessed
    
    # Relationship
    user = relationship("User", back_populates="audit_logs")

# ==========================================
# Patient Consent Table
# ==========================================
class PatientConsent(Base):
    __tablename__ = "patient_consents"
    
    consent_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, nullable=False, index=True)
    consent_type = Column(String(50), nullable=False)  # DATA_SHARING, EMERGENCY_ACCESS, RESEARCH
    granted = Column(Boolean, default=False)
    granted_date = Column(DateTime)
    revoked_date = Column(DateTime)
    expires_at = Column(DateTime)
    granted_to_user_id = Column(String(50))
    granted_to_role = Column(String(50))
    scope = Column(Text)  # JSON - what data can be accessed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# ==========================================
# Break-Glass Access Logs
# ==========================================
class BreakGlassAccess(Base):
    __tablename__ = "break_glass_access"
    
    access_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), ForeignKey("users.user_id"), nullable=False)
    patient_id = Column(Integer, nullable=False, index=True)
    justification = Column(Text, nullable=False)
    emergency_type = Column(String(100))  # CARDIAC_ARREST, TRAUMA, STROKE, etc.
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(50))
    session_id = Column(String(100))
    reviewed = Column(Boolean, default=False)
    reviewed_by = Column(String(50))
    reviewed_date = Column(DateTime)
    review_notes = Column(Text)
    approved = Column(Boolean)

# ==========================================
# Encryption Keys Management
# ==========================================
class EncryptionKey(Base):
    __tablename__ = "encryption_keys"
    
    key_id = Column(Integer, primary_key=True, index=True)
    key_name = Column(String(100), unique=True, nullable=False)
    key_hash = Column(String(255), nullable=False)  # Store hash, not actual key
    algorithm = Column(String(50), default="AES-256-GCM")
    created_date = Column(DateTime, default=datetime.utcnow)
    rotated_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    purpose = Column(String(100))  # PHI_FIELD_ENCRYPTION, SESSION_ENCRYPTION, etc.

# ==========================================
# Security Events / Intrusion Detection
# ==========================================
class SecurityEvent(Base):
    __tablename__ = "security_events"
    
    event_id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), nullable=False)  # FAILED_LOGIN, BRUTE_FORCE, UNAUTHORIZED_ACCESS, etc.
    severity = Column(String(20))  # LOW, MEDIUM, HIGH, CRITICAL
    user_id = Column(String(50))
    ip_address = Column(String(50))
    description = Column(Text)
    details = Column(Text)  # JSON
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    resolved = Column(Boolean, default=False)
    resolved_by = Column(String(50))
    resolved_date = Column(DateTime)
    action_taken = Column(Text)

# ==========================================
# Data Version Control
# ==========================================
class DataVersion(Base):
    __tablename__ = "data_versions"
    
    version_id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String(50), nullable=False)
    record_id = Column(String(100), nullable=False)
    version_number = Column(Integer, nullable=False)
    data_snapshot = Column(Text, nullable=False)  # JSON snapshot
    changed_by = Column(String(50), ForeignKey("users.user_id"))
    changed_at = Column(DateTime, default=datetime.utcnow)
    change_type = Column(String(20))  # CREATE, UPDATE, DELETE
    change_reason = Column(Text)

# Create all tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
