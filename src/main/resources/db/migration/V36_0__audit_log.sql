CREATE TABLE IF NOT EXISTS audit_log
(
    id          BINARY(16)   NOT NULL PRIMARY KEY,
    entry       mediumtext   NOT NULL,
    time        DATETIME(6)  NOT NULL,
    user_id     VARCHAR(255) NOT NULL,
    constraint audit_log_user_id_fk foreign key (user_id) references safa_user (user_id)
);
