ALTER TABLE jira_project
    ADD last_update datetime NULL DEFAULT NOW();

ALTER TABLE jira_project
    MODIFY last_update datetime NOT NULL;
