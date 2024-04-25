CREATE TABLE IF NOT EXISTS comment
(
    id          BINARY(16) NOT NULL PRIMARY KEY,
    content     mediumtext,
    status      VARCHAR(255),
    type        VARCHAR(255),
    created     DATETIME,
    updated     DATETIME,
    author_id   BINARY(16),
    artifact_id BINARY(16),
    version_id  BINARY(16),
    constraint comment_author_id_fk foreign key (author_id) references safa_user (user_id),
    constraint comment_artifact_id_df foreign key (artifact_id) references artifact (artifact_id),
    constraint comment_version_id_fk foreign key (version_id) references project_version (version_id)
);


CREATE TABLE IF NOT EXISTS comment_concept
(
    id           BINARY(16) NOT NULL PRIMARY KEY,
    comment_id   BINARY(16),
    concept_name VARCHAR(255),
    constraint unknown_concept_comment_comment_id_fk foreign key (comment_id) references comment (id)
);

CREATE TABLE IF NOT EXISTS comment_artifact
(
    id          BINARY(16) NOT NULL PRIMARY KEY,
    comment_id  BINARY(16),
    artifact_id BINARY(16),
    constraint unknown_concept_comment_comment_id_fk foreign key (comment_id) references comment (id),
    constraint contradiction_comment_artifact_artifact_id_df foreign key (artifact_id) references artifact (artifact_id)
);
