CREATE TABLE github_access_credentials (
  artifact_id char(36) NOT NULL,
   version SMALLINT NULL,
   access_token VARCHAR(64) NULL,
   refresh_token VARCHAR(128) NULL,
   client_secret VARCHAR(64) NULL,
   client_id VARCHAR(64) NULL,
   user_id char(36) NOT NULL,
   access_token_expiration_date datetime NULL,
   refresh_token_expiration_date datetime NULL,
   github_handler VARCHAR(255) NULL,
   CONSTRAINT pk_github_access_credentials PRIMARY KEY (artifact_id)
);

CREATE TABLE github_project (
  mapping_id char(36) NOT NULL,
   safa_project_id char(36) NOT NULL,
   repository_name VARCHAR(255) NOT NULL,
   branch VARCHAR(32) NOT NULL,
   last_commit_sha VARCHAR(64) NOT NULL,
   user_id char(36) NOT NULL,
   CONSTRAINT pk_github_project PRIMARY KEY (mapping_id)
);

ALTER TABLE github_access_credentials ADD CONSTRAINT FK_GITHUB_ACCESS_CREDENTIALS_ON_USER FOREIGN KEY (user_id) REFERENCES safa_user (user_id);

ALTER TABLE github_project ADD CONSTRAINT FK_GITHUB_PROJECT_ON_SAFA_PROJECT FOREIGN KEY (safa_project_id) REFERENCES project (project_id);

ALTER TABLE github_project ADD CONSTRAINT FK_GITHUB_PROJECT_ON_USER FOREIGN KEY (user_id) REFERENCES safa_user (user_id);