CREATE TABLE IF NOT EXISTS share_project_token
(
    id           BINARY(16)    NOT NULL PRIMARY KEY,
    project_id   VARCHAR(255)  NOT NULL,
    expiration   DATETIME      NOT NULL,
    role         VARCHAR(255)  NOT NULL,
    CONSTRAINT share_project_token_project_id_fk FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE CASCADE
);