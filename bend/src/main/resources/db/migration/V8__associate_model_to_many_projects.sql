CREATE TABLE IF NOT EXISTS model_project
(
    id         varchar(255) NOT NULL PRIMARY KEY,
    model_id   varchar(255) NOT NULL,
    project_id varchar(255) NOT NULL,
    CONSTRAINT model_reference FOREIGN KEY (model_id) REFERENCES trace_generation_model (id),
    CONSTRAINT project_reference FOREIGN KEY (project_id) REFERENCES project (project_id)
);

ALTER TABLE trace_generation_model
    DROP CONSTRAINT trace_generation_model_ibfk_1;

ALTER TABLE trace_generation_model
    DROP COLUMN project_id;
