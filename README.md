# 🏥 Healthcare Interoperability System

**Emergency medical data exchange system with HIPAA-compliant authentication, patient matching, and FHIR compliance**

## 🎯 Overview

A comprehensive healthcare system that enables secure patient data exchange across multiple hospital systems (Epic, Cerner, NextGen). Features include emergency patient lookup, probabilistic patient matching, drug-allergy checking, and complete HIPAA audit trails.

## ✨ Key Features

### 🔐 Security & Compliance
- **JWT Authentication** - Secure token-based login
- **Role-Based Access Control (RBAC)** - 5 user roles with distinct permissions
- **HIPAA Audit Logging** - Complete access trail for all PHI
- **Field-Level Encryption** - AES-256 encryption for sensitive data
- **Session Management** - 30-minute timeout with auto-refresh
- **Break-Glass Access** - Emergency override with mandatory justification

### 🏥 Healthcare Features
- **Emergency Patient Search** - Fast cross-hospital patient lookup
- **Probabilistic Matching** - AI-powered patient deduplication (75% confidence threshold)
- **Drug-Allergy Checking** - Real-time contraindication alerts
- **FHIR R4 Compliance** - Standardized healthcare data exchange
- **Multi-Hospital Support** - Unified records from multiple EHR systems

### 👥 User Roles
- **ADMIN** - Full system access + user management
- **DOCTOR** - Complete PHI access, can edit records
- **NURSE** - Limited PHI with data masking
- **EMERGENCY** - Break-glass access with justification
- **PATIENT** - View own records only

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- Oracle Database (for patient data)
- SQLite (for security data)

### 1. Clone Repository
```bash
git clone https://github.com/Ibrubicks/healthcare-interoperability-system.git
cd healthcare-interoperability-system
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python init_db.py
uvicorn main_new:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 4. Login
- **URL:** http://localhost:3000
- **Username:** admin
- **Password:** Admin@123

## 📁 Project Structure

```
healthcare-interoperability-system/
├── backend/                    # Python FastAPI backend
│   ├── main_new.py            # Main API with authentication
│   ├── auth.py                # Authentication logic
│   ├── security.py            # Encryption & RBAC
│   ├── database.py            # SQLite security DB
│   ├── models.py              # Pydantic models
│   ├── init_db.py             # Database initialization
│   ├── requirements.txt       # Python dependencies
│   ├── SECURITY_README.md     # Security documentation
│   └── QUICKSTART.md          # Backend setup guide
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── contexts/          # Auth context
│   │   ├── services/          # API services
│   │   └── styles/            # CSS styles
│   ├── package.json           # Node dependencies
│   └── README.md              # Frontend guide
├── sql/                        # Oracle database scripts
│   ├── 02_tables.sql          # Patient tables
│   ├── 04_insert_data.sql     # Sample data
│   └── ...                    # Other SQL scripts
└── README.md                   # This file
```

## 🔧 Technology Stack

**Backend:**
- FastAPI (Python web framework)
- SQLite (security/auth database)
- Oracle (patient data database)
- JWT (authentication tokens)
- bcrypt (password hashing)
- Cryptography (field-level encryption)

**Frontend:**
- React 19
- React Router (routing)
- Axios (API calls)
- Context API (state management)

**Database:**
- SQLite - Authentication, sessions, audit logs
- Oracle - Patient records, hospital data

## 🎓 Default Test Accounts

| Username | Password | Role | Purpose |
|----------|----------|------|---------|
| admin | Admin@123 | ADMIN | System administration |
| doctor1 | Doctor@123 | DOCTOR | Full patient access |
| nurse1 | Nurse@123 | NURSE | Limited access (masked PHI) |
| emergency1 | Emergency@123 | EMERGENCY | Break-glass access |

⚠️ **Change these passwords immediately after deployment!**

## 📊 API Endpoints

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/register` - Register user
- `POST /api/auth/change-password` - Change password

### Patient Data
- `GET /api/emergency-search` - Search patients
- `GET /api/patients` - List all patients
- `GET /api/matching-scores` - Get patient matches
- `GET /api/drug-interactions` - Drug-allergy matrix

### Security & Audit
- `GET /api/audit-logs` - View audit logs
- `GET /api/audit-logs/patient/{id}` - Patient access history
- `POST /api/emergency-access` - Break-glass access
- `GET /api/sessions` - Active sessions
- `GET /api/security-events` - Security events (Admin)

## 🔒 Security Features

### Authentication
- JWT tokens with 30-minute expiry
- Refresh tokens valid for 7 days
- Automatic token refresh
- Account lockout after 5 failed attempts

### Authorization
- Role-based permissions
- Data masking for sensitive fields
- Break-glass emergency access
- Session timeout after inactivity

### Audit & Compliance
- Every PHI access logged
- Who, What, When, Where, Why tracking
- 6-year log retention (HIPAA requirement)
- Tamper-proof audit trail

### Data Protection
- SSN encryption at rest
- Password hashing (bcrypt)
- Secure token storage
- HTTPS/TLS ready

## 📖 Documentation

- **Backend Security:** `backend/SECURITY_README.md`
- **Backend Setup:** `backend/QUICKSTART.md`
- **Frontend Guide:** `frontend/README.md`
- **API Docs:** http://localhost:8000/docs (Swagger)

## 🧪 Testing

### Test Backend
```bash
cd backend
python init_db.py
# Initializes DB with test data
```

### Test Authentication
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin@123"}'
```

### Test Frontend
```bash
cd frontend
npm start
# Login at http://localhost:3000
```

## 🐛 Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (needs 3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Initialize DB: `python init_db.py`

**Frontend won't start:**
- Check Node version: `node --version` (needs 14+)
- Install dependencies: `npm install`
- Check `.env` file exists

**Login fails:**
- Verify backend is running on port 8000
- Check credentials: admin / Admin@123
- Check browser console for errors

**API calls fail:**
- Verify `REACT_APP_API_URL` in frontend/.env
- Check CORS settings in backend
- Check network tab in browser devtools

## 🚀 Deployment

### Production Checklist
- [ ] Change all default passwords
- [ ] Set strong `SECRET_KEY` in backend
- [ ] Enable HTTPS/TLS
- [ ] Configure production database
- [ ] Set up log rotation
- [ ] Configure backup system
- [ ] Enable monitoring/alerts
- [ ] Conduct security audit
- [ ] Train staff on system usage

## 📝 License

This project is for educational purposes. Ensure HIPAA compliance before production use.

## 🤝 Contributing

This is a portfolio/demonstration project. For production use, conduct thorough security audits and compliance reviews.

## ⚠️ Important Notes

- **This system handles PHI** - Unauthorized access violates HIPAA
- **Change default passwords** - Never use in production as-is
- **HTTPS required** - Enable TLS/SSL for production
- **Regular audits** - Review access logs and security events
- **Backup critical** - Implement disaster recovery plan

## 📞 Support

For issues or questions:
1. Check documentation in respective folders
2. Review API docs at http://localhost:8000/docs
3. Check browser console for frontend errors
4. Review backend logs for API errors

---

**Built with ❤️ for secure healthcare data exchange**
