ALTER TABLE safa_user
    ADD COLUMN default_org_id BINARY(16) DEFAULT NULL;

UPDATE safa_user
    SET default_org_id = personal_org_id
    WHERE default_org_id IS NULL;