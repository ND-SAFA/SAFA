ALTER TABLE github_access_credentials
    DROP CONSTRAINT github_access_credentials_ibfk_1;

ALTER TABLE github_access_credentials
    ADD CONSTRAINT github_access_credentials_ibfk_1
        FOREIGN KEY (user_id) REFERENCES safa_user (user_id) ON DELETE CASCADE;