ALTER TABLE artifact
DROP COLUMN document_type;

ALTER TABLE artifact_body
DROP COLUMN custom_fields;

CREATE TABLE artifact_schema_field
(
    id                VARCHAR(255) NOT NULL,
    type              INT          NOT NULL,
    keyname           VARCHAR(255) NOT NULL,
    label             VARCHAR(255) NOT NULL,
    artifact_type_id  VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT UNIQUE_KEYNAME_PER_ARTIFACT_TYPE UNIQUE (keyname, artifact_type_id),
    FOREIGN KEY (artifact_type_id) REFERENCES artifact_type (type_id) ON DELETE CASCADE
);

CREATE TABLE selection_field_option
(
    id               VARCHAR(255) NOT NULL,
    value            VARCHAR(255) NOT NULL,
    schema_field_id  VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (schema_field_id) REFERENCES artifact_schema_field (id) ON DELETE CASCADE
);

CREATE TABLE float_field
(
    id               VARCHAR(255) NOT NULL,
    min              FLOAT        NOT NULL,
    max              FLOAT        NOT NULL,
    schema_field_id  VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (schema_field_id) REFERENCES artifact_schema_field (id) ON DELETE CASCADE
);

CREATE TABLE integer_field
(
    id               VARCHAR(255) NOT NULL,
    min              INT          NOT NULL,
    max              INT          NOT NULL,
    schema_field_id  VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (schema_field_id) REFERENCES artifact_schema_field (id) ON DELETE CASCADE
);

CREATE TABLE artifact_field_version
(
    id                   VARCHAR(255) NOT NULL,
    artifact_version_id  VARCHAR(255) NOT NULL,
    field_id             VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (artifact_version_id) REFERENCES artifact_body (entity_version_id) ON DELETE CASCADE,
    FOREIGN KEY (field_id) REFERENCES artifact_schema_field (id) ON DELETE CASCADE
);

CREATE TABLE string_field_value
(
    id                   VARCHAR(255) NOT NULL,
    value                MEDIUMTEXT   NOT NULL,
    field_version_id     VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (field_version_id) REFERENCES artifact_field_version (id) ON DELETE CASCADE
);

CREATE TABLE string_array_field_value
(
    id                   VARCHAR(255) NOT NULL,
    value                MEDIUMTEXT   NOT NULL,
    field_version_id     VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (field_version_id) REFERENCES artifact_field_version (id) ON DELETE CASCADE
);

CREATE TABLE integer_field_value
(
    id                   VARCHAR(255) NOT NULL,
    value                INT          NOT NULL,
    field_version_id     VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (field_version_id) REFERENCES artifact_field_version (id) ON DELETE CASCADE
);

CREATE TABLE float_field_value
(
    id                   VARCHAR(255) NOT NULL,
    value                FLOAT        NOT NULL,
    field_version_id     VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (field_version_id) REFERENCES artifact_field_version (id) ON DELETE CASCADE
);

CREATE TABLE boolean_field_value
(
    id                   VARCHAR(255) NOT NULL,
    value                BOOLEAN      NOT NULL,
    field_version_id     VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (field_version_id) REFERENCES artifact_field_version (id) ON DELETE CASCADE
);