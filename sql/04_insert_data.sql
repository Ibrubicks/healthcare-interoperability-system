
-- ==========================================
-- INSERT HOSPITAL SYSTEMS
-- ==========================================
INSERT INTO Hospital_Systems VALUES (100, 'City Medical Center', 'New York', 'Epic', 'https://api.citymedical.com/fhir/r4', SYSDATE);
INSERT INTO Hospital_Systems VALUES (101, 'St. Peter''s Hospital', 'Los Angeles', 'Cerner', 'https://api.stpeters.com/fhir/r4', SYSDATE);
INSERT INTO Hospital_Systems VALUES (102, 'Valley Health System', 'San Francisco', 'NextGen', 'https://api.valleyhealth.com/fhir/r4', SYSDATE);

COMMIT;

-- ==========================================
-- INSERT PATIENTS
-- ==========================================
INSERT INTO Patients VALUES (1000, 'John', 'Smith', TO_DATE('1965-03-15', 'YYYY-MM-DD'), 'M', '123-45-6789', '212-555-0101', 'john.smith@email.com', 'Sarah Smith', SYSDATE, SYSDATE);
INSERT INTO Patients VALUES (1001, 'Maria', 'Garcia', TO_DATE('1978-07-22', 'YYYY-MM-DD'), 'F', '987-65-4321', '415-555-0202', 'maria.garcia@email.com', 'Carlos Garcia', SYSDATE, SYSDATE);
INSERT INTO Patients VALUES (1002, 'Robert', 'Johnson', TO_DATE('1952-11-08', 'YYYY-MM-DD'), 'M', '456-78-9012', '310-555-0303', 'robert.johnson@email.com', 'Linda Johnson', SYSDATE, SYSDATE);

COMMIT;

-- ==========================================
-- INSERT PATIENT RECORDS - CITY MEDICAL
-- ==========================================
INSERT INTO Patient_Records VALUES (5000, 1000, 100, 'CMC-2024-98765', 'Type 2 Diabetes since 2015. Hypertension controlled. Previous MI in 2019.', '[{"medication":"Metformin","dose":"1000mg","frequency":"twice daily"},{"medication":"Lisinopril","dose":"10mg","frequency":"daily"}]', '[{"allergen":"Penicillin","reaction":"anaphylaxis","severity":"CRITICAL"},{"allergen":"Codeine","reaction":"severe rash","severity":"HIGH"}]', '[{"condition":"Type 2 Diabetes","icd_code":"E11.9"},{"condition":"Hypertension","icd_code":"I10"},{"condition":"CAD","icd_code":"I25.10"}]', TO_DATE('2024-10-15', 'YYYY-MM-DD'), SYSDATE);

INSERT INTO Patient_Records VALUES (5001, 1001, 100, 'CMC-2024-54321', 'Asthma patient. Occasional inhaler use. No significant surgeries.', '[{"medication":"Albuterol","dose":"2 puffs","frequency":"as needed"}]', '[{"allergen":"Sulfa drugs","reaction":"rash","severity":"MEDIUM"}]', '[{"condition":"Asthma","icd_code":"J45.9"}]', TO_DATE('2024-09-20', 'YYYY-MM-DD'), SYSDATE);

COMMIT;

-- ==========================================
-- INSERT PATIENT RECORDS - ST. PETERS
-- ==========================================
INSERT INTO Patient_Records VALUES (5002, 1000, 101, 'SPH-98765-2024', 'Diabetes mellitus. Cardiac history. Last EKG showed normal findings.', '[{"medication":"Metformin","dose":"1g","frequency":"BID"},{"medication":"Lisinopril","dose":"10mg","frequency":"OD"},{"medication":"Aspirin","dose":"81mg","frequency":"daily"}]', '[{"allergen":"Penicillin","reaction":"severe allergic reaction","severity":"CRITICAL"},{"allergen":"Codein","reaction":"dermatitis","severity":"HIGH"}]', '[{"condition":"Diabetes Type II","icd_code":"E11.9"},{"condition":"HTN","icd_code":"I10"}]', TO_DATE('2024-10-10', 'YYYY-MM-DD'), SYSDATE);

INSERT INTO Patient_Records VALUES (5003, 1002, 101, 'SPH-78901-2024', 'Elderly patient. COPD. Frequent respiratory issues. Lives independently.', '[{"medication":"Tiotropium","dose":"18mcg","frequency":"daily"},{"medication":"Omeprazole","dose":"20mg","frequency":"daily"}]', '[{"allergen":"NSAID","reaction":"GI bleeding","severity":"CRITICAL"}]', '[{"condition":"COPD","icd_code":"J44.9"},{"condition":"Gastric Ulcer","icd_code":"K25.9"}]', TO_DATE('2024-10-12', 'YYYY-MM-DD'), SYSDATE);

COMMIT;

-- ==========================================
-- INSERT PATIENT RECORDS - VALLEY HEALTH
-- ==========================================
INSERT INTO Patient_Records VALUES (5004, 1000, 102, 'VHS2024-98765A', 'Patient reports history of diabetes and high blood pressure. On multiple medications.', '[{"medication":"Metformin","dose":"1000mg","frequency":"2x daily"},{"medication":"Lisinopril","dose":"10 mg","frequency":"once daily"}]', '[{"allergen":"Penicillin","reaction":"anaphylaxis shock","severity":"CRITICAL"},{"allergen":"Codeine","reaction":"hives and rash","severity":"HIGH"}]', '[{"condition":"DM2","icd_code":"E11.9"},{"condition":"Hypertension","icd_code":"I10"}]', TO_DATE('2024-10-18', 'YYYY-MM-DD'), SYSDATE);

INSERT INTO Patient_Records VALUES (5005, 1001, 102, 'VHS2024-54321B', 'Young female with asthma. Controlled with medication.', '[{"medication":"Salbutamol","dose":"100mcg","frequency":"PRN"}]', '[{"allergen":"Sulfamethoxazole","reaction":"urticaria","severity":"MEDIUM"}]', '[{"condition":"Asthma","icd_code":"J45.9"}]', TO_DATE('2024-10-14', 'YYYY-MM-DD'), SYSDATE);

COMMIT;