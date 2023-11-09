ALTER TABLE safa_user ADD COLUMN verified BOOL DEFAULT FALSE;

CREATE TABLE IF NOT EXISTS email_verification_token
(
    id              BINARY(16)   NOT NULL PRIMARY KEY,
    user_id         VARCHAR(36)  NOT NULL UNIQUE,
    token           VARCHAR(255) NOT NULL,
    expiration_date datetime     NOT NULL,
    constraint email_verification_token_ibfk_1 foreign key (user_id) references safa_user (user_id) on delete cascade
);