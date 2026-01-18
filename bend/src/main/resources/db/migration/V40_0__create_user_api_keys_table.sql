-- Create user_api_keys table for storing encrypted user API keys
CREATE TABLE user_api_keys (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    openai_api_key VARCHAR(512),
    anthropic_api_key VARCHAR(512),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_api_keys_user FOREIGN KEY (user_id) REFERENCES safa_user(user_id) ON DELETE CASCADE
);

-- Add unique constraint on user_id (one API key record per user)
CREATE UNIQUE INDEX idx_user_api_keys_user_id ON user_api_keys(user_id);

-- Add index for performance on updated_at
CREATE INDEX idx_user_api_keys_updated ON user_api_keys(updated_at);
