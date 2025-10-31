# 🧪 COMPLETE TESTING GUIDE
## Healthcare Interoperability System with Authentication

---

## 📋 **SETUP STEPS**

### **Step 1: Install Backend Dependencies**

```bash
cd backend
pip install -r requirements.txt
```

**Note:** If you get pydantic-core error with Python 3.13, downgrade to Python 3.11 or 3.12:
```bash
brew install python@3.11
python3.11 -m pip install -r requirements.txt
```

---

### **Step 2: Initialize Security Database**

```bash
cd backend
python init_db.py
```

**Expected Output:**
```
✅ Security database created successfully at: security.db
✅ Tables created successfully
✅ Default users created:
   - admin (ADMIN)
   - doctor1 (DOCTOR)
   - nurse1 (NURSE)
   - emergency1 (EMERGENCY)
✅ Default roles created
✅ Security database initialized successfully!
```

---

### **Step 3: Start Backend Server**

```bash
cd backend
uvicorn main_new:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**✅ Backend is running!** Keep this terminal open.

---

### **Step 4: Test Backend API**

Open a **new terminal** and test:

```bash
curl http://localhost:8000/api/health
```

**Expected Output:**
```json
{
  "status": "healthy",
  "service": "Healthcare Interoperability System",
  "version": "2.0.0",
  "authentication": "enabled"
}
```

---

### **Step 5: Test Authentication**

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin@123"}'
```

**Expected Output:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**✅ Authentication is working!**

---

### **Step 6: Install Frontend Dependencies**

Open a **new terminal:**

```bash
cd frontend
npm install
```

**Expected Output:**
```
added 1348 packages in 15s
```

---

### **Step 7: Start Frontend**

```bash
cd frontend
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.1.x:3000

webpack compiled successfully
```

**✅ Frontend is running!** Browser should open automatically to `http://localhost:3000`

---

## 🧪 **TESTING SCENARIOS**

### **TEST 1: Login as Admin**

**Steps:**
1. Browser opens to `http://localhost:3000`
2. You'll see login page with gradient background
3. Enter credentials:
   - **Username:** `admin`
   - **Password:** `Admin@123`
4. Click **"Sign In"**

**Expected Result:**
✅ Redirects to Dashboard
✅ Shows welcome message: "Welcome back, admin!"
✅ Shows role badge: **ADMIN** (red badge)
✅ Shows quick action cards
✅ Shows system statistics
✅ Shows permissions: "View PHI", "Edit PHI", "Admin Access"

**Screenshot areas to check:**
- Header shows: "🏥 Healthcare Interoperability System"
- User info in top-right: "admin" with "ADMIN" badge
- Quick action cards visible
- System statistics showing (Total Users, Active Sessions, etc.)
- Security notice at bottom

---

### **TEST 2: Access Emergency Search**

**Steps:**
1. From Dashboard, click **"Emergency Search"** card (🚨 icon)
2. You're now on emergency patient search page
3. Fill in the form:
   - **First Name:** `John`
   - **Last Name:** `Smith`
4. Click **"Search Patient"**

**Expected Result:**
✅ Shows patient information
✅ Displays patient details: John Smith, DOB: 1965-03-15
✅ Shows hospital records from multiple hospitals
✅ Shows allergies: Penicillin (CRITICAL), Codeine (HIGH)
✅ Shows medications: Metformin, Lisinopril
✅ Shows chronic conditions: Type 2 Diabetes, Hypertension

**Backend Terminal Shows:**
```
INFO:     127.0.0.1:xxxxx - "GET /api/emergency-search?first_name=John&last_name=Smith HTTP/1.1" 200 OK
```

---

### **TEST 3: Logout and Login as Different User**

**Steps:**
1. Click **"Logout"** button (top-right)
2. Redirects to login page
3. Login with:
   - **Username:** `doctor1`
   - **Password:** `Doctor@123`

**Expected Result:**
✅ Redirects to Dashboard
✅ Shows: "Welcome back, doctor1!"
✅ Role badge shows: **DOCTOR** (teal badge)
✅ Shows permissions: "View PHI", "Edit PHI", "Export Data"
✅ Does NOT show system statistics (not admin)
✅ Shows Emergency Search and Patient List cards

---

### **TEST 4: Login as Nurse (Data Masking Test)**

**Steps:**
1. Logout
2. Login with:
   - **Username:** `nurse1`
   - **Password:** `Nurse@123`
3. Navigate to Emergency Search
4. Search for: **John** **Smith**

**Expected Result:**
✅ Login successful
✅ Role badge shows: **NURSE** (light teal badge)
✅ Patient data shows BUT sensitive info is MASKED:
   - SSN: `***-**-6789` (only last 4 digits)
   - Phone: `***-***-0101` (only last 4 digits)
✅ Medical history visible but export disabled

---

### **TEST 5: View API Documentation**

**Steps:**
1. Open browser to: `http://localhost:8000/docs`

**Expected Result:**
✅ Shows Swagger UI
✅ Lists all API endpoints:
   - /api/health
   - /api/auth/login
   - /api/auth/logout
   - /api/emergency-search
   - /api/audit-logs
   - etc.
✅ Each endpoint shows parameters and responses
✅ Can test endpoints directly from Swagger

---

### **TEST 6: Check Audit Logs**

**Steps:**
1. Login as admin
2. Click **"Audit Logs"** card from dashboard
   (This route needs to be implemented, but backend works)

**Alternative - Check via API:**
```bash
# First, get access token from login
ACCESS_TOKEN="your_token_here"

curl http://localhost:8000/api/audit-logs \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Expected Result:**
✅ Shows all access logs
✅ Each log contains:
   - User who accessed
   - Patient accessed
   - Action performed
   - Timestamp
   - IP address
   - Purpose

**Example Log Entry:**
```json
{
  "log_id": 1,
  "user_id": "admin",
  "username": "admin",
  "patient_id": 1000,
  "action": "VIEW",
  "record_type": "patient_record",
  "status": "SUCCESS",
  "ip_address": "127.0.0.1",
  "access_date": "2024-10-31T12:34:56",
  "purpose_of_access": "Emergency patient lookup"
}
```

---

### **TEST 7: Protected Route Test**

**Steps:**
1. Logout (clear session)
2. Manually navigate to: `http://localhost:3000/dashboard`

**Expected Result:**
✅ Immediately redirects to `/login`
✅ Cannot access protected pages without authentication
✅ After login, redirects back to originally requested page

---

### **TEST 8: Token Refresh Test**

**Steps:**
1. Login normally
2. Keep browser open for 25-30 minutes
3. Try to navigate or perform action

**Expected Result:**
✅ Token automatically refreshes in background
✅ No interruption to user
✅ Session continues smoothly
✅ New tokens stored in localStorage

---

### **TEST 9: Invalid Login Test**

**Steps:**
1. Try to login with:
   - **Username:** `admin`
   - **Password:** `wrongpassword`

**Expected Result:**
✅ Shows error message: "Invalid username or password"
✅ Red error box appears
✅ Does not redirect
✅ Can try again

---

### **TEST 10: Session Management Test**

**Steps:**
1. Login as admin
2. Open browser DevTools (F12)
3. Go to Application tab → Local Storage
4. Check stored items

**Expected Result:**
✅ See `access_token` stored
✅ See `refresh_token` stored
✅ See `user` object with user info
✅ After logout, all items cleared

---

## 🔍 **VERIFICATION CHECKLIST**

### **Backend Verification:**
- [ ] Backend starts on port 8000
- [ ] Health endpoint responds
- [ ] Login endpoint returns JWT tokens
- [ ] Swagger docs accessible at /docs
- [ ] Database file `security.db` created in backend/

### **Frontend Verification:**
- [ ] Frontend starts on port 3000
- [ ] Login page loads with styling
- [ ] Can login with test accounts
- [ ] Dashboard shows after login
- [ ] Logout works and redirects to login
- [ ] Protected routes redirect to login when not authenticated
- [ ] Role-based UI works (different views for different roles)

### **Integration Verification:**
- [ ] Frontend can call backend APIs
- [ ] JWT tokens passed in Authorization header
- [ ] Patient search returns data
- [ ] Audit logs are created automatically
- [ ] Data masking works for nurses
- [ ] Emergency access requires justification

### **Security Verification:**
- [ ] Cannot access APIs without token
- [ ] Invalid credentials rejected
- [ ] Account locks after 5 failed attempts
- [ ] Sessions expire after 30 minutes
- [ ] All PHI access is logged
- [ ] SSN appears encrypted in database

---

## 📸 **WHAT YOU SHOULD SEE**

### **Login Page:**
```
┌─────────────────────────────────────┐
│    🏥 Healthcare System             │
│    Emergency Medical Data Exchange  │
├─────────────────────────────────────┤
│           Sign In                   │
│                                     │
│  Username: [___________________]    │
│  Password: [___________________]    │
│                                     │
│       [    Sign In    ]             │
│                                     │
│  Default Test Accounts:             │
│  • Admin: admin / Admin@123         │
│  • Doctor: doctor1 / Doctor@123     │
│  • Nurse: nurse1 / Nurse@123        │
│  • Emergency: emergency1/Emergency@123│
└─────────────────────────────────────┘
```

### **Dashboard (Admin):**
```
┌──────────────────────────────────────────────────────────┐
│ 🏥 Healthcare Interoperability System        admin [ADMIN] [Logout] │
│ HIPAA-Compliant Emergency Medical Data Exchange          │
├──────────────────────────────────────────────────────────┤
│ Welcome back, admin!                                     │
│ You are logged in as ADMIN                               │
│                                                          │
│ Quick Actions:                                           │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│ │🚨Emergency│ │👥Patients│ │📋Audit   │ │🔒Security │  │
│ │ Search   │ │ List     │ │ Logs     │ │ Events   │  │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│                                                          │
│ System Statistics:                                       │
│ Total Users: 4  Active Sessions: 1  Audit Logs: 25      │
│                                                          │
│ Your Permissions:                                        │
│ ✅ View PHI  ✅ Edit PHI  ✅ Export Data  ✅ Admin Access│
└──────────────────────────────────────────────────────────┘
```

---

## 🐛 **TROUBLESHOOTING**

### **Problem: Backend won't start**
**Solution:**
```bash
# Check Python version
python3 --version  # Should be 3.8-3.12

# Try with specific Python version
python3.11 -m pip install -r requirements.txt
python3.11 init_db.py
python3.11 -m uvicorn main_new:app --reload
```

### **Problem: Frontend won't start**
**Solution:**
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm start
```

### **Problem: Login fails**
**Solution:**
- Verify backend is running on port 8000
- Check backend terminal for errors
- Try curl command to test backend directly
- Check browser console (F12) for errors

### **Problem: "Cannot connect to API"**
**Solution:**
- Check `frontend/.env` has `REACT_APP_API_URL=http://localhost:8000`
- Ensure backend is running
- Check for CORS errors in browser console

### **Problem: Protected routes don't work**
**Solution:**
- Clear browser localStorage
- Logout and login again
- Check browser console for routing errors

---

## ✅ **SUCCESS CRITERIA**

Your system is working correctly if:

1. ✅ Backend starts and responds to health check
2. ✅ Can login with all 4 test accounts
3. ✅ Dashboard loads after login
4. ✅ Emergency search returns patient data
5. ✅ Logout works and clears session
6. ✅ Cannot access dashboard without login
7. ✅ Different roles see different UI
8. ✅ Audit logs are created automatically
9. ✅ Swagger docs accessible
10. ✅ No console errors in browser

---

## 🎉 **YOU'RE DONE!**

If all tests pass, congratulations! You have a fully functional HIPAA-compliant healthcare interoperability system with:

- ✅ JWT Authentication
- ✅ Role-Based Access Control
- ✅ Audit Logging
- ✅ Session Management
- ✅ Protected Routes
- ✅ Data Masking
- ✅ Emergency Access
- ✅ Responsive Design

**Next steps:**
- Create more patient records
- Add more user accounts
- Customize UI styling
- Add additional features
- Deploy to production (with proper security!)

---

**Need help?** Check the documentation in:
- `backend/SECURITY_README.md`
- `backend/QUICKSTART.md`
- `frontend/README.md`
- API docs at http://localhost:8000/docs
