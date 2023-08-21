CREATE TABLE IF NOT EXISTS org_membership
(
    id                 BINARY(16)   NOT NULL PRIMARY KEY,
    user_id            VARCHAR(255) NOT NULL,
    org_id             BINARY(16)   NOT NULL,
    role               VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES safa_user (user_id) ON DELETE CASCADE,
    FOREIGN KEY (org_id) REFERENCES organization (id) ON DELETE CASCADE
);