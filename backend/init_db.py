"""
Initialize Security Database with Default Data
Creates admin user and sets up initial roles
"""
import sys
import uuid
from datetime import datetime

# Import our modules
import database
import security
from database import User, Role

def init_security_db():
    """Initialize security database with default admin user and roles"""
    
    # Create tables
    print("Creating database tables...")
    database.init_db()
    print("✓ Tables created successfully")
    
    # Create database session
    db = next(database.get_db())
    
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("⚠ Admin user already exists")
        else:
            # Create default admin user
            print("\nCreating default admin user...")
            admin_user = User(
                user_id=str(uuid.uuid4()),
                username="admin",
                email="admin@healthcare.com",
                hashed_password=security.hash_password("Admin@123"),
                full_name="System Administrator",
                role="ADMIN",
                department="IT",
                is_active=True,
                is_verified=True,
                password_changed_date=datetime.utcnow()
            )
            db.add(admin_user)
            print("✓ Admin user created")
            print("  Username: admin")
            print("  Password: Admin@123")
            print("  ⚠️  IMPORTANT: Change this password immediately after first login!")
        
        # Create default roles
        print("\nCreating default roles...")
        roles_data = [
            {
                "role_name": "ADMIN",
                "description": "Full system access with user management",
                "can_view_phi": True,
                "can_edit_phi": True,
                "can_delete_phi": True,
                "can_export_data": True,
                "requires_justification": False
            },
            {
                "role_name": "DOCTOR",
                "description": "Medical professional with full patient access",
                "can_view_phi": True,
                "can_edit_phi": True,
                "can_delete_phi": False,
                "can_export_data": True,
                "requires_justification": False
            },
            {
                "role_name": "NURSE",
                "description": "Nursing staff with limited patient access",
                "can_view_phi": True,
                "can_edit_phi": True,
                "can_delete_phi": False,
                "can_export_data": False,
                "requires_justification": True
            },
            {
                "role_name": "EMERGENCY",
                "description": "Emergency responders with break-glass access",
                "can_view_phi": True,
                "can_edit_phi": True,
                "can_delete_phi": False,
                "can_export_data": True,
                "requires_justification": True
            },
            {
                "role_name": "PATIENT",
                "description": "Patient access to own records only",
                "can_view_phi": True,
                "can_edit_phi": False,
                "can_delete_phi": False,
                "can_export_data": True,
                "requires_justification": False
            }
        ]
        
        for role_data in roles_data:
            existing_role = db.query(Role).filter(Role.role_name == role_data["role_name"]).first()
            if not existing_role:
                role = Role(**role_data)
                db.add(role)
                print(f"  ✓ Created role: {role_data['role_name']}")
        
        # Create additional test users
        print("\nCreating test users...")
        test_users = [
            {
                "username": "doctor1",
                "email": "doctor1@healthcare.com",
                "password": "Doctor@123",
                "full_name": "Dr. Sarah Johnson",
                "role": "DOCTOR",
                "department": "Emergency Medicine"
            },
            {
                "username": "nurse1",
                "email": "nurse1@healthcare.com",
                "password": "Nurse@123",
                "full_name": "Emily Davis",
                "role": "NURSE",
                "department": "Emergency Room"
            },
            {
                "username": "emergency1",
                "email": "emergency1@healthcare.com",
                "password": "Emergency@123",
                "full_name": "John EMT",
                "role": "EMERGENCY",
                "department": "EMS"
            }
        ]
        
        for user_data in test_users:
            existing = db.query(User).filter(User.username == user_data["username"]).first()
            if not existing:
                user = User(
                    user_id=str(uuid.uuid4()),
                    username=user_data["username"],
                    email=user_data["email"],
                    hashed_password=security.hash_password(user_data["password"]),
                    full_name=user_data["full_name"],
                    role=user_data["role"],
                    department=user_data["department"],
                    is_active=True,
                    password_changed_date=datetime.utcnow()
                )
                db.add(user)
                print(f"  ✓ Created user: {user_data['username']} ({user_data['role']})")
        
        # Commit all changes
        db.commit()
        print("\n✅ Database initialization complete!")
        print("\n" + "="*60)
        print("DEFAULT LOGIN CREDENTIALS:")
        print("="*60)
        print("\n1. Admin:")
        print("   Username: admin")
        print("   Password: Admin@123")
        print("\n2. Doctor:")
        print("   Username: doctor1")
        print("   Password: Doctor@123")
        print("\n3. Nurse:")
        print("   Username: nurse1")
        print("   Password: Nurse@123")
        print("\n4. Emergency:")
        print("   Username: emergency1")
        print("   Password: Emergency@123")
        print("\n" + "="*60)
        print("⚠️  SECURITY WARNING: Change all default passwords immediately!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("="*60)
    print("HIPAA-Compliant Healthcare System - Database Initialization")
    print("="*60)
    print()
    init_security_db()
