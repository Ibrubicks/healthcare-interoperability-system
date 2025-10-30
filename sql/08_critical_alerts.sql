
-- ==========================================
-- INSERT CRITICAL ALERTS
-- ==========================================

INSERT INTO Critical_Alerts VALUES (seq_alert_id.NEXTVAL, 1000, 'ALLERGY', 'CRITICAL - Penicillin allergy detected', 'CRITICAL', '[{"allergen":"Penicillin","reaction":"anaphylaxis","severity":"CRITICAL"}]', SYSDATE, 'N', NULL, NULL);

INSERT INTO Critical_Alerts VALUES (seq_alert_id.NEXTVAL, 1000, 'ALLERGY', 'HIGH - Codeine allergy detected', 'HIGH', '[{"allergen":"Codeine","reaction":"severe rash","severity":"HIGH"}]', SYSDATE, 'N', NULL, NULL);

INSERT INTO Critical_Alerts VALUES (seq_alert_id.NEXTVAL, 1002, 'ALLERGY', 'CRITICAL - NSAID allergy (GI bleeding risk)', 'CRITICAL', '[{"allergen":"NSAID","reaction":"GI bleeding","severity":"CRITICAL"}]', SYSDATE, 'N', NULL, NULL);

COMMIT;

-- ==========================================
-- INSERT AUDIT TRAIL ENTRIES
-- ==========================================

INSERT INTO Access_Logs (Log_ID, User_ID, Patient_ID, Action, Record_Type, Status, IP_Address, Access_Date, Purpose_of_Access)
VALUES (seq_log_id.NEXTVAL, 'DR_EMILY_THOMAS', 1000, 'VIEW', 'PATIENT_FULL_RECORD', 'SUCCESS', '192.168.1.105', SYSDATE, 'Emergency lookup - Unconscious patient');

INSERT INTO Access_Logs (Log_ID, User_ID, Patient_ID, Action, Record_Type, Status, IP_Address, Access_Date, Purpose_of_Access)
VALUES (seq_log_id.NEXTVAL, 'DR_JAMES_WILSON', 1001, 'VIEW', 'PATIENT_FULL_RECORD', 'SUCCESS', '192.168.1.106', SYSDATE, 'Emergency lookup - Asthma check');

INSERT INTO Access_Logs (Log_ID, User_ID, Patient_ID, Action, Record_Type, Status, IP_Address, Access_Date, Purpose_of_Access)
VALUES (seq_log_id.NEXTVAL, 'DR_ROBERT_ANDERSON', 1002, 'VIEW', 'PATIENT_FULL_RECORD', 'SUCCESS', '192.168.1.107', SYSDATE, 'Emergency lookup - COPD patient');

COMMIT;

-- ==========================================
-- VERIFICATION QUERIES
-- ==========================================

SELECT COUNT(*) AS total_alerts FROM Critical_Alerts;
SELECT COUNT(*) AS total_access_logs FROM Access_Logs;