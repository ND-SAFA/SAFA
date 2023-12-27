/*
 * Create personal organizations
 */

INSERT INTO organization (name, description, owner_id, personal_org, full_org_team_id, payment_tier, id)
SELECT email, '', user_id, TRUE, '', 'free', (SELECT ${uuid_generator})
FROM safa_user;

/*
 * Record personal orgs in safa_user table
 */
ALTER TABLE safa_user
    ADD COLUMN personal_org_id BINARY(16) DEFAULT NULL;

CREATE TEMPORARY TABLE user_orgs AS
SELECT o.id, su.user_id
FROM organization o
         INNER JOIN safa_user su on o.owner_id = su.user_id
WHERE o.personal_org = TRUE;

UPDATE safa_user
SET safa_user.personal_org_id =
        (SELECT user_orgs.id
         FROM user_orgs
         WHERE safa_user.user_id = user_orgs.user_id);

DROP TABLE user_orgs;

/*
 * Create teams for all organizations
 */
INSERT INTO team (name, organization_id, full_org_team, id)
SELECT name, id, TRUE, (SELECT ${uuid_generator})
FROM organization;

/*
 * Record full org teams in organization table
 */
CREATE TEMPORARY TABLE org_teams AS
SELECT t.id team_id, o.id org_id
FROM team t
         INNER JOIN organization o on t.organization_id = o.id
WHERE t.full_org_team = TRUE;

UPDATE organization
SET organization.full_org_team_id =
        (SELECT org_teams.team_id
         FROM org_teams
         WHERE org_teams.org_id = organization.id);

DROP TABLE org_teams;

/*
 * Add users to their teams
 */
INSERT INTO team_membership (user_id, team_id, role, id)
SELECT safa_user.user_id, team.id, 'ADMIN', (SELECT ${uuid_generator})
FROM team
         INNER JOIN organization on team.organization_id = organization.id
         INNER JOIN safa_user on organization.owner_id = safa_user.user_id;
