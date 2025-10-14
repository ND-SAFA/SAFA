ALTER TABLE trace_generation_model
    DROP CONSTRAINT trace_generation_model_ibfk_1;
ALTER TABLE trace_generation_model
    ADD CONSTRAINT trace_generation_model_ibfk_1
        FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE CASCADE;

