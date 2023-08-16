ALTER TABLE project ADD COLUMN team_id BINARY(16) NOT NULL;

CREATE TEMPORARY TABLE project_teams AS
    SELECT project.project_id, team.id, user_project_membership.membership_id
        FROM project
        INNER JOIN user_project_membership on project.project_id = user_project_membership.project_id
        INNER JOIN safa_user on user_project_membership.user_id = safa_user.user_id
        INNER JOIN organization on safa_user.personal_org_id = organization.id
        INNER JOIN team on organization.full_org_team_id = team.id
    WHERE user_project_membership.project_role = 'OWNER';

UPDATE project SET team_id =
    (
        SELECT project_teams.id FROM project_teams
            WHERE project_teams.project_id = project.project_id
            LIMIT 1
    );

DELETE FROM user_project_membership
    WHERE user_project_membership.membership_id IN
    (
        SELECT project_teams.membership_id
            FROM project_teams
            INNER JOIN project on project.project_id = project_teams.project_id
            WHERE project_teams.id = project.team_id
    );

DROP TABLE project_teams;