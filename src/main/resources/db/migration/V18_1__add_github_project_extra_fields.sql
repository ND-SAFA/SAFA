ALTER TABLE github_project ADD COLUMN include mediumtext NOT NULL;
ALTER TABLE github_project ADD COLUMN exclude mediumtext NOT NULL;
ALTER TABLE github_project ADD COLUMN artifact_type_id VARCHAR(255) NOT NULL;