create table artifact
(
    artifact_id   varchar(255) not null,
    document_type varchar(255),
    name          varchar(255),
    project_id    varchar(255) not null,
    type_id       varchar(255) not null,
    primary key (artifact_id)
);
create table artifact_body
(
    entity_version_id varchar(255) not null,
    content           TEXT         not null,
    custom_fields     TEXT,
    modification_type integer      not null,
    summary           varchar(255) not null,
    artifact_id       varchar(255) not null,
    version_id        varchar(255) not null,
    primary key (entity_version_id)
);
create table artifact_file
(
    file_id    varchar(255) not null,
    file_name  varchar(255) not null,
    type_id    varchar(255) not null,
    project_id varchar(255) not null,
    primary key (file_id)
);
create table artifact_type
(
    type_id    varchar(255) not null,
    icon       varchar(255) not null,
    name       varchar(255) not null,
    project_id varchar(255) not null,
    primary key (type_id)
);
create table commit_error
(
    id          varchar(255) not null,
    activity    integer,
    description varchar(500),
    file_name   varchar(255),
    line_number bigint,
    version_id  varchar(255) not null,
    primary key (id)
);
create table current_document
(
    id          varchar(255) not null,
    document_id varchar(255) not null,
    user_id     varchar(255) not null,
    primary key (id)
);
create table document
(
    document_id   varchar(255) not null,
    description   varchar(255),
    name          varchar(255),
    document_type varchar(255) not null,
    project_id    varchar(255) not null,
    primary key (document_id)
);
create table document_artifact
(
    document_artifact_id varchar(255) not null,
    artifact_id          varchar(255) not null,
    document_id          varchar(255) not null,
    version_id           varchar(255) not null,
    primary key (document_artifact_id)
);
create table document_column
(
    document_column_id varchar(255) not null,
    data_type          varchar(255) not null,
    name               varchar(255) not null,
    required           bit          not null,
    table_column_index integer      not null,
    document_id        varchar(255) not null,
    primary key (document_column_id)
);
create table fta_artifact
(
    fta_artifact_id varchar(255) not null,
    logic_type      integer,
    artifact_id     varchar(255) not null,
    primary key (fta_artifact_id)
);
create table jira_access_credentials
(
    artifact_id         varchar(255) not null,
    bearer_access_token BLOB,
    client_id           varchar(32),
    client_secret       varchar(64),
    cloud_id            varchar(64),
    refresh_token       varchar(128),
    version             smallint,
    user_id             varchar(255) not null,
    primary key (artifact_id)
);
create table jira_project
(
    mapping_id      varchar(255) not null,
    jira_project_id bigint       not null,
    safa_project_id varchar(255) not null,
    primary key (mapping_id)
);
create table job
(
    id                  varchar(255) not null,
    completed_at        datetime(6),
    completed_entity_id binary(255),
    current_progress    integer      not null,
    current_step        integer      not null,
    job_type            integer      not null,
    last_updated_at     datetime(6)  not null,
    name                varchar(255) not null,
    started_at          datetime(6)  not null,
    status              integer      not null,
    user_id             varchar(255) not null,
    primary key (id)
);
create table project
(
    project_id  varchar(255) not null,
    description varchar(255) not null,
    name        varchar(255) not null,
    primary key (project_id)
);
create table project_membership
(
    membership_id varchar(255) not null,
    project_role  varchar(255),
    user_id       varchar(255) not null,
    project_id    varchar(255) not null,
    primary key (membership_id)
);
create table project_rule
(
    id          varchar(255) not null,
    description varchar(255),
    name        varchar(255),
    rule        varchar(255),
    project_id  varchar(255) not null,
    primary key (id)
);
create table project_version
(
    version_id    varchar(255) not null,
    major_version integer      not null,
    minor_version integer      not null,
    revision      integer      not null,
    project_id    varchar(255) not null,
    primary key (version_id)
);
create table safa_user
(
    user_id  varchar(255) not null,
    email    varchar(255) not null,
    password varchar(255) not null,
    primary key (user_id)
);
create table safety_case_artifact
(
    safety_case_artifact_id varchar(255) not null,
    safety_case_type        integer,
    artifact_id             varchar(255) not null,
    primary key (safety_case_artifact_id)
);
create table trace_link
(
    trace_link_id      varchar(255) not null,
    source_artifact_id varchar(255) not null,
    target_artifact_id varchar(255) not null,
    primary key (trace_link_id)
);
create table trace_link_version
(
    trace_link_version_id varchar(255) not null,
    approval_status       integer,
    modification_type     integer      not null,
    score                 double precision,
    trace_type            integer      not null,
    version_id            varchar(255) not null,
    trace_link_id         varchar(255) not null,
    primary key (trace_link_version_id)
);
create table trace_matrix
(
    trace_matrix_id varchar(255) not null,
    project_id      varchar(255) not null,
    source_type_id  varchar(255) not null,
    target_type_id  varchar(255) not null,
    primary key (trace_matrix_id)
);
alter table artifact
    add constraint UNIQUE_ARTIFACT_NAME_PER_PROJECT unique (project_id, name);
alter table artifact_body
    add constraint UNIQUE_ARTIFACT_BODY_PER_VERSION unique (artifact_id, version_id);
alter table artifact_type
    add constraint UNIQUE_ARTIFACT_TYPE_PER_PROJECT unique (project_id, name);
alter table current_document
    add constraint SINGLE_DEFAULT_DOCUMENT_PER_USER unique (user_id);
alter table document_artifact
    add constraint UNIQUE_ARTIFACT_PER_DOCUMENT unique (document_id, artifact_id);
alter table fta_artifact
    add constraint UK_94vhfnmgqhp8bihv4pdxeneyw unique (artifact_id);
alter table jira_project
    add constraint UK_1itvanuxcvv0971w3ngwi6wtw unique (jira_project_id);
alter table jira_project
    add constraint UK_oc6tvvmtlieaafr5cfx7c5mlc unique (safa_project_id);
alter table project_membership
    add constraint SINGLE_ROLE_PER_PROJECT unique (project_id, user_id);
alter table project_rule
    add constraint UK_6x2u31xd76hdwpc24qnv94p8n unique (project_id);
alter table project_version
    add constraint UNIQUE_VERSION_ID_PER_PROJECT unique (project_id, major_version, minor_version, revision);
alter table safa_user
    add constraint UK_bbj3a5mc1mp25iokuv86ylavc unique (email);
alter table safety_case_artifact
    add constraint UK_kaq12rb2mfpitx0w56af4mmgb unique (artifact_id);
alter table trace_link
    add constraint SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET unique (source_artifact_id, target_artifact_id);
alter table trace_link_version
    add constraint SINGLE_TRACE_VERSION_PER_PROJECT_VERSION unique (version_id, trace_link_id);
alter table trace_matrix
    add constraint UNIQUE_TRACE_MATRIX_PER_PROJECT unique (project_id, source_type_id, target_type_id);
alter table artifact
    add constraint FKqi7jpmsvst8h67mvp18lrkdol foreign key (project_id) references project (project_id) on delete cascade;
alter table artifact
    add constraint FKmm9u2cvnnr5va4cf0rtwdxpum foreign key (type_id) references artifact_type (type_id) on delete cascade;
alter table artifact_body
    add constraint FK96iykarnp5i4sfipafelb6aun foreign key (artifact_id) references artifact (artifact_id) on delete cascade;
alter table artifact_body
    add constraint FK8theajq5bt7dgh40h2wv7qrva foreign key (version_id) references project_version (version_id) on delete cascade;
alter table artifact_file
    add constraint FKn9s4qdf27so9w43lp67b7y6ru foreign key (type_id) references artifact_type (type_id) on delete cascade;
alter table artifact_file
    add constraint FKl1wcjfqjrujiyqoti0u50n70j foreign key (project_id) references project (project_id) on delete cascade;
alter table artifact_type
    add constraint FKkix0u3hbft5ylkx8esamuiear foreign key (project_id) references project (project_id) on delete cascade;
alter table commit_error
    add constraint FKi77is2jvt3q3kno7pwp6funy2 foreign key (version_id) references project_version (version_id) on delete cascade;
alter table current_document
    add constraint FKl9kiq2qk3hhw40fxmqmqodqiq foreign key (document_id) references document (document_id) on delete cascade;
alter table current_document
    add constraint FKddqxs77x11ma35eu7ifjgqijk foreign key (user_id) references safa_user (user_id) on delete cascade;
alter table document
    add constraint FKebvohyx0uckt4eb2cpiqiciba foreign key (project_id) references project (project_id) on delete cascade;
alter table document_artifact
    add constraint FKsvx425s29krqit2e81ike7vv2 foreign key (artifact_id) references artifact (artifact_id) on delete cascade;
alter table document_artifact
    add constraint FKfcvhwahys89ubu2sqiirlyh7w foreign key (document_id) references document (document_id) on delete cascade;
alter table document_artifact
    add constraint FKluluxrrg6mu59ofemh8rnn7ea foreign key (version_id) references project_version (version_id) on delete cascade;
alter table document_column
    add constraint FKcgjv6jki0idifdlb1xb6c3cfh foreign key (document_id) references document (document_id) on delete cascade;
alter table fta_artifact
    add constraint FK8ijfwkbqinm492ifvpcog8oga foreign key (artifact_id) references artifact (artifact_id) on delete cascade;
alter table jira_access_credentials
    add constraint FK5vyycewe6gmlb43bwah2kqo36 foreign key (user_id) references safa_user (user_id) on delete cascade;
alter table jira_project
    add constraint FK3ij4h33i9axnwk9qto6kvsfws foreign key (safa_project_id) references project (project_id) on delete cascade;
alter table job
    add constraint FK2ht8oy9wpktierop39tyeqa1i foreign key (user_id) references safa_user (user_id) on delete cascade;
alter table project_membership
    add constraint FK62xirmb10rpi857wdn4a51dit foreign key (user_id) references safa_user (user_id) on delete cascade;
alter table project_membership
    add constraint FK6nerxrll628ug1mvgpt2spgpk foreign key (project_id) references project (project_id) on delete cascade;
alter table project_rule
    add constraint FK9vjvvwmwgukcvvakqcdpep6yx foreign key (project_id) references project (project_id) on delete cascade;
alter table project_version
    add constraint FK5r3lhwoo0bphctbeckcv009si foreign key (project_id) references project (project_id) on delete cascade;
alter table safety_case_artifact
    add constraint FKadg3wb9i26ekegrtpms0kmwdg foreign key (artifact_id) references artifact (artifact_id) on delete cascade;
alter table trace_link
    add constraint FKme8gxiuxljaxhw6pffdfq4s8r foreign key (source_artifact_id) references artifact (artifact_id) on delete cascade;
alter table trace_link
    add constraint FK9m5jqvqus8xydedrqnyybtrnt foreign key (target_artifact_id) references artifact (artifact_id) on delete cascade;
alter table trace_link_version
    add constraint FKsc2el1f9m95j05stacmo2ekm9 foreign key (version_id) references project_version (version_id) on delete cascade;
alter table trace_link_version
    add constraint FK9sl2vswo07cd5qo8m3bpv2r4c foreign key (trace_link_id) references trace_link (trace_link_id) on delete cascade;
alter table trace_matrix
    add constraint FKn86rl38xiq1w7t6m0fa04d04k foreign key (project_id) references project (project_id) on delete cascade;
alter table trace_matrix
    add constraint FKq45awb99p2vpytx8d1a7i1apu foreign key (source_type_id) references artifact_type (type_id) on delete cascade;
alter table trace_matrix
    add constraint FKardwxr379hvy9gpqd98hc2m0 foreign key (target_type_id) references artifact_type (type_id) on delete cascade;
