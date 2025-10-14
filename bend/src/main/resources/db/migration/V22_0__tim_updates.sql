DROP TABLE IF EXISTS trace_matrix;

ALTER TABLE artifact_type RENAME COLUMN type_id TO id;
ALTER TABLE artifact_type ADD COLUMN color VARCHAR(255) NOT NULL DEFAULT '';

CREATE TABLE IF NOT EXISTS trace_matrix
(
    id                   BINARY(16) NOT NULL PRIMARY KEY,
    project_version_id   VARCHAR(255) NOT NULL,
    source_type_id       VARCHAR(255) NOT NULL,
    target_type_id       VARCHAR(255) NOT NULL,
    count                INT NOT NULL DEFAULT 0,
    generated_count       INT NOT NULL DEFAULT 0,
    approved_count        INT NOT NULL DEFAULT 0,
    FOREIGN KEY (source_type_id) REFERENCES artifact_type (id) ON DELETE CASCADE,
    FOREIGN KEY (target_type_id) REFERENCES artifact_type (id) ON DELETE CASCADE,
    FOREIGN KEY (project_version_id) REFERENCES project_version (version_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS type_counts
(
    id                   BINARY(16) NOT NULL PRIMARY KEY,
    type_id              VARCHAR(255) NOT NULL,
    project_version_id   VARCHAR(255) NOT NULL,
    count                INT NOT NULL DEFAULT 0,
    FOREIGN KEY (type_id) REFERENCES artifact_type (id) ON DELETE CASCADE,
    FOREIGN KEY (project_version_id) REFERENCES project_version (version_id) ON DELETE CASCADE
);

