CREATE TABLE IF NOT EXISTS chat
(
    id         BINARY(16)                         NOT NULL PRIMARY KEY,
    version_id VARCHAR(255) CHARACTER SET utf8mb3 NOT NULL,
    owner_id   VARCHAR(255) CHARACTER SET utf8mb3 NOT NULL,
    title      VARCHAR(255),
    CONSTRAINT version_id_fk FOREIGN KEY (version_id) REFERENCES project_version (version_id) ON DELETE CASCADE,
    CONSTRAINT chat_user_id_fk FOREIGN KEY (owner_id) REFERENCES safa_user (user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chat_message
(
    id        BINARY(16) NOT NULL PRIMARY KEY,
    chat_id   BINARY(16) NOT NULL,
    is_user   BOOL,
    author_id VARCHAR(255) CHARACTER SET utf8mb3,
    created   DATETIME,
    content   MEDIUMTEXT,
    CONSTRAINT chat_message_chat_id_fk FOREIGN KEY (chat_id) REFERENCES chat (id) ON DELETE CASCADE,
    CONSTRAINT chat_message_author_id_fk FOREIGN KEY (author_id) REFERENCES safa_user (user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chat_message_artifact
(
    id          BINARY(16) NOT NULL PRIMARY KEY,
    message_id  BINARY(16) NOT NULL,
    artifact_id VARCHAR(255) CHARACTER SET utf8mb3,
    CONSTRAINT chat_message_artifact_message_id_fk FOREIGN KEY (message_id) REFERENCES chat_message (id) ON DELETE CASCADE,
    CONSTRAINT chat_message_artifact_artifact_id_fk FOREIGN KEY (artifact_id) REFERENCES artifact (artifact_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chat_share
(
    id         BINARY(16)   NOT NULL PRIMARY KEY,
    chat_id    BINARY(16)   NOT NULL,
    user_id    VARCHAR(255) NOT NULL,
    permission varchar(255),
    CONSTRAINT chat_share_user_id_fk FOREIGN KEY (user_id) REFERENCES safa_user (user_id) ON DELETE CASCADE
);
