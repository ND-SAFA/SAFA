# Core Entities
INSERT INTO prod.safa_user
SELECT *
FROM dev.safa_user d
where d.user_id not in (select user_id from prod.safa_user);
INSERT INTO prod.project
SELECT *
FROM dev.project d
where d.project_id not in (select project_id from prod.project);
INSERT INTO prod.project_membership
SELECT *
FROM dev.project_membership d
where d.membership_id not in (select membership_id from prod.project_membership);
INSERT INTO prod.project_version
SELECT *
FROM dev.project_version d
where d.version_id not in (select version_id from prod.project_version);
INSERT INTO prod.project_rule
SELECT *
FROM dev.project_rule d
where d.id not in (select id from prod.project_rule);

# Base Project Entities
INSERT INTO prod.artifact_type
SELECT *
FROM dev.artifact_type d
where d.type_id not in (select type_id from prod.artifact_type);
INSERT INTO prod.artifact
SELECT *
FROM dev.artifact d
where d.artifact_id not in (select artifact_id from prod.artifact);
INSERT INTO prod.trace_link
SELECT *
FROM dev.trace_link d
where d.trace_link_id not in (select trace_link_id from prod.trace_link);

# Version entities
INSERT INTO prod.artifact_body
SELECT *
FROM dev.artifact_body d
where d.entity_version_id not in (select entity_version_id from prod.artifact_body);
INSERT INTO prod.trace_link_version
SELECT *
FROM dev.trace_link_version d
where d.trace_link_version_id not in (select trace_link_version_id from prod.trace_link_version);
INSERT INTO prod.fta_artifact
SELECT *
FROM dev.fta_artifact d
where d.fta_artifact_id not in (select fta_artifact_id from prod.fta_artifact);
INSERT INTO prod.safety_case_artifact
SELECT *
FROM dev.safety_case_artifact d
where d.safety_case_artifact_id not in (select safety_case_artifact_id from prod.safety_case_artifact);

# Flat Files
INSERT INTO prod.artifact_file
SELECT *
FROM dev.artifact_file d
where d.file_id not in (select file_id from prod.artifact_file);
INSERT INTO prod.trace_matrix
SELECT *
FROM dev.trace_matrix d
where d.trace_matrix_id not in (select trace_matrix_id from prod.trace_matrix);

# Auxilary base entities
INSERT INTO prod.commit_error
SELECT *
FROM dev.commit_error d
where d.id not in (select id from prod.commit_error);
-- INSERT INTO prod.job SELECT * FROM dev.job;

# Jira Entities
INSERT INTO prod.jira_access_credentials
SELECT *
FROM dev.jira_access_credentials d
where d.artifact_id not in (select artifact_id from prod.jira_access_credentials);
INSERT INTO prod.jira_project
SELECT *
FROM dev.jira_project d
where d.mapping_id not in (select mapping_id from prod.jira_project);

# GitHub Entities
INSERT INTO prod.github_access_credentials
SELECT *
FROM dev.github_access_credentials d
where d.artifact_id not in (select artifact_id from prod.github_access_credentials);
INSERT INTO prod.github_project
SELECT *
FROM dev.github_project d
where d.mapping_id not in (select mapping_id from prod.github_project);


# Document entities
INSERT INTO prod.document
SELECT *
FROM dev.document d
where d.document_id not in (select document_id from prod.document);
INSERT INTO prod.current_document
SELECT *
FROM dev.current_document d
where d.id not in (select id from prod.current_document);
INSERT INTO prod.document_artifact
SELECT *
FROM dev.document_artifact d
where d.document_artifact_id not in (select document_artifact_id from prod.document_artifact);
INSERT INTO prod.document_column
SELECT *
FROM dev.document_column d
where d.document_column_id not in (select document_column_id from prod.document_column);

# Layout
INSERT INTO prod.artifact_position
SELECT *
FROM dev.artifact_position d
where d.id not in (select id from prod.artifact_position);



