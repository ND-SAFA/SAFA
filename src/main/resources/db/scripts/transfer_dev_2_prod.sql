# Core Entities
INSERT INTO prod.safa_user
SELECT *
FROM dev.safa_user;
INSERT INTO prod.project
SELECT *
FROM dev.project;
INSERT INTO prod.project_membership
SELECT *
FROM dev.project_membership;
INSERT INTO prod.project_version
SELECT *
FROM dev.project_version;
INSERT INTO prod.project_rule
SELECT *
FROM dev.project_rule;

# Base Project Entities
INSERT INTO prod.artifact_type
SELECT *
FROM dev.artifact_type;
INSERT INTO prod.artifact
SELECT *
FROM dev.artifact;
INSERT INTO prod.trace_link
SELECT *
FROM dev.trace_link;

# Version entities
INSERT INTO prod.artifact_body
SELECT *
FROM dev.artifact_body;
INSERT INTO prod.trace_link_version
SELECT *
FROM dev.trace_link_version;
INSERT INTO prod.fta_artifact
SELECT *
FROM dev.fta_artifact;
INSERT INTO prod.safety_case_artifact
SELECT *
FROM dev.safety_case_artifact;

# Flat Files
INSERT INTO prod.artifact_file
SELECT *
FROM dev.artifact_file;
INSERT INTO prod.trace_matrix
SELECT *
FROM dev.trace_matrix;

# Auxilary base entities
INSERT INTO prod.commit_error
SELECT *
FROM dev.commit_error;
INSERT INTO prod.job
SELECT *
FROM dev.job;

# Jira Entities
INSERT INTO prod.jira_access_credentials
SELECT *
FROM dev.jira_access_credentials;
INSERT INTO prod.jira_project
SELECT *
FROM dev.jira_project;

# Document entities
-- INSERT INTO prod.document SELECT * FROM dev.document;
INSERT INTO prod.current_document
SELECT *
FROM dev.current_document;
INSERT INTO prod.document_artifact
SELECT *
FROM dev.document_artifact;
INSERT INTO prod.document_column
SELECT *
FROM dev.document_column;





