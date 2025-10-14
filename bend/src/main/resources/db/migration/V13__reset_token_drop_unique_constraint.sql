ALTER TABLE password_reset_token
MODIFY COLUMN user_id VARCHAR(36) NOT NULL;