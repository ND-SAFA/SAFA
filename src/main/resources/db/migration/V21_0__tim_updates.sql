DROP TABLE IF EXISTS trace_matrix;

CREATE TABLE IF NOT EXISTS trace_matrix
(
    id                BINARY(16) NOT NULL PRIMARY KEY,
    sourceType        VARCHAR(255) NOT NULL,
    targetType        VARCHAR(255) NOT NULL,
    count             INT NOT NULL DEFAULT 0,
    generatedCount    INT NOT NULL DEFAULT 0,
    approvedCount     INT NOT NULL DEFAULT 0,
    FOREIGN KEY (sourceType) REFERENCES artifact_type (type_id),
    FOREIGN KEY (targetType) REFERENCES artifact_type (type_id)
);

ALTER TABLE artifact_type RENAME COLUMN type_id TO id;
ALTER TABLE artifact_type ADD COLUMN color VARCHAR(255) NOT NULL;
ALTER TABLE artifact_type ADD COLUMN count INT NOT NULL DEFAULT 0;

