
/*
    Wipe jira_project table since without the org ID, you can't use the project IDs anyway
*/
DELETE FROM jira_project;

ALTER TABLE jira_project
    ADD org_id BINARY(16) NOT NULL;