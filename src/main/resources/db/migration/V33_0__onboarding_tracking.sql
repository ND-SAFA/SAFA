CREATE TABLE IF NOT EXISTS onboarding
(
    id         BINARY(16)   NOT NULL PRIMARY KEY,
    user_id    VARCHAR(255) NOT NULL,
    completed  BOOL         NOT NULL,
    project_id VARCHAR(255) NULL,
    CONSTRAINT onboarding_user_id_fk FOREIGN KEY (user_id) REFERENCES safa_user (user_id) ON DELETE CASCADE,
    CONSTRAINT onboarding_user_id_unique UNIQUE (user_id),
    CONSTRAINT onboarding_project_id_fk FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE SET NULL
);
