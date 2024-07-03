CREATE TABLE IF NOT EXISTS audit_log
(
    id          BINARY(16)   NOT NULL PRIMARY KEY,
    entry       MEDIUMTEXT   NOT NULL,
    time        DATETIME(6)  NOT NULL,
    user_id     VARCHAR(255),
    user_email  VARCHAR(255) NOT NULL,
    CONSTRAINT audit_log_user_id_fk FOREIGN KEY (user_id) REFERENCES safa_user (user_id) ON DELETE SET NULL
);
