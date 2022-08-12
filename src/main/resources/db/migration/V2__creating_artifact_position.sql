CREATE TABLE IF NOT EXISTS artifact_position
(
    id                varchar(255) NOT NULL PRIMARY KEY,
    entity_version_id varchar(255) NOT NULL,
    document_id       varchar(255),
    x                 DOUBLE       NOT NULL,
    y                 DOUBLE       NOT NULL,
    FOREIGN KEY (entity_version_id) REFERENCES artifact_body (entity_version_id) ON DELETE CASCADE
);
