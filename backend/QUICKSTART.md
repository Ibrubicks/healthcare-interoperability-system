# HIPAA-Compliant Healthcare System - Quick Start Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Initialize Security Database
```bash
python init_db.py
```

You'll see output like:
```
✓ Tables created successfully
✓ Admin user created
  Username: admin
  Password: Admin@123
```

### Step 3: Start the Backend Server
```bash
# Option 1: Using the new HIPAA-compliant version
uvicorn main_new:app --reload --port 8000

# Option 2: Rename main_new.py to main.py (after testing)
# mv main.py main_old.py
# mv main_new.py main.py
# uvicorn main:app --reload --port 8000
```

### Step 4: Test the API

Open your browser to: **http://localhost:8000/docs**

You'll see the interactive Swagger UI with all endpoints.

### Step 5: Login and Get Token

**Using curl:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin@123"}'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

Copy the `access_token` value!

### Step 6: Access Protected Endpoint

```bash
curl -X GET "http://localhost:8000/api/emergency-search?first_name=John&last_name=Doe" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## 📋 Default Test Users

| Username | Password | Role | Description |
|----------|----------|------|-------------|
| admin | Admin@123 | ADMIN | Full access + user management |
| doctor1 | Doctor@123 | DOCTOR | Full PHI access, can edit |
| nurse1 | Nurse@123 | NURSE | Limited PHI access, sees masked data |
| emergency1 | Emergency@123 | EMERGENCY | Break-glass emergency access |

⚠️ **CHANGE ALL PASSWORDS AFTER FIRST LOGIN!**

## 🧪 Testing the Features

### 1. Test Authentication
```bash
# Login as doctor
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "doctor1", "password": "Doctor@123"}'
```

### 2. Test Patient Search (Requires Auth)
```bash
# Will fail without token
curl -X GET "http://localhost:8000/api/emergency-search?first_name=John&last_name=Doe"

# Will succeed with token
curl -X GET "http://localhost:8000/api/emergency-search?first_name=John&last_name=Doe" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Test Audit Logging
```bash
# View your own audit logs
curl -X GET http://localhost:8000/api/audit-logs \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Test Break-Glass Access
```bash
# Login as emergency user first
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "emergency1", "password": "Emergency@123"}'

# Then use break-glass access
curl -X POST http://localhost:8000/api/emergency-access \
  -H "Authorization: Bearer EMERGENCY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "justification": "Patient arrived unconscious, no ID, immediate treatment required",
    "emergency_type": "CARDIAC_ARREST"
  }'
```

### 5. Test Data Masking
```bash
# Login as nurse (sees masked data)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "nurse1", "password": "Nurse@123"}'

# Search patient - SSN and phone will be masked
curl -X GET "http://localhost:8000/api/emergency-search?first_name=John&last_name=Doe" \
  -H "Authorization: Bearer NURSE_TOKEN"
```

## 🔐 Security Features in Action

### Automatic Audit Logging
Every PHI access is automatically logged:
- ✅ Who accessed the data
- ✅ What data was accessed
- ✅ When it was accessed
- ✅ From where (IP address)
- ✅ Success or failure

### Session Management
- ✅ 30-minute access tokens
- ✅ 7-day refresh tokens
- ✅ Automatic session timeout after 30 min inactivity
- ✅ Multiple device support

### Account Security
- ✅ Account locked after 5 failed attempts
- ✅ 30-minute lockout period
- ✅ Password strength requirements
- ✅ Password change tracking

### Role-Based Access
- ✅ ADMIN: Full access
- ✅ DOCTOR: Full PHI, no user management
- ✅ NURSE: Limited PHI, sees masked sensitive data
- ✅ EMERGENCY: Break-glass access with justification
- ✅ PATIENT: Own records only

## 📊 View System Statistics (Admin Only)

```bash
curl -X GET http://localhost:8000/api/stats \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

Response:
```json
{
  "total_users": 4,
  "active_sessions": 2,
  "total_audit_logs": 15,
  "failed_login_attempts": 0,
  "security_events_last_24h": 5,
  "break_glass_accesses_last_24h": 0
}
```

## 🔄 Password Change Flow

```bash
# Change your password
curl -X POST http://localhost:8000/api/auth/change-password \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "Admin@123",
    "new_password": "NewSecure@Pass123"
  }'
```

All sessions are revoked after password change for security.

## 🚪 Logout

```bash
curl -X POST http://localhost:8000/api/auth/logout \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📱 Using with Postman

1. **Import API**: Go to http://localhost:8000/openapi.json
2. **Set Authorization**: 
   - Type: Bearer Token
   - Token: YOUR_ACCESS_TOKEN
3. **Make Requests**: All protected endpoints now accessible

## 🐛 Troubleshooting

### Error: "Could not validate credentials"
- Token expired - use refresh token endpoint
- Token invalid - login again
- Check Authorization header format: `Bearer YOUR_TOKEN`

### Error: "Account is temporarily locked"
- Wait 30 minutes
- Or contact admin to manually unlock

### Error: "Access denied"
- Your role doesn't have permission
- Contact admin for role change

### Error: "Database connection failed"
- Check Oracle database is running
- Verify credentials in .env file

## 📈 Next Steps

### For Production:
1. ✅ Change all default passwords
2. ✅ Set up proper SECRET_KEY in .env
3. ✅ Enable HTTPS (TLS/SSL)
4. ✅ Set up database backups
5. ✅ Configure log rotation
6. ✅ Set up monitoring alerts
7. ✅ Conduct security audit
8. ✅ Train staff on security procedures

### For Development:
1. Test all endpoints
2. Verify audit logging
3. Test role-based access
4. Test emergency access
5. Review security events
6. Test session timeout
7. Test account lockout

## 🆘 Support

- Documentation: `/backend/SECURITY_README.md`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

## ✅ Verification Checklist

- [ ] Backend starts without errors
- [ ] Can login with admin credentials
- [ ] Token received successfully
- [ ] Can access protected endpoints with token
- [ ] Cannot access without token (401 error)
- [ ] Audit logs are being created
- [ ] Different roles have different access
- [ ] Data masking works for NURSE role
- [ ] Password change works
- [ ] Logout revokes session

---

**🎉 You're all set! Your HIPAA-compliant healthcare system is ready.**
