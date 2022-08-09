package edu.nd.crc.safa.config;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

/**
 * The container centralizing all route names used within controllers and testing.
 * See usages of class RouteBuilder within tests for example of how to construct paths.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class AppRoutes {
    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Accounts {
        public static final String LOGIN = "/login";
        private static final String ACCOUNTS_PREFIX = "/accounts";
        public static final String CREATE_ACCOUNT = ACCOUNTS_PREFIX + "/create";
        public static final String JIRA_CREDENTIALS = ACCOUNTS_PREFIX + "/jira/credentials";
        public static final String JIRA_CREDENTIALS_REFRESH = ACCOUNTS_PREFIX + "/jira/credentials/{cloudId}";
        public static final String JIRA_CREDENTIALS_VALIDATE = ACCOUNTS_PREFIX + "/jira/credentials/validate";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Jobs {
        private static final String JOBS_PREFIX = "/jobs";
        public static final String FLAT_FILE_PROJECT_UPDATE_JOB = JOBS_PREFIX + "/projects/versions/{versionId}";
        public static final String GET_JOBS = JOBS_PREFIX;
        private static final String JOB_ID = JOBS_PREFIX + "/{jobId}";
        public static final String DELETE_JOB = JOB_ID;
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Projects {
        private static final String PROJECT_PREFIX = "/projects";
        public static final String RETRIEVE_JIRA_PROJECTS = PROJECT_PREFIX + "/jira/{cloudId}";
        public static final String DELETE_PROJECT_BY_ID = PROJECT_PREFIX + "/{projectId}";
        public static final String CREATE_OR_UPDATE_PROJECT_META = PROJECT_PREFIX;
        public static final String GET_PROJECTS = PROJECT_PREFIX;

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Import {
            public static final String IMPORT_PREFIX = PROJECT_PREFIX + "/import";
            public static final String PULL_JIRA_PROJECT = IMPORT_PREFIX + "/jira/{cloudId}/{id}";
        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Membership {
            public static final String ADD_PROJECT_MEMBER = PROJECT_PREFIX + "/{projectId}/members";
            public static final String GET_PROJECT_MEMBERS = PROJECT_PREFIX + "/{projectId}/members";
            public static final String DELETE_PROJECT_MEMBERSHIP = PROJECT_PREFIX + "/members/{projectMembershipId}";
            public static final String GET_USER_PROJECTS = PROJECT_PREFIX;
        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Documents {
            public static final String CREATE_OR_UPDATE_DOCUMENT = PROJECT_PREFIX + "/versions/{versionId}/documents";
            public static final String GET_PROJECT_DOCUMENTS = PROJECT_PREFIX + "/{projectId}/documents";
            public static final String DELETE_DOCUMENT = PROJECT_PREFIX + "/documents/{documentId}";
            public static final String SET_CURRENT_DOCUMENT = PROJECT_PREFIX + "/documents/current/{documentId}";
            public static final String CLEAR_CURRENT_DOCUMENT = PROJECT_PREFIX + "/documents/current";
        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class DocumentArtifact {
            public static final String ADD_ARTIFACTS_TO_DOCUMENT = PROJECT_PREFIX + "/versions/{versionId}/documents"
                + "/{documentId}/artifacts";
            public static final String REMOVE_ARTIFACT_FROM_DOCUMENT = ADD_ARTIFACTS_TO_DOCUMENT + "/{artifactId}";
        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Links {
            public static final String GET_GENERATED_LINKS_IN_PROJECT_VERSION = PROJECT_PREFIX
                + "/versions/{versionId}/links/generated";
            public static final String GENERATE_LINKS = PROJECT_PREFIX + "/links/generate";
        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Versions {
            public static final String GET_VERSIONS = PROJECT_PREFIX + "/{projectId}/versions";
            public static final String GET_CURRENT_VERSION = PROJECT_PREFIX + "/{projectId}/versions/current";
            public static final String CREATE_NEW_MAJOR_VERSION = PROJECT_PREFIX + "/{projectId}/versions/major";
            public static final String CREATE_NEW_MINOR_VERSION = PROJECT_PREFIX + "/{projectId}/versions/minor";
            public static final String CREATE_NEW_REVISION_VERSION = PROJECT_PREFIX + "/{projectId}/versions/revision";
        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Entities {
            public static final String CHECK_IF_ARTIFACT_EXISTS = PROJECT_PREFIX
                + "/versions/{versionId}/artifacts/validate/{artifactName}";
            public static final String GET_PROJECT_IN_VERSION = PROJECT_PREFIX + "/versions/{versionId}";
            public static final String GET_ARTIFACTS_IN_PROJECT_VERSION = GET_PROJECT_IN_VERSION + "/artifacts";
            public static final String GET_TRACES_IN_VERSION = GET_PROJECT_IN_VERSION + "/traces";
            public static final String DELETE_VERSION_BY_ID = GET_PROJECT_IN_VERSION;
        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Delta {
            public static final String CALCULATE_PROJECT_DELTA = PROJECT_PREFIX
                + "/delta/{baselineVersionId}/{targetVersionId}";
        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Commits {
            public static final String COMMIT_CHANGE = PROJECT_PREFIX + "/versions/{versionId}/commit";
        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class FlatFiles {
            public static final String UPDATE_PROJECT_VERSION_FROM_FLAT_FILES = PROJECT_PREFIX
                + "/versions/{versionId}/flat-files";
            public static final String DOWNLOAD_FLAT_FILES = UPDATE_PROJECT_VERSION_FROM_FLAT_FILES + "/{fileType}";
            public static final String CREATE_PROJECT_FROM_FLAT_FILES = PROJECT_PREFIX + "/flat-files";
            public static final String PARSE_ARTIFACT_FILE = PROJECT_PREFIX + "/parse/artifacts/{artifactType}";
            public static final String PARSE_TRACE_FILE = PROJECT_PREFIX + "/parse/traces";

        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class TraceMatrix {
            public static final String GET_TRACE_MATRICES = PROJECT_PREFIX + "/{projectId}/matrices";
            public static final String CREATE_TRACE_MATRIX = PROJECT_PREFIX + "/{projectId}/matrices/"
                + "{sourceArtifactTypeName}/{targetArtifactTypeName}";
            public static final String DELETE_TRACE_MATRIX = PROJECT_PREFIX + "/{projectId}/matrices/"
                + "{sourceArtifactTypeName}/{targetArtifactTypeName}";
        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class ArtifactType {
            public static final String GET_PROJECT_ARTIFACT_TYPES = PROJECT_PREFIX + "/{projectId}/artifactTypes";
            public static final String CREATE_OR_UPDATE_ARTIFACT_TYPE = GET_PROJECT_ARTIFACT_TYPES;
            public static final String DELETE_ARTIFACT_TYPE = PROJECT_PREFIX + "/artifactTypes/{typeId}";
        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Rules {
            public static final String CREATE_WARNING_IN_PROJECT = "/project/{projectId}/rules";
            public static final String GET_WARNINGS_IN_PROJECT_VERSION = PROJECT_PREFIX
                + "/versions/{versionId}/warnings";
        }
    }
}
