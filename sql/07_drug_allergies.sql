-- ==========================================
-- Drug-Allergy Interaction Matrix
-- ==========================================

INSERT INTO Drug_Allergy_Matrix VALUES (1, 'PENI-001', 'Penicillin', 'PENI', 'Penicillin', 'CONTRAINDICATED', 'Penicillin allergy - Risk of anaphylaxis', SYSDATE);
INSERT INTO Drug_Allergy_Matrix VALUES (2, 'AMOX-001', 'Amoxicillin', 'PENI', 'Penicillin', 'CONTRAINDICATED', 'Amoxicillin is a penicillin-class antibiotic', SYSDATE);
INSERT INTO Drug_Allergy_Matrix VALUES (3, 'CODEI-001', 'Codeine', 'CODE', 'Codeine', 'CONTRAINDICATED', 'Known codeine allergy - Risk of severe rash', SYSDATE);
INSERT INTO Drug_Allergy_Matrix VALUES (4, 'ASPIR-001', 'Aspirin', 'NSAI', 'NSAID', 'SIGNIFICANT', 'NSAIDs can cause GI bleeding in patients with ulcers', SYSDATE);
INSERT INTO Drug_Allergy_Matrix VALUES (5, 'IBUPR-001', 'Ibuprofen', 'NSAI', 'NSAID', 'SIGNIFICANT', 'NSAIDs can cause GI bleeding - Monitor closely', SYSDATE);
INSERT INTO Drug_Allergy_Matrix VALUES (6, 'SULFA-001', 'Sulfamethoxazole', 'SULFA', 'Sulfa drugs', 'SIGNIFICANT', 'Sulfa allergy - Risk of urticaria and rash', SYSDATE);
INSERT INTO Drug_Allergy_Matrix VALUES (7, 'METRO-001', 'Metformin', 'DIABT', 'Diabetes Treatment', 'MINOR', 'Safe for diabetes management', SYSDATE);

COMMIT;

SELECT COUNT(*) FROM Drug_Allergy_Matrix;