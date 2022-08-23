CREATE TABLE IF NOT EXISTS artifact_position
(
    id          varchar(255) NOT NULL PRIMARY KEY,
    artifact_id varchar(255) NOT NULL,
    version_id  varchar(255) NOT NULL,
    document_id varchar(255),
    x           DOUBLE       NOT NULL,
    y           DOUBLE       NOT NULL,
    foreign key (artifact_id) references artifact (artifact_id) on delete cascade,
    foreign key (version_id) references project_version (version_id) on delete cascade,
    foreign key (document_id) references document (document_id) on delete cascade
);
