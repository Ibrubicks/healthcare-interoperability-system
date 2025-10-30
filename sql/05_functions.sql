
-- ==========================================
-- CREATE FUZZY MATCHING FUNCTIONS
-- ==========================================

CREATE OR REPLACE FUNCTION calculate_name_similarity(name1 IN VARCHAR2, name2 IN VARCHAR2) RETURN NUMBER IS
    match_percentage NUMBER;
BEGIN
    name1 := UPPER(TRIM(name1));
    name2 := UPPER(TRIM(name2));
    IF name1 = name2 THEN RETURN 1.0; END IF;
    IF LENGTH(name1) = 0 OR LENGTH(name2) = 0 THEN RETURN 0.0; END IF;
    match_percentage := ROUND((1 - (ABS(LENGTH(name1) - LENGTH(name2)) / GREATEST(LENGTH(name1), LENGTH(name2)))), 2);
    IF SUBSTR(name1, 1, 3) = SUBSTR(name2, 1, 3) THEN match_percentage := ROUND(match_percentage + 0.15, 2); END IF;
    IF match_percentage > 1.0 THEN match_percentage := 1.0; END IF;
    RETURN match_percentage;
END;
/

CREATE OR REPLACE FUNCTION calculate_dob_similarity(dob1 IN DATE, dob2 IN DATE) RETURN NUMBER IS
    days_diff NUMBER;
BEGIN
    days_diff := ABS(dob1 - dob2);
    IF days_diff = 0 THEN RETURN 1.0;
    ELSIF days_diff <= 7 THEN RETURN 0.95;
    ELSIF days_diff <= 30 THEN RETURN 0.80;
    ELSIF days_diff <= 365 THEN RETURN 0.50;
    ELSE RETURN 0.0;
    END IF;
END;
/

CREATE OR REPLACE FUNCTION calculate_ssn_similarity(ssn1 IN VARCHAR2, ssn2 IN VARCHAR2) RETURN NUMBER IS
BEGIN
    IF ssn1 = ssn2 THEN RETURN 1.0;
    ELSIF ssn1 IS NULL OR ssn2 IS NULL THEN RETURN 0.0;
    ELSE RETURN 0.0;
    END IF;
END;
/
