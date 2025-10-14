ALTER TABLE jira_access_credentials MODIFY COLUMN refresh_token mediumtext;
ALTER TABLE project MODIFY COLUMN description mediumtext NOT NULL;
