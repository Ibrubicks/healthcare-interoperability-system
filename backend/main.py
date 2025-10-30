
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cx_Oracle
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection setup
def get_db_connection():
    try:
        dsn_tns = cx_Oracle.makedsn('localhost', 1521, service_name='orcl')
        connection = cx_Oracle.connect(user='system', password='your_password_here', dsn=dsn_tns)
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# ==========================================
# ROUTE 1: Health Check
# ==========================================
@app.get("/api/health")
def health_check():
    return {'status': 'Backend is running!'}

# ==========================================
# ROUTE 2: Emergency Patient Search
# ==========================================
@app.get("/api/emergency-search")
def emergency_search(first_name: str, last_name: str, dob: str):
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = conn.cursor()
        
        query = """
        SELECT 
            p.Patient_ID,
            p.First_Name,
            p.Last_Name,
            p.Date_of_Birth,
            p.Gender,
            p.Phone,
            p.Emergency_Contact,
            COUNT(DISTINCT pr.Hospital_ID) AS num_hospitals
        FROM Patients p
        LEFT JOIN Patient_Records pr ON p.Patient_ID = pr.Patient_ID
        WHERE UPPER(p.First_Name) LIKE UPPER(:first_name || '%')
          AND UPPER(p.Last_Name) LIKE UPPER(:last_name || '%')
        GROUP BY p.Patient_ID, p.First_Name, p.Last_Name, p.Date_of_Birth, p.Gender, p.Phone, p.Emergency_Contact
        """
        
        cursor.execute(query, {'first_name': first_name, 'last_name': last_name})
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        patient_id = result[0]
        patient = {
            'patient_id': patient_id,
            'first_name': result[1],
            'last_name': result[2],
            'date_of_birth': str(result[3]),
            'gender': result[4],
            'phone': result[5],
            'emergency_contact': result[6],
            'num_hospitals': result[7]
        }
        
        # Get all hospital records
        hospital_query = """
        SELECT 
            hs.Hospital_Name,
            pr.MRN,
            pr.Last_Visit_Date,
            pr.Current_Medications,
            pr.Allergies,
            pr.Chronic_Conditions
        FROM Patient_Records pr
        JOIN Hospital_Systems hs ON pr.Hospital_ID = hs.Hospital_ID
        WHERE pr.Patient_ID = :patient_id
        ORDER BY hs.Hospital_Name
        """
        
        cursor.execute(hospital_query, {'patient_id': patient_id})
        hospital_records = []
        for row in cursor.fetchall():
            hospital_records.append({
                'hospital': row[0],
                'mrn': row[1],
                'last_visit': str(row[2]),
                'medications': row[3],
                'allergies': row[4],
                'chronic_conditions': row[5]
            })
        
        # Get critical alerts
        alerts_query = """
        SELECT 
            Alert_ID,
            Alert_Type,
            Description,
            Severity,
            Alert_Details,
            Acknowledged
        FROM Critical_Alerts
        WHERE Patient_ID = :patient_id
        ORDER BY 
            CASE Severity
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
            END
        """
        
        cursor.execute(alerts_query, {'patient_id': patient_id})
        alerts = []
        for row in cursor.fetchall():
            alerts.append({
                'alert_id': row[0],
                'type': row[1],
                'description': row[2],
                'severity': row[3],
                'details': row[4],
                'acknowledged': row[5]
            })
        
        cursor.close()
        conn.close()
        
        return {
            'patient': patient,
            'hospital_records': hospital_records,
            'alerts': alerts
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# ROUTE 3: Get All Patients
# ==========================================
@app.get("/api/patients")
def get_all_patients():
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = conn.cursor()
        
        query = """
        SELECT 
            Patient_ID,
            First_Name,
            Last_Name,
            Date_of_Birth,
            Gender,
            Phone
        FROM Patients
        ORDER BY Last_Name, First_Name
        """
        
        cursor.execute(query)
        patients = []
        for row in cursor.fetchall():
            patients.append({
                'patient_id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'date_of_birth': str(row[3]),
                'gender': row[4],
                'phone': row[5]
            })
        
        cursor.close()
        conn.close()
        
        return {'patients': patients}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# ROUTE 4: Get Matching Scores
# ==========================================
@app.get("/api/matching-scores")
def get_matching_scores(patient_id: int):
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = conn.cursor()
        
        query = """
        SELECT 
            ms.Match_ID,
            p1.First_Name || ' ' || p1.Last_Name AS Patient_1,
            p2.First_Name || ' ' || p2.Last_Name AS Patient_2,
            hs1.Hospital_Name AS Hospital_1,
            hs2.Hospital_Name AS Hospital_2,
            ms.Overall_Confidence_Score,
            ms.First_Name_Score,
            ms.Last_Name_Score,
            ms.DOB_Score,
            ms.SSN_Score
        FROM Matching_Scores ms
        JOIN Patients p1 ON ms.Patient_ID_1 = p1.Patient_ID
        JOIN Patients p2 ON ms.Patient_ID_2 = p2.Patient_ID
        JOIN Hospital_Systems hs1 ON ms.Hospital_ID_1 = hs1.Hospital_ID
        JOIN Hospital_Systems hs2 ON ms.Hospital_ID_2 = hs2.Hospital_ID
        WHERE ms.Patient_ID_1 = :patient_id OR ms.Patient_ID_2 = :patient_id
        ORDER BY ms.Overall_Confidence_Score DESC
        """
        
        cursor.execute(query, {'patient_id': patient_id})
        matches = []
        for row in cursor.fetchall():
            matches.append({
                'match_id': row[0],
                'patient_1': row[1],
                'patient_2': row[2],
                'hospital_1': row[3],
                'hospital_2': row[4],
                'confidence_score': float(row[5]),
                'first_name_score': float(row[6]),
                'last_name_score': float(row[7]),
                'dob_score': float(row[8]),
                'ssn_score': float(row[9])
            })
        
        cursor.close()
        conn.close()
        
        return {'matches': matches}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# ROUTE 5: Get Drug Interactions
# ==========================================
@app.get("/api/drug-interactions")
def get_drug_interactions():
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = conn.cursor()
        
        query = """
        SELECT 
            Drug_Name,
            Allergen_Name,
            Interaction_Severity,
            Interaction_Description
        FROM Drug_Allergy_Matrix
        WHERE Interaction_Severity IN ('CONTRAINDICATED', 'SIGNIFICANT')
        ORDER BY Interaction_Severity DESC, Drug_Name
        """
        
        cursor.execute(query)
        interactions = []
        for row in cursor.fetchall():
            interactions.append({
                'drug': row[0],
                'allergen': row[1],
                'severity': row[2],
                'description': row[3]
            })
        
        cursor.close()
        conn.close()
        
        return {'interactions': interactions}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# ROUTE 6: Log Emergency Access (HIPAA Audit)
# ==========================================
@app.post("/api/log-access")
def log_access(user_id: str, patient_id: int, purpose: str, ip_address: str):
    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        cursor = conn.cursor()
        
        query = """
        INSERT INTO Access_Logs 
        (Log_ID, User_ID, Patient_ID, Action, Record_Type, Status, IP_Address, Access_Date, Purpose_of_Access)
        VALUES 
        (seq_log_id.NEXTVAL, :user_id, :patient_id, 'VIEW', 'PATIENT_FULL_RECORD', 'SUCCESS', :ip_address, SYSDATE, :purpose)
        """
        
        cursor.execute(query, {
            'user_id': user_id,
            'patient_id': patient_id,
            'ip_address': ip_address,
            'purpose': purpose
        })
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {'status': 'Access logged successfully'}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run: uvicorn main.py --reload

