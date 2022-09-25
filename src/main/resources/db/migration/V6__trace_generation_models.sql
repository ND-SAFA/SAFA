CREATE TABLE IF NOT EXISTS trace_generation_model
(
    id         varchar(255) NOT NULL PRIMARY KEY,
    name       varchar(255) NOT NULL,
    base_model varchar(255) NOT NULL,
    project_id varchar(255) NOT NULL,
    CONSTRAINT trace_generation_model_ibfk_1 FOREIGN KEY (project_id) REFERENCES project (project_id)
);
