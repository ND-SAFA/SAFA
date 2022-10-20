ALTER TABLE github_project
    DROP CONSTRAINT github_project_ibfk_1;

ALTER TABLE github_project
    DROP COLUMN safa_project_id;

ALTER TABLE github_project
    ADD COLUMN safa_project_id VARCHAR(255) NOT NULL;

ALTER TABLE github_project
    ADD CONSTRAINT github_project_safa_project_fk1
        FOREIGN KEY (safa_project_id) REFERENCES project (project_id) ON DELETE CASCADE;
