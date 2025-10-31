import sqlite3
from datetime import datetime

# Create database
conn = sqlite3.connect('healthcare.db')
cursor = conn.cursor()

# Create patients table
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    date_of_birth TEXT,
    gender TEXT,
    phone TEXT,
    emergency_contact TEXT
)
''')

# Create hospital_records table
cursor.execute('''
CREATE TABLE IF NOT EXISTS hospital_records (
    record_id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    hospital_name TEXT,
    mrn TEXT,
    last_visit TEXT,
    medications TEXT,
    allergies TEXT,
    chronic_conditions TEXT
)
''')

# Create alerts table
cursor.execute('''
CREATE TABLE IF NOT EXISTS critical_alerts (
    alert_id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    alert_type TEXT,
    description TEXT,
    severity TEXT,
    acknowledged TEXT
)
''')

# Insert sample patient data
cursor.execute('''
INSERT INTO patients VALUES 
(1, 'John', 'Smith', '1965-03-15', 'M', '212-555-0101', 'Sarah Smith - 212-555-0102')
''')

cursor.execute('''
INSERT INTO patients VALUES 
(2, 'Emily', 'Johnson', '1978-07-22', 'F', '415-555-0203', 'Michael Johnson - 415-555-0204')
''')

# Insert hospital records
cursor.execute('''
INSERT INTO hospital_records VALUES 
(1, 1, 'City Medical Center', 'CMC-2024-98765', '2024-10-15', 
'Metformin 1000mg, Lisinopril 10mg', 
'Penicillin (severe)', 
'Type 2 Diabetes, Hypertension')
''')

cursor.execute('''
INSERT INTO hospital_records VALUES 
(2, 1, 'General Hospital', 'GH-2024-12345', '2024-09-20', 
'Aspirin 81mg', 
'Penicillin (severe)', 
'Coronary Artery Disease')
''')

cursor.execute('''
INSERT INTO hospital_records VALUES 
(3, 2, 'Regional Health', 'RH-2024-56789', '2024-10-28', 
'Albuterol Inhaler', 
'Shellfish', 
'Asthma')
''')

# Insert alerts
cursor.execute('''
INSERT INTO critical_alerts VALUES 
(1, 1, 'ALLERGY', 'CRITICAL - Penicillin allergy detected', 'CRITICAL', 'N')
''')

cursor.execute('''
INSERT INTO critical_alerts VALUES 
(2, 1, 'CONDITION', 'Patient has history of heart disease', 'HIGH', 'N')
''')

cursor.execute('''
INSERT INTO critical_alerts VALUES 
(3, 2, 'ALLERGY', 'Shellfish allergy', 'MEDIUM', 'N')
''')

conn.commit()
conn.close()

print("✅ Database created successfully: healthcare.db")
print("✅ Sample data inserted")
