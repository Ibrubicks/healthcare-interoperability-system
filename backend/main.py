from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import datetime

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    try:
        conn = sqlite3.connect('healthcare.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.get("/api/health")
def health_check():
    return {"status": "Backend is running!"}

@app.get("/api/emergency-search")
def emergency_search(first_name: str, last_name: str, dob: str):
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = conn.cursor()
        
        # Get patient info
        cursor.execute('''
            SELECT * FROM patients 
            WHERE LOWER(first_name) = LOWER(?) 
            AND LOWER(last_name) = LOWER(?) 
            AND date_of_birth = ?
        ''', (first_name, last_name, dob))
        
        patient = cursor.execute('''
            SELECT * FROM patients 
            WHERE LOWER(first_name) = LOWER(?) 
            AND LOWER(last_name) = LOWER(?)
        ''', (first_name, last_name)).fetchone()
        
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        patient_id = patient['patient_id']
        
        # Get hospital records
        cursor.execute('''
            SELECT * FROM hospital_records WHERE patient_id = ?
        ''', (patient_id,))
        
        hospital_records = []
        for row in cursor.fetchall():
            hospital_records.append({
                "hospital": row['hospital_name'],
                "mrn": row['mrn'],
                "last_visit": row['last_visit'],
                "medications": row['medications'],
                "allergies": row['allergies'],
                "chronic_conditions": row['chronic_conditions']
            })
        
        # Get alerts
        cursor.execute('''
            SELECT * FROM critical_alerts WHERE patient_id = ?
        ''', (patient_id,))
        
        alerts = []
        for row in cursor.fetchall():
            alerts.append({
                "alert_id": row['alert_id'],
                "type": row['alert_type'],
                "description": row['description'],
                "severity": row['severity'],
                "acknowledged": row['acknowledged']
            })
        
        conn.close()
        
        return {
            "patient": {
                "patient_id": patient['patient_id'],
                "first_name": patient['first_name'],
                "last_name": patient['last_name'],
                "date_of_birth": patient['date_of_birth'],
                "gender": patient['gender'],
                "phone": patient['phone'],
                "emergency_contact": patient['emergency_contact'],
                "num_hospitals": len(hospital_records)
            },
            "hospital_records": hospital_records,
            "alerts": alerts
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/log-access")
def log_access(user_id: str, patient_id: int, purpose: str, ip_address: str):
    return {"status": "Access logged"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
