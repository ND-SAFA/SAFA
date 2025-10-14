CREATE TABLE IF NOT EXISTS comment
(
    id          BINARY(16)   NOT NULL PRIMARY KEY,
    content     mediumtext   NOT NULL,
    status      VARCHAR(255) NOT NULL,
    type        VARCHAR(255) NOT NULL,
    created_at  DATETIME(6)  NOT NULL,
    updated_at  DATETIME(6)  NOT NULL,
    author_id   VARCHAR(255),
    artifact_id VARCHAR(255) NOT NULL,
    version_id  VARCHAR(255) NOT NULL,
    constraint comment_author_id_fk foreign key (author_id) references safa_user (user_id) on delete cascade,
    constraint comment_artifact_id_df foreign key (artifact_id) references artifact (artifact_id) on delete cascade,
    constraint comment_version_id_fk foreign key (version_id) references project_version (version_id) on delete cascade
);


CREATE TABLE IF NOT EXISTS comment_concept
(
    id           BINARY(16)   NOT NULL PRIMARY KEY,
    comment_id   BINARY(16)   NOT NULL,
    concept_name VARCHAR(255) NOT NULL,
    constraint unknown_concept_comment_comment_id_fk foreign key (comment_id) references comment (id) on delete cascade
);

CREATE TABLE IF NOT EXISTS comment_artifact
(
    id          BINARY(16)   NOT NULL PRIMARY KEY,
    comment_id  BINARY(16)   NOT NULL,
    artifact_id VARCHAR(255) NOT NULL,
    constraint comment_artifact_comment_id_fk foreign key (comment_id) references comment (id) on delete cascade,
    constraint comment_artifact_artifact_id_fk foreign key (artifact_id) references artifact (artifact_id) on delete cascade
);
