ALTER TABLE jira_access_credentials
    DROP COLUMN cloud_id;

ALTER TABLE jira_access_credentials
    DROP COLUMN client_id;

ALTER TABLE jira_access_credentials
    DROP COLUMN client_secret;

ALTER TABLE github_access_credentials
    DROP COLUMN client_id;

ALTER TABLE github_access_credentials
    DROP COLUMN client_secret;