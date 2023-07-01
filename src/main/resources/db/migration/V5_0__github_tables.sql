CREATE TABLE IF NOT EXISTS github_access_credentials
(
    artifact_id                   varchar(255) NOT NULL PRIMARY KEY,
    version                       SMALLINT     NULL,
    access_token                  VARCHAR(64)  NULL,
    refresh_token                 VARCHAR(128) NULL,
    client_secret                 VARCHAR(64)  NULL,
    client_id                     VARCHAR(64)  NULL,
    user_id                       varchar(255) NOT NULL,
    access_token_expiration_date  datetime     NULL,
    refresh_token_expiration_date datetime     NULL,
    github_handler                VARCHAR(255) NULL,
    CONSTRAINT github_access_credentials_ibfk_1 FOREIGN KEY (user_id) REFERENCES safa_user (user_id)
);

CREATE TABLE IF NOT EXISTS github_project
(
    mapping_id      VARCHAR(255) NOT NULL PRIMARY KEY,
    safa_project_id VARCHAR(255) NOT NULL,
    repository_name VARCHAR(255) NOT NULL,
    branch          VARCHAR(32)  NOT NULL,
    last_commit_sha VARCHAR(64)  NOT NULL,
    user_id         VARCHAR(255) NOT NULL,
    CONSTRAINT github_project_ibfk_1 FOREIGN KEY (safa_project_id) REFERENCES project (project_id),
    CONSTRAINT github_project_ibfk_2 FOREIGN KEY (user_id) REFERENCES safa_user (user_id)
);
