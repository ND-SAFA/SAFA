-- Add preferred provider column to user_api_keys table
ALTER TABLE user_api_keys
ADD COLUMN preferred_provider VARCHAR(50) DEFAULT 'openai';

-- Add check constraint to ensure valid provider values
ALTER TABLE user_api_keys
ADD CONSTRAINT chk_preferred_provider
CHECK (preferred_provider IN ('openai', 'anthropic'));

-- Add index for performance
CREATE INDEX idx_user_api_keys_provider ON user_api_keys(preferred_provider);
