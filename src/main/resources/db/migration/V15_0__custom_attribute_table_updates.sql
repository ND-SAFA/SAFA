ALTER TABLE artifact_body
DROP COLUMN custom_fields;

CREATE TABLE custom_attribute
(
    id                VARCHAR(255) NOT NULL,
    type              INT          NOT NULL,
    keyname           VARCHAR(255) NOT NULL,
    label             VARCHAR(255) NOT NULL,
    project_id        VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT UNIQUE_KEYNAME_PER_PROJECT UNIQUE (keyname, project_id),
    FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE CASCADE
);

CREATE TABLE selection_attribute_option
(
    id               VARCHAR(255) NOT NULL,
    option_value     VARCHAR(255) NOT NULL,
    attribute_id     VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (attribute_id) REFERENCES custom_attribute (id) ON DELETE CASCADE
);

CREATE TABLE float_attribute
(
    id               VARCHAR(255) NOT NULL,
    min              DOUBLE       NOT NULL,
    max              DOUBLE       NOT NULL,
    attribute_id     VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (attribute_id) REFERENCES custom_attribute (id) ON DELETE CASCADE
);

CREATE TABLE integer_attribute
(
    id               VARCHAR(255) NOT NULL,
    min              INT          NOT NULL,
    max              INT          NOT NULL,
    attribute_id     VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (attribute_id) REFERENCES custom_attribute (id) ON DELETE CASCADE
);

CREATE TABLE artifact_attribute_version
(
    id                   VARCHAR(255) NOT NULL,
    artifact_version_id  VARCHAR(255) NOT NULL,
    attribute_id         VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (artifact_version_id) REFERENCES artifact_body (entity_version_id) ON DELETE CASCADE,
    FOREIGN KEY (attribute_id) REFERENCES custom_attribute (id) ON DELETE CASCADE
);

CREATE TABLE string_attribute_value
(
    id                    VARCHAR(255) NOT NULL,
    attribute_value       MEDIUMTEXT   NOT NULL,
    attribute_version_id  VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT UNIQUE_STRING_ATTRIBUTE_VALUE_PER_ATTRIBUTE UNIQUE (attribute_version_id),
    FOREIGN KEY (attribute_version_id) REFERENCES artifact_attribute_version (id) ON DELETE CASCADE
);

CREATE TABLE string_array_attribute_value
(
    id                    VARCHAR(255) NOT NULL,
    attribute_value       MEDIUMTEXT   NOT NULL,
    attribute_version_id  VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (attribute_version_id) REFERENCES artifact_attribute_version (id) ON DELETE CASCADE
);

CREATE TABLE integer_attribute_value
(
    id                    VARCHAR(255) NOT NULL,
    attribute_value       INT          NOT NULL,
    attribute_version_id  VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT UNIQUE_INTEGER_ATTRIBUTE_VALUE_PER_ATTRIBUTE UNIQUE (attribute_version_id),
    FOREIGN KEY (attribute_version_id) REFERENCES artifact_attribute_version (id) ON DELETE CASCADE
);

CREATE TABLE float_attribute_value
(
    id                    VARCHAR(255) NOT NULL,
    attribute_value       DOUBLE       NOT NULL,
    attribute_version_id  VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT UNIQUE_FLOAT_ATTRIBUTE_VALUE_PER_ATTRIBUTE UNIQUE (attribute_version_id),
    FOREIGN KEY (attribute_version_id) REFERENCES artifact_attribute_version (id) ON DELETE CASCADE
);

CREATE TABLE boolean_attribute_value
(
    id                    VARCHAR(255) NOT NULL,
    attribute_value       BOOLEAN      NOT NULL,
    attribute_version_id  VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT UNIQUE_BOOLEAN_ATTRIBUTE_VALUE_PER_ATTRIBUTE UNIQUE (attribute_version_id),
    FOREIGN KEY (attribute_version_id) REFERENCES artifact_attribute_version (id) ON DELETE CASCADE
);