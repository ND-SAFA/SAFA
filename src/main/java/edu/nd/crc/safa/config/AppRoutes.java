package edu.nd.crc.safa.config;

import java.util.Arrays;
import java.util.List;

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

    public static String createPath(List<String> paths) {
        return String.join("/", paths);
    }

    public static String createPathWithPrefix(String prefix, String... args) {
        List<String> argList = Arrays.asList(args);
        argList.add(0, prefix);
        return createPath(argList);
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Accounts {
        public static final String LOGIN = "/login";
        protected static final String PREFIX = "/accounts";
        public static final String CREATE_ACCOUNT = path(Accounts.PREFIX, "create");
        public static final String DELETE_ACCOUNT = path(PREFIX, "delete");
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Layout {
        protected static final String PREFIX = "/layout";
        public static final String GET_DOCUMENT_LAYOUT = Versions.BY_ID + Documents.BY_ID + Layout.PREFIX;
        public static final String GET_PROJECT_LAYOUT = Projects.BY_ID + Layout.PREFIX;
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Jobs {
        protected static final String JOBS_PREFIX = "/jobs";
        public static final String FLAT_FILE_PROJECT_UPDATE_JOB = JOBS_PREFIX + "/projects/versions/{versionId}";
        public static final String GET_JOBS = JOBS_PREFIX;
        public static final String JSON_PROJECT_JOB = JOBS_PREFIX + Projects.PREFIX;
        private static final String JOB_ID = JOBS_PREFIX + "/{jobId}";
        public static final String DELETE_JOB = JOB_ID;
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Projects {
        protected static final String PREFIX = "/projects";
        public static final String BY_ID = PREFIX + "/{projectId}";
        public static final String DELETE_PROJECT_BY_ID = PREFIX + "/{projectId}";
        public static final String CREATE_OR_UPDATE_PROJECT_META = PREFIX;
        public static final String GET_PROJECTS = PREFIX;

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Membership {
            public static final String ADD_PROJECT_MEMBER = PREFIX + "/{projectId}/members";
            public static final String GET_PROJECT_MEMBERS = PREFIX + "/{projectId}/members";
            public static final String DELETE_PROJECT_MEMBERSHIP = PREFIX + "/members/{projectMembershipId}";
            public static final String GET_USER_PROJECTS = PREFIX;
        }

        @NoArgsConstructor(access = AccessLevel.PRIVATE)
        public static class Entities {
            public static final String CHECK_IF_ARTIFACT_EXISTS = PREFIX
                + "/versions/{versionId}/artifacts/validate";
            public static final String GET_PROJECT_IN_VERSION = PREFIX + "/versions/{versionId}";
            public static final String GET_ARTIFACTS_IN_PROJECT_VERSION = GET_PROJECT_IN_VERSION + "/artifacts";
            public static final String GET_TRACES_IN_VERSION = GET_PROJECT_IN_VERSION + "/traces";
        }

    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class ArtifactType {
        public static final String GET_PROJECT_ARTIFACT_TYPES = Projects.PREFIX + "/{projectId}/artifactTypes";
        public static final String CREATE_OR_UPDATE_ARTIFACT_TYPE = GET_PROJECT_ARTIFACT_TYPES;
        public static final String DELETE_ARTIFACT_TYPE = Projects.PREFIX + "/artifactTypes/{typeId}";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Commits {
        public static final String COMMIT_CHANGE = Projects.PREFIX + "/versions/{versionId}/commit";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Delta {
        public static final String CALCULATE_PROJECT_DELTA = Projects.PREFIX
            + "/delta/{baselineVersionId}/{targetVersionId}";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Documents {
        public static final String GET_PROJECT_DOCUMENTS = Projects.PREFIX + "/{projectId}/documents";
        protected static final String PREFIX = "/documents";
        public static final String CREATE_OR_UPDATE_DOCUMENT = Versions.BY_ID + Documents.PREFIX;
        public static final String GET_DOCUMENT_BY_ID = Projects.PREFIX + Documents.PREFIX + "/{documentId}";
        public static final String DELETE_DOCUMENT = Projects.PREFIX + Documents.PREFIX + "/{documentId}";
        public static final String SET_CURRENT_DOCUMENT = Projects.PREFIX + Documents.PREFIX + "/current/{documentId}";
        public static final String CLEAR_CURRENT_DOCUMENT = Projects.PREFIX + Documents.PREFIX + "/current";
        protected static final String BY_ID = PREFIX + "/{documentId}";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class DocumentArtifact {
        public static final String ADD_ARTIFACTS_TO_DOCUMENT = Projects.PREFIX + "/versions/{versionId}/documents"
            + "/{documentId}/artifacts";
        public static final String REMOVE_ARTIFACT_FROM_DOCUMENT = ADD_ARTIFACTS_TO_DOCUMENT + "/{artifactId}";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Rules {
        public static final String CREATE_WARNING_IN_PROJECT = "/project/{projectId}/rules";
        public static final String GET_WARNINGS_IN_PROJECT_VERSION = Projects.PREFIX
            + "/versions/{versionId}/warnings";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class FlatFiles {
        public static final String UPDATE_PROJECT_VERSION_FROM_FLAT_FILES = Projects.PREFIX
            + "/versions/{versionId}/flat-files";
        public static final String DOWNLOAD_FLAT_FILES = UPDATE_PROJECT_VERSION_FROM_FLAT_FILES + "/{fileType}";
        public static final String CREATE_NEW_PROJECT_FROM_FLAT_FILES = Projects.PREFIX + "/flat-files";
        public static final String PARSE_ARTIFACT_FILE = Projects.PREFIX + "/parse/artifacts/{artifactType}";
        public static final String PARSE_TRACE_FILE = Projects.PREFIX + "/parse/traces";

    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class TraceMatrix {
        public static final String GET_TRACE_MATRICES = Projects.PREFIX + "/{projectId}/matrices";
        public static final String CREATE_TRACE_MATRIX = Projects.PREFIX + "/{projectId}/matrices/"
            + "{sourceArtifactTypeName}/{targetArtifactTypeName}";
        public static final String DELETE_TRACE_MATRIX = Projects.PREFIX + "/{projectId}/matrices/"
            + "{sourceArtifactTypeName}/{targetArtifactTypeName}";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Jira {
        public static final String JIRA_CREDENTIALS = Accounts.PREFIX + "/jira/credentials";
        public static final String JIRA_CREDENTIALS_REFRESH = Accounts.PREFIX + "/jira/credentials/{cloudId}";
        public static final String JIRA_CREDENTIALS_VALIDATE = Accounts.PREFIX + "/jira/credentials/validate";
        public static final String RETRIEVE_JIRA_PROJECTS = Projects.PREFIX + "/jira/{cloudId}";
        public static final String IMPORT_PREFIX = Projects.PREFIX + "/import";
        public static final String CREATE_PROJECT_FROM_JIRA = IMPORT_PREFIX + "/jira/{cloudId}/{id}";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Links {
        public static final String GET_GENERATED_LINKS_IN_PROJECT_VERSION = Projects.PREFIX
            + "/versions/{versionId}/links/generated";
        public static final String GENERATE_LINKS = Projects.PREFIX + "/links/generate";
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    public static class Versions {
        public static final String GET_VERSIONS = Projects.PREFIX + "/{projectId}/versions";
        public static final String BY_ID = Projects.PREFIX + "/versions/{versionId}";
        public static final String GET_CURRENT_VERSION = Projects.PREFIX + "/{projectId}/versions/current";
        public static final String CREATE_NEW_MAJOR_VERSION = Projects.PREFIX + "/{projectId}/versions/major";
        public static final String CREATE_NEW_MINOR_VERSION = Projects.PREFIX + "/{projectId}/versions/minor";
        public static final String CREATE_NEW_REVISION_VERSION = Projects.PREFIX + "/{projectId}/versions/revision";
        public static final String DELETE_VERSION_BY_ID = Projects.Entities.GET_PROJECT_IN_VERSION;
    }
}
