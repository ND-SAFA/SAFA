CREATE TABLE IF NOT EXISTS organization
(
    id                 BINARY(16)   NOT NULL PRIMARY KEY,
    name               VARCHAR(255) NOT NULL,
    description        MEDIUMTEXT   NOT NULL,
    owner_id           VARCHAR(255) NOT NULL,
    payment_tier       VARCHAR(255) NOT NULL,
    personal_org       BOOLEAN      NOT NULL,
    full_org_team_id   BINARY(16),
    FOREIGN KEY (owner_id) REFERENCES safa_user (user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS team
(
    id                 BINARY(16)   NOT NULL PRIMARY KEY,
    name               VARCHAR(255) NOT NULL,
    organization_id    BINARY(16)   NOT NULL,
    full_org_team      BOOLEAN      NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organization (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS team_membership
(
    id                 BINARY(16)   NOT NULL PRIMARY KEY,
    user_id            VARCHAR(255) NOT NULL,
    team_id            BINARY(16)   NOT NULL,
    role               VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES safa_user (user_id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES team (id) ON DELETE CASCADE
);

ALTER TABLE project_membership RENAME TO user_project_membership;

CREATE TABLE IF NOT EXISTS team_project_membership
(
    id                 BINARY(16)   NOT NULL PRIMARY KEY,
    project_id         VARCHAR(255) NOT NULL,
    team_id            BINARY(16)   NOT NULL,
    FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES team (id) ON DELETE CASCADE
);


