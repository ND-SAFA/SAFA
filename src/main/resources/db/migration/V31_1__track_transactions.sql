CREATE TABLE IF NOT EXISTS billing_info
(
    id                 BINARY(16)  NOT NULL PRIMARY KEY,
    balance            INT         NOT NULL DEFAULT 0,
    total_used         INT         NOT NULL DEFAULT 0,
    total_successful   INT         NOT NULL DEFAULT 0,
    organization_id    BINARY(16)  NOT NULL,
    version            BIGINT      NOT NULL DEFAULT 0,
    CONSTRAINT billing_info_org_id_fk FOREIGN KEY (organization_id) REFERENCES organization (id) ON DELETE CASCADE,
    CONSTRAINT billing_info_org_id_unique UNIQUE (organization_id)
);

INSERT INTO billing_info (id, organization_id)
SELECT (SELECT ${uuid_generator}), org.id
FROM organization org;



CREATE TABLE IF NOT EXISTS transaction
(
    id               BINARY(16)     NOT NULL PRIMARY KEY,
    status           VARCHAR(255)   NOT NULL,
    amount           INT            NOT NULL,
    description      VARCHAR(1024)  NOT NULL,
    timestamp        DATETIME       NOT NULL,
    organization_id  BINARY(16)     NOT NULL,
    CONSTRAINT transaction_org_id_fk FOREIGN KEY (organization_id) REFERENCES organization (id) ON DELETE CASCADE
);