ALTER TABLE model_project
    DROP CONSTRAINT model_reference;
ALTER TABLE model_project
    ADD CONSTRAINT model_reference
        FOREIGN KEY (model_id) REFERENCES trace_generation_model (id) ON DELETE CASCADE;
ALTER TABLE model_project
    DROP CONSTRAINT project_reference;
ALTER TABLE model_project
    ADD CONSTRAINT project_reference
        FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE CASCADE;
