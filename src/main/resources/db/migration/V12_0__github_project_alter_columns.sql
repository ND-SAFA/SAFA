ALTER TABLE github_project
    DROP CONSTRAINT github_project_ibfk_2;

ALTER TABLE github_project
    DROP COLUMN user_id;

ALTER TABLE github_project
    MODIFY COLUMN last_commit_sha VARCHAR(64) NULL;
