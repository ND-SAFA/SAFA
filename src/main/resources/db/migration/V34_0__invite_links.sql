CREATE TABLE IF NOT EXISTS membership_invite_token
(
    id           BINARY(16)    NOT NULL PRIMARY KEY,
    entity_id    VARCHAR(255)  NOT NULL,
    expiration   DATETIME      NOT NULL,
    role         VARCHAR(255)  NOT NULL
);