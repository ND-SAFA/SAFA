CREATE TABLE attribute_layout
(
    id             VARCHAR(255) NOT NULL,
    name           VARCHAR(255) NOT NULL,
    project_id     VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE CASCADE
);

CREATE TABLE attribute_position
(
    id             VARCHAR(255) NOT NULL,
    x              INT          NOT NULL,
    y              INT          NOT NULL,
    width          INT          NOT NULL,
    height         INT          NOT NULL,
    layout_id      VARCHAR(255) NOT NULL,
    attribute_id   VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (layout_id) REFERENCES attribute_layout (id) ON DELETE CASCADE,
    FOREIGN KEY (attribute_id) REFERENCES custom_attribute (id) ON DELETE CASCADE
);

CREATE TABLE artifact_type_to_layout
(
    id                 VARCHAR(255) NOT NULL,
    artifact_type_id   VARCHAR(255) NOT NULL,
    layout_id          VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (layout_id) REFERENCES attribute_layout (id) ON DELETE CASCADE,
    FOREIGN KEY (artifact_type_id) REFERENCES artifact_type (type_id) ON DELETE CASCADE
);
