ALTER TABLE password_reset_token
    DROP CONSTRAINT password_reset_token_ibfk_1;

ALTER TABLE password_reset_token
    ADD CONSTRAINT password_reset_token_ibfk_1 FOREIGN KEY (user_id) REFERENCES safa_user (user_id) ON DELETE CASCADE;
