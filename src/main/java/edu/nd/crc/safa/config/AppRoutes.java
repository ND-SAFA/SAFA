package edu.nd.crc.safa.config;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

/**
 * The container centralizing all route names used within controllers and testing.
 * See usages of class RouteBuilder within tests for example of how to construct paths.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class AppRoutes {

    public static String path(String... args) {
        return String.join("/", args);
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Accounts {
        public static final String LOGIN = "/login";
        protected static final String PREFIX = "/accounts";
        public static final String CHANGE_PASSWORD = Accounts.PREFIX + "/change";
        public static final String RESET_PASSWORD = Accounts.PREFIX + "/reset";
        public static final String FORGOT_PASSWORD = Accounts.PREFIX + "/forgot";
        public static final String CREATE_ACCOUNT = Accounts.PREFIX + "/create";
        public static final String DELETE_ACCOUNT = Accounts.PREFIX + "/delete";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Jobs {
        protected static final String JOBS_PREFIX = "/jobs";

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Projects {
            public static final String CREATE_PROJECT_VIA_JSON = JOBS_PREFIX + AppRoutes.Projects.ROOT;
            public static final String UPDATE_PROJECT_VIA_FLAT_FILES = JOBS_PREFIX + "/projects/versions/{versionId}";
        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Meta {
            public static final String GET_JOBS = JOBS_PREFIX;
            private static final String JOB_ID = JOBS_PREFIX + "/{jobId}";
            public static final String DELETE_JOB = JOB_ID;
        }
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Projects {
        protected static final String ROOT = "/projects";
        public static final String BY_ID = ROOT + "/{projectId}";
        public static final String DELETE_PROJECT_BY_ID = ROOT + "/{projectId}";
        public static final String CREATE_OR_UPDATE_PROJECT_META = ROOT;
        public static final String GET_PROJECTS = ROOT;

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Membership {
            public static final String ADD_PROJECT_MEMBER = ROOT + "/{projectId}/members";
            public static final String GET_PROJECT_MEMBERS = ROOT + "/{projectId}/members";
            public static final String DELETE_PROJECT_MEMBERSHIP = ROOT + "/members/{projectMembershipId}";
            public static final String GET_USER_PROJECTS = ROOT;
        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Entities {
            public static final String CHECK_IF_ARTIFACT_EXISTS = ROOT
                + "/versions/{versionId}/artifacts/validate";
        }

    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class ArtifactType {
        public static final String GET_PROJECT_ARTIFACT_TYPES = Projects.ROOT + "/{projectId}/artifactTypes";
        public static final String CREATE_OR_UPDATE_ARTIFACT_TYPE = GET_PROJECT_ARTIFACT_TYPES;
        public static final String DELETE_ARTIFACT_TYPE = Projects.ROOT + "/artifactTypes/{typeId}";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Commits {
        public static final String COMMIT_CHANGE = Projects.ROOT + "/versions/{versionId}/commit";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Delta {
        public static final String CALCULATE_PROJECT_DELTA = Projects.ROOT
            + "/delta/{baselineVersionId}/{targetVersionId}";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Documents {
        public static final String GET_PROJECT_DOCUMENTS = Versions.BY_ID + "/documents";
        protected static final String ROOT = "/documents";
        public static final String CREATE_OR_UPDATE_DOCUMENT = Versions.BY_ID + Documents.ROOT;
        public static final String SET_CURRENT_DOCUMENT = Projects.ROOT + Documents.ROOT + "/current/{documentId}";
        public static final String CLEAR_CURRENT_DOCUMENT = Projects.ROOT + Documents.ROOT + "/current";
        protected static final String BY_ID = ROOT + "/{documentId}";
        public static final String GET_DOCUMENT_BY_ID = Versions.BY_ID + Documents.BY_ID;
        public static final String DELETE_DOCUMENT_BY_ID = Projects.ROOT + Documents.BY_ID;
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class DocumentArtifact {
        public static final String ADD_ARTIFACTS_TO_DOCUMENT = Projects.ROOT + "/versions/{versionId}/documents"
            + "/{documentId}/artifacts";
        public static final String REMOVE_ARTIFACT_FROM_DOCUMENT = ADD_ARTIFACTS_TO_DOCUMENT + "/{artifactId}";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Rules {
        public static final String CREATE_WARNING_IN_PROJECT = "/project/{projectId}/rules";
        public static final String GET_WARNINGS_IN_PROJECT_VERSION = Projects.ROOT
            + "/versions/{versionId}/warnings";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class FlatFiles {
        public static final String UPDATE_PROJECT_VERSION_FROM_FLAT_FILES = Projects.ROOT
            + "/versions/{versionId}/flat-files";
        public static final String DOWNLOAD_FLAT_FILES = UPDATE_PROJECT_VERSION_FROM_FLAT_FILES + "/{fileType}";
        public static final String CREATE_NEW_PROJECT_FROM_FLAT_FILES = Projects.ROOT + "/flat-files";
        public static final String PARSE_ARTIFACT_FILE = Projects.ROOT + "/parse/artifacts/{artifactType}";
        public static final String PARSE_TRACE_FILE = Projects.ROOT + "/parse/traces";

    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class TraceMatrix {
        public static final String GET_TRACE_MATRICES = Projects.ROOT + "/{projectId}/matrices";
        public static final String CREATE_TRACE_MATRIX = Projects.ROOT + "/{projectId}/matrices/"
            + "{sourceArtifactTypeName}/{targetArtifactTypeName}";
        public static final String DELETE_TRACE_MATRIX = Projects.ROOT + "/{projectId}/matrices/"
            + "{sourceArtifactTypeName}/{targetArtifactTypeName}";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Jira {
        public static final String RETRIEVE_JIRA_PROJECTS = Projects.ROOT + "/jira/{cloudId}";

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Credentials {
            public static final String ROOT = Accounts.PREFIX + "/jira/credentials";
            public static final String REFRESH = Credentials.ROOT + "/{cloudId}";
            public static final String VALIDATE = Credentials.ROOT + "/validate";

        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Import {
            public static final String ROOT = Projects.ROOT + "/import";
            public static final String BY_ID = Import.ROOT + "/jira/{cloudId}/{id}";
            public static final String UPDATE = Versions.BY_ID + "/import/jira/{cloudId}/{id}";
        }
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Github {
        public static final String RETRIEVE_GITHUB_REPOSITORIES = Projects.ROOT + "/github";

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Credentials {
            public static final String ROOT = Accounts.PREFIX + "/github/credentials";
            public static final String REFRESH = Accounts.PREFIX + "/github/credentials";
        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Import {
            public static final String UPDATE = Versions.BY_ID + "/import/github/{repositoryName}";
            private static final String ROOT = Projects.ROOT + "/import";
            public static final String BY_NAME = Import.ROOT + "/github/{repositoryName}";
        }
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Links {
        public static final String GET_GENERATED_LINKS_IN_PROJECT_VERSION = Projects.ROOT
            + "/versions/{versionId}/links/generated";
        public static final String GENERATE_LINKS = Projects.ROOT + "/links/generate";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Versions {
        public static final String GET_VERSIONS = Projects.ROOT + "/{projectId}/versions";
        public static final String BY_ID = Projects.ROOT + "/versions/{versionId}";
        public static final String GET_CURRENT_VERSION = Projects.ROOT + "/{projectId}/versions/current";
        public static final String CREATE_NEW_MAJOR_VERSION = Projects.ROOT + "/{projectId}/versions/major";
        public static final String CREATE_NEW_MINOR_VERSION = Projects.ROOT + "/{projectId}/versions/minor";
        public static final String CREATE_NEW_REVISION_VERSION = Projects.ROOT + "/{projectId}/versions/revision";
        public static final String DELETE_VERSION_BY_ID = Versions.BY_ID;
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Retrieval {
        public static final String GET_PROJECT_IN_VERSION = Versions.BY_ID;
        public static final String GET_TRACES_IN_VERSION = Versions.BY_ID + "/traces";
        public static final String GET_ARTIFACTS_IN_VERSION = Versions.BY_ID + "/artifacts";
        public static final String GET_ARTIFACT_IDS_IN_VERSION = Versions.BY_ID + "/artifacts/query";

    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Sync {
        public static final String GET_CHANGES = Versions.BY_ID + "/changes";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Layout {
        public static final String REGENERATE_LAYOUT = Versions.BY_ID + "/layout";
    }
}
