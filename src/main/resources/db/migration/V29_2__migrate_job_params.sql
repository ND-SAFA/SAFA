ALTER TABLE job
    DROP FOREIGN KEY job_ibfk_2;
ALTER TABLE job
    ADD CONSTRAINT job_ibfk_2
        FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE SET NULL;
