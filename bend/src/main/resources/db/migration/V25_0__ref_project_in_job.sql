ALTER TABLE job
    ADD COLUMN project_id VARCHAR(255);

ALTER TABLE job
    ADD CONSTRAINT job_ibfk_2
        FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE SET NULL;
