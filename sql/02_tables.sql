
-- ==========================================
-- TABLE 1: Hospital Systems Registry
-- ==========================================
CREATE TABLE Hospital_Systems (
    Hospital_ID NUMBER PRIMARY KEY,
    Hospital_Name VARCHAR2(100) NOT NULL,
    City VARCHAR2(50) NOT NULL,
    System_Type VARCHAR2(50),
    API_Endpoint VARCHAR2(200),
    Created_Date DATE DEFAULT SYSDATE,
    CONSTRAINT uk_hospital_name UNIQUE(Hospital_Name)
);

-- ==========================================
-- TABLE 2: Master Patient Index (MPI)
-- ==========================================
CREATE TABLE Patients (
    Patient_ID NUMBER PRIMARY KEY,
    First_Name VARCHAR2(50) NOT NULL,
    Last_Name VARCHAR2(50) NOT NULL,
    Date_of_Birth DATE NOT NULL,
    Gender CHAR(1),
    SSN VARCHAR2(20),
    Phone VARCHAR2(20),
    Email VARCHAR2(100),
    Emergency_Contact VARCHAR2(100),
    Created_Date DATE DEFAULT SYSDATE,
    Last_Updated DATE DEFAULT SYSDATE,
    CONSTRAINT chk_gender CHECK (Gender IN ('M', 'F', 'O')),
    CONSTRAINT uk_ssn UNIQUE(SSN)
);

-- ==========================================
-- TABLE 3: Hospital-Specific Patient Records
-- ==========================================
CREATE TABLE Patient_Records (
    Record_ID NUMBER PRIMARY KEY,
    Patient_ID NUMBER NOT NULL,
    Hospital_ID NUMBER NOT NULL,
    MRN VARCHAR2(30),
    Medical_History CLOB,
    Current_Medications CLOB,
    Allergies CLOB,
    Chronic_Conditions CLOB,
    Last_Visit_Date DATE,
    Last_Updated DATE DEFAULT SYSDATE,
    CONSTRAINT fk_patient FOREIGN KEY (Patient_ID) REFERENCES Patients(Patient_ID),
    CONSTRAINT fk_hospital FOREIGN KEY (Hospital_ID) REFERENCES Hospital_Systems(Hospital_ID),
    CONSTRAINT uk_hospital_mrn UNIQUE(Hospital_ID, MRN)
);

-- ==========================================
-- TABLE 4: FHIR Normalized Data
-- ==========================================
CREATE TABLE Normalized_Data (
    Normalized_ID NUMBER PRIMARY KEY,
    Patient_ID NUMBER NOT NULL,
    Record_ID NUMBER NOT NULL,
    FHIR_Standard VARCHAR2(10),
    FHIR_JSON CLOB NOT NULL,
    Normalization_Date DATE DEFAULT SYSDATE,
    CONSTRAINT fk_norm_patient FOREIGN KEY (Patient_ID) REFERENCES Patients(Patient_ID),
    CONSTRAINT fk_norm_record FOREIGN KEY (Record_ID) REFERENCES Patient_Records(Record_ID)
);

-- ==========================================
-- TABLE 5: Probabilistic Matching Scores
-- ==========================================
CREATE TABLE Matching_Scores (
    Match_ID NUMBER PRIMARY KEY,
    Patient_ID_1 NUMBER NOT NULL,
    Patient_ID_2 NUMBER NOT NULL,
    Hospital_ID_1 NUMBER NOT NULL,
    Hospital_ID_2 NUMBER NOT NULL,
    First_Name_Score NUMBER(3,2),
    Last_Name_Score NUMBER(3,2),
    DOB_Score NUMBER(3,2),
    SSN_Score NUMBER(3,2),
    Overall_Confidence_Score NUMBER(3,2),
    Match_Status VARCHAR2(20),
    Created_Date DATE DEFAULT SYSDATE,
    Reviewed_By VARCHAR2(100),
    Reviewed_Date DATE,
    CONSTRAINT chk_confidence CHECK (Overall_Confidence_Score >= 0 AND Overall_Confidence_Score <= 1)
);

-- ==========================================
-- TABLE 6: Critical Alerts System
-- ==========================================
CREATE TABLE Critical_Alerts (
    Alert_ID NUMBER PRIMARY KEY,
    Patient_ID NUMBER NOT NULL,
    Alert_Type VARCHAR2(50),
    Description VARCHAR2(500),
    Severity VARCHAR2(20),
    Alert_Details CLOB,
    Created_Date DATE DEFAULT SYSDATE,
    Acknowledged CHAR(1) DEFAULT 'N',
    Acknowledged_By VARCHAR2(100),
    Acknowledged_Date DATE,
    CONSTRAINT fk_alert_patient FOREIGN KEY (Patient_ID) REFERENCES Patients(Patient_ID),
    CONSTRAINT chk_severity CHECK (Severity IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')),
    CONSTRAINT chk_alert_type CHECK (Alert_Type IN ('ALLERGY', 'DRUG_INTERACTION', 'CHRONIC_CONDITION', 'MEDICATION_WARNING'))
);

-- ==========================================
-- TABLE 7: HIPAA-Compliant Audit Trail
-- ==========================================
CREATE TABLE Access_Logs (
    Log_ID NUMBER PRIMARY KEY,
    User_ID VARCHAR2(50) NOT NULL,
    Patient_ID NUMBER NOT NULL,
    Action VARCHAR2(100),
    Record_Type VARCHAR2(50),
    Status VARCHAR2(20),
    IP_Address VARCHAR2(20),
    Device_Info VARCHAR2(200),
    Access_Date DATE DEFAULT SYSDATE,
    Session_ID VARCHAR2(50),
    Purpose_of_Access VARCHAR2(200),
    Data_Elements_Accessed CLOB,
    CONSTRAINT fk_log_patient FOREIGN KEY (Patient_ID) REFERENCES Patients(Patient_ID)
);

-- ==========================================
-- TABLE 8: Drug-Allergy Interaction Database
-- ==========================================
CREATE TABLE Drug_Allergy_Matrix (
    Interaction_ID NUMBER PRIMARY KEY,
    Drug_Code VARCHAR2(20),
    Drug_Name VARCHAR2(100),
    Allergen_Code VARCHAR2(20),
    Allergen_Name VARCHAR2(100),
    Interaction_Severity VARCHAR2(20),
    Interaction_Description VARCHAR2(500),
    Created_Date DATE DEFAULT SYSDATE
);

-- ==========================================
-- TABLE 9: User Roles and Access Control
-- ==========================================
CREATE TABLE User_Roles (
    User_ID VARCHAR2(50) PRIMARY KEY,
    User_Name VARCHAR2(100) NOT NULL,
    Role_Type VARCHAR2(50),
    Department VARCHAR2(100),
    Hospital_ID NUMBER,
    Access_Level VARCHAR2(20),
    Created_Date DATE DEFAULT SYSDATE,
    Last_Login DATE,
    CONSTRAINT fk_user_hospital FOREIGN KEY (Hospital_ID) REFERENCES Hospital_Systems(Hospital_ID)
);

COMMIT;