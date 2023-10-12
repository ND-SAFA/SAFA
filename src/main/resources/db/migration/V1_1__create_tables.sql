create table if not exists safa_user
(
    user_id  varchar(255) not null,
    email    varchar(255) not null,
    password varchar(255) not null,
    primary key (user_id),
    constraint UNIQUE_EMAIL unique (email)
);
create table if not exists project
(
    project_id  varchar(255) not null,
    description varchar(255) not null,
    name        varchar(255) not null,
    primary key (project_id)
);
create table if not exists project_version
(
    version_id    varchar(255) not null,
    major_version integer      not null,
    minor_version integer      not null,
    revision      integer      not null,
    project_id    varchar(255) not null,
    primary key (version_id),
    constraint UNIQUE_VERSION_ID_PER_PROJECT unique (project_id, major_version, minor_version, revision),
    foreign key (project_id) references project (project_id) on delete cascade
);
create table if not exists artifact_type
(
    type_id    varchar(255) not null,
    icon       varchar(255) not null,
    name       varchar(255) not null,
    project_id varchar(255) not null,
    primary key (type_id),
    constraint UNIQUE_ARTIFACT_TYPE_PER_PROJECT unique (project_id, name),
    foreign key (project_id) references project (project_id) on delete cascade
);

create table if not exists artifact
(
    artifact_id   varchar(255) not null,
    document_type varchar(255),
    name          varchar(255),
    project_id    varchar(255) not null,
    type_id       varchar(255) not null,
    primary key (artifact_id),
    constraint UNIQUE_ARTIFACT_NAME_PER_PROJECT unique (project_id, name),
    foreign key (project_id) references project (project_id) on delete cascade,
    foreign key (type_id) references artifact_type (type_id) on delete cascade
);
create table if not exists artifact_body
(
    entity_version_id varchar(255) not null,
    content           TEXT         not null,
    custom_fields     TEXT,
    modification_type integer      not null,
    summary           varchar(255) not null,
    artifact_id       varchar(255) not null,
    version_id        varchar(255) not null,
    primary key (entity_version_id),
    constraint UNIQUE_ARTIFACT_BODY_PER_VERSION unique (artifact_id, version_id),
    foreign key (artifact_id) references artifact (artifact_id) on delete cascade,
    foreign key (version_id) references project_version (version_id) on delete cascade
);
create table if not exists artifact_file
(
    file_id    varchar(255) not null,
    file_name  varchar(255) not null,
    type_id    varchar(255) not null,
    project_id varchar(255) not null,
    primary key (file_id),
    foreign key (type_id) references artifact_type (type_id) on delete cascade,
    foreign key (project_id) references project (project_id) on delete cascade
);

create table if not exists commit_error
(
    id          varchar(255) not null,
    activity    integer,
    description varchar(500),
    file_name   varchar(255),
    line_number bigint,
    version_id  varchar(255) not null,
    primary key (id),
    foreign key (version_id) references project_version (version_id) on delete cascade
);

create table if not exists document
(
    document_id   varchar(255) not null,
    description   varchar(255),
    name          varchar(255),
    document_type varchar(255) not null,
    project_id    varchar(255) not null,
    primary key (document_id),
    foreign key (project_id) references project (project_id) on delete cascade
);
create table if not exists current_document
(
    id          varchar(255) not null,
    document_id varchar(255) not null,
    user_id     varchar(255) not null,
    primary key (id),
    constraint SINGLE_DEFAULT_DOCUMENT_PER_USER unique (user_id),
    foreign key (document_id) references document (document_id) on delete cascade,
    foreign key (user_id) references safa_user (user_id) on delete cascade
);
create table if not exists document_artifact
(
    document_artifact_id varchar(255) not null,
    artifact_id          varchar(255) not null,
    document_id          varchar(255) not null,
    version_id           varchar(255) not null,
    primary key (document_artifact_id),
    constraint UNIQUE_ARTIFACT_PER_DOCUMENT unique (document_id, artifact_id),
    foreign key (artifact_id) references artifact (artifact_id) on delete cascade,
    foreign key (document_id) references document (document_id) on delete cascade,
    foreign key (version_id) references project_version (version_id) on delete cascade
);
create table if not exists document_column
(
    document_column_id varchar(255) not null,
    data_type          varchar(255) not null,
    name               varchar(255) not null,
    required           bit          not null,
    table_column_index integer      not null,
    document_id        varchar(255) not null,
    primary key (document_column_id),
    foreign key (document_id) references document (document_id) on delete cascade
);
create table if not exists fta_artifact
(
    fta_artifact_id varchar(255) not null,
    logic_type      integer,
    artifact_id     varchar(255) not null unique,
    primary key (fta_artifact_id),
    constraint UNIQUE_ARTIFACT_PARENT_PER_FTA_ARTIFACT unique (artifact_id),
    foreign key (artifact_id) references artifact (artifact_id) on delete cascade

);
create table if not exists jira_access_credentials
(
    artifact_id         varchar(255) not null,
    bearer_access_token BLOB,
    client_id           varchar(32),
    client_secret       varchar(64),
    cloud_id            varchar(64),
    refresh_token       varchar(128),
    version             smallint,
    user_id             varchar(255) not null,
    primary key (artifact_id),
    foreign key (user_id) references safa_user (user_id) on delete cascade
);
create table if not exists jira_project
(
    mapping_id      varchar(255) not null,
    jira_project_id bigint       not null,
    safa_project_id varchar(255) not null,
    primary key (mapping_id),
    foreign key (safa_project_id) references project (project_id) on delete cascade
);
create table if not exists job
(
    id                  varchar(255) not null,
    completed_at        datetime(6),
    completed_entity_id varchar(255),
    current_progress    integer      not null,
    current_step        integer      not null,
    job_type            integer      not null,
    last_updated_at     datetime(6)  not null,
    name                varchar(255) not null,
    started_at          datetime(6)  not null,
    status              integer      not null,
    user_id             varchar(255) not null,
    primary key (id),
    foreign key (user_id) references safa_user (user_id) on delete cascade
);

create table if not exists project_membership
(
    membership_id varchar(255) not null,
    project_role  varchar(255),
    user_id       varchar(255) not null,
    project_id    varchar(255) not null,
    primary key (membership_id),
    constraint SINGLE_ROLE_PER_PROJECT unique (project_id, user_id),
    constraint user_project_membership_ibfk_1 foreign key (user_id) references safa_user (user_id) on delete cascade,
    constraint user_project_membership_ibfk_2 foreign key (project_id) references project (project_id) on delete cascade
);
create table if not exists project_rule
(
    id          varchar(255) not null,
    description varchar(255),
    name        varchar(255),
    rule        varchar(255),
    project_id  varchar(255) not null,
    primary key (id),
    foreign key (project_id) references project (project_id) on delete cascade
);


create table if not exists safety_case_artifact
(
    safety_case_artifact_id varchar(255) not null,
    safety_case_type        integer,
    artifact_id             varchar(255) not null,
    primary key (safety_case_artifact_id),
    constraint UNIQUE_ARTIFACT_PARENT_PER_SAFETY_ARTIFACT unique (artifact_id),
    foreign key (artifact_id) references artifact (artifact_id) on delete cascade
);
create table if not exists trace_link
(
    trace_link_id      varchar(255) not null,
    source_artifact_id varchar(255) not null,
    target_artifact_id varchar(255) not null,
    primary key (trace_link_id),
    constraint SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET unique (source_artifact_id, target_artifact_id),
    foreign key (source_artifact_id) references artifact (artifact_id) on delete cascade,
    foreign key (target_artifact_id) references artifact (artifact_id) on delete cascade
);
create table if not exists trace_link_version
(
    trace_link_version_id varchar(255) not null,
    approval_status       integer,
    modification_type     integer      not null,
    score                 double precision,
    trace_type            integer      not null,
    version_id            varchar(255) not null,
    trace_link_id         varchar(255) not null,
    primary key (trace_link_version_id),
    constraint SINGLE_TRACE_VERSION_PER_PROJECT_VERSION unique (version_id, trace_link_id),
    foreign key (version_id) references project_version (version_id) on delete cascade,
    foreign key (trace_link_id) references trace_link (trace_link_id) on delete cascade
);
create table if not exists trace_matrix
(
    trace_matrix_id varchar(255) not null,
    project_id      varchar(255) not null,
    source_type_id  varchar(255) not null,
    target_type_id  varchar(255) not null,
    primary key (trace_matrix_id),
    constraint UNIQUE_TRACE_MATRIX_PER_PROJECT unique (project_id, source_type_id, target_type_id),
    foreign key (project_id) references project (project_id) on delete cascade,
    foreign key (source_type_id) references artifact_type (type_id) on delete cascade,
    foreign key (target_type_id) references artifact_type (type_id) on delete cascade
);
