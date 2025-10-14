-- Add last_edited column
ALTER TABLE project
    ADD COLUMN last_edited DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;


