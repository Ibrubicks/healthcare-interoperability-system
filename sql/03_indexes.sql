CREATE INDEX idx_patient_ssn ON Patients(SSN);
CREATE INDEX idx_patient_name ON Patients(Last_Name, First_Name);
CREATE INDEX idx_patient_dob ON Patients(Date_of_Birth);
CREATE INDEX idx_record_hospital ON Patient_Records(Hospital_ID);
CREATE INDEX idx_record_patient ON Patient_Records(Patient_ID);
CREATE INDEX idx_matching_confidence ON Matching_Scores(Overall_Confidence_Score);
CREATE INDEX idx_alerts_severity ON Critical_Alerts(Severity);
CREATE INDEX idx_alerts_patient ON Critical_Alerts(Patient_ID);
CREATE INDEX idx_logs_patient ON Access_Logs(Patient_ID);
CREATE INDEX idx_logs_date ON Access_Logs(Access_Date);
CREATE INDEX idx_logs_user ON Access_Logs(User_ID);

COMMIT;
