CREATE TABLE IF NOT EXISTS password_reset_token
(
    id              VARCHAR(36)  NOT NULL PRIMARY KEY,
    user_id         VARCHAR(36)  NOT NULL UNIQUE,
    token           VARCHAR(255) NOT NULL,
    expiration_date datetime     NOT NULL,
    FOREIGN KEY (user_id) REFERENCES safa_user (user_id)
);
