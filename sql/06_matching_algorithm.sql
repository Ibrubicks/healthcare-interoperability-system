-- ==========================================
-- PROBABILISTIC MATCHING ALGORITHM
-- ==========================================

DECLARE
    v_fname_score NUMBER;
    v_lname_score NUMBER;
    v_dob_score NUMBER;
    v_ssn_score NUMBER;
    v_overall_score NUMBER;
BEGIN
    FOR rec IN (
        SELECT p1.patient_id AS p1_id, p2.patient_id AS p2_id,
               p1.first_name, p1.last_name, p1.date_of_birth, p1.ssn,
               p2.first_name AS p2_first, p2.last_name AS p2_last,
               p2.date_of_birth AS p2_dob, p2.ssn AS p2_ssn,
               pr1.hospital_id AS h1_id, pr2.hospital_id AS h2_id
        FROM Patients p1
        JOIN Patient_Records pr1 ON p1.patient_id = pr1.patient_id
        JOIN Patients p2 ON p1.patient_id < p2.patient_id
        JOIN Patient_Records pr2 ON p2.patient_id = pr2.patient_id
        WHERE pr1.hospital_id < pr2.hospital_id
    )
    LOOP
        v_fname_score := calculate_name_similarity(rec.first_name, rec.p2_first);
        v_lname_score := calculate_name_similarity(rec.last_name, rec.p2_last);
        v_dob_score := calculate_dob_similarity(rec.date_of_birth, rec.p2_dob);
        v_ssn_score := calculate_ssn_similarity(rec.ssn, rec.p2_ssn);
        v_overall_score := ROUND((v_fname_score * 0.15) + (v_lname_score * 0.25) + (v_dob_score * 0.35) + (v_ssn_score * 0.25), 2);
        
        IF v_overall_score > 0.75 THEN
            INSERT INTO Matching_Scores (Match_ID, Patient_ID_1, Patient_ID_2, Hospital_ID_1, Hospital_ID_2,
                First_Name_Score, Last_Name_Score, DOB_Score, SSN_Score, Overall_Confidence_Score, Match_Status)
            VALUES (seq_match_id.NEXTVAL, rec.p1_id, rec.p2_id, rec.h1_id, rec.h2_id,
                v_fname_score, v_lname_score, v_dob_score, v_ssn_score, v_overall_score, 'CONFIRMED');
        END IF;
    END LOOP;
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Probabilistic matching completed successfully!');
END;
/