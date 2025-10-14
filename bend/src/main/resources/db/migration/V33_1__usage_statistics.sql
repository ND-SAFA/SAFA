CREATE TABLE IF NOT EXISTS usage_statistics
(
    id                     BINARY(16)   NOT NULL PRIMARY KEY,
    user_id                VARCHAR(255) NOT NULL,
    project_imports        INT,
    project_summarizations INT,
    project_generations    INT,
    lines_generated_on     INT,
    account_created        DATETIME,
    github_linked          DATETIME,
    project_imported       DATETIME,
    generation_performed   DATETIME,
    CONSTRAINT usage_statistics_user_id_fk FOREIGN KEY (user_id) REFERENCES safa_user (user_id) ON DELETE CASCADE,
    CONSTRAINT usage_statistics_user_id_unique UNIQUE (user_id)
);
