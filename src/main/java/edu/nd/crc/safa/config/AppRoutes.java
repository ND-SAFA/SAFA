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

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Accounts {
        public static final String LOGIN = "/login";
        public static final String LOGOUT = "/logout";
        protected static final String PREFIX = "/accounts";
        public static final String CHANGE_PASSWORD = Accounts.PREFIX + "/change";
        public static final String RESET_PASSWORD = Accounts.PREFIX + "/reset";
        public static final String FORGOT_PASSWORD = Accounts.PREFIX + "/forgot";
        public static final String FORGOT_PASSWORD_NO_EMAIL = Accounts.PREFIX + "/forgot/no-email";
        public static final String CREATE_ACCOUNT = Accounts.PREFIX + "/create";
        public static final String CREATE_VERIFIED_ACCOUNT = Accounts.PREFIX + "/create-verified";
        public static final String VERIFY_ACCOUNT = Accounts.PREFIX + "/verify";
        public static final String DELETE_ACCOUNT = Accounts.PREFIX + "/delete";
        public static final String SELF = Accounts.PREFIX + "/self";
        public static final String DEFAULT_ORG = Accounts.PREFIX + "/organization";

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class SuperUser {
            public static final String ROOT = Accounts.PREFIX + "/superuser";
            public static final String ACTIVATE = ROOT + "/activate";
            public static final String DEACTIVATE = ROOT + "/deactivate";
        }
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class ArtifactType {
        public static final String GET_PROJECT_ARTIFACT_TYPES = Projects.ROOT + "/{projectId}/artifactTypes";
        public static final String CREATE_ARTIFACT_TYPE = GET_PROJECT_ARTIFACT_TYPES;
        public static final String UPDATE_ARTIFACT_TYPE = GET_PROJECT_ARTIFACT_TYPES + "/{artifactType}";
        public static final String DELETE_ARTIFACT_TYPE = Projects.ROOT + "/artifactTypes/{typeId}";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Attribute {
        public static final String ROOT = Projects.BY_ID + "/attributes";
        public static final String BY_KEY = ROOT + "/{key}";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class AttributeLayout {
        public static final String ROOT = Projects.BY_ID + "/attribute-layouts";
        public static final String BY_ID = ROOT + "/{id}";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Comments {
        public static final String COMMENT_CREATE = "/comments/artifact/{artifactId}";
        public static final String COMMENT_GET = "/comments/artifact/{artifactId}";
        public static final String COMMENT_RESOLVE = "/comments/{commentId}/resolve";
        private static final String BY_ID = "/comments/{commentId}";
        public static final String COMMENT_UPDATE_CONTENT = BY_ID + "/content";
        public static final String COMMENT_DELETE = BY_ID;
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Commits {
        public static final String COMMIT_CHANGE = Projects.ROOT + "/versions/{versionId}/commit";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Chat {
        private static final String ROOT = "/chats";
        public static final String CHAT_GET = ROOT + "/projects/{projectId}";
        public static final String CHAT_CREATE = ROOT;
        private static final String BY_ID = ROOT + "/{chatId}";
        public static final String CHAT_UPDATE = BY_ID;
        public static final String CHAT_DELETE = BY_ID;
        public static final String CHAT_TITLE = BY_ID + "/title";

        public static class Message {
            public static final String MESSAGE_SEND = BY_ID + "/messages";
            public static final String MESSAGE_GET = BY_ID + "/messages";
        }
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Delta {
        public static final String CALCULATE_PROJECT_DELTA = Projects.ROOT
            + "/delta/{baselineVersionId}/{targetVersionId}";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
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

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class DocumentArtifact {
        public static final String ADD_ARTIFACTS_TO_DOCUMENT = Projects.ROOT + "/versions/{versionId}/documents"
            + "/{documentId}/artifacts";
        public static final String REMOVE_ARTIFACT_FROM_DOCUMENT = ADD_ARTIFACTS_TO_DOCUMENT + "/{artifactId}";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class FlatFiles {
        public static final String UPDATE_PROJECT_VERSION_FROM_FLAT_FILES = Projects.ROOT
            + "/versions/{versionId}/flat-files";
        public static final String DOWNLOAD_FLAT_FILES = UPDATE_PROJECT_VERSION_FROM_FLAT_FILES + "/{fileType}";
        public static final String PARSE_ARTIFACT_FILE = Projects.ROOT + "/parse/artifacts/{artifactType}";
        public static final String PARSE_TRACE_FILE = Projects.ROOT + "/parse/traces";

    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class HGen {
        public static final String GENERATE = "/hgen/{versionId}";
        public static final String ESTIMATE = GENERATE + "/estimate";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Models {
        public static final String MODEL_ROOT = "/models";
        public static final String MODEL_ROOT_BY_ID = Projects.BY_ID + MODEL_ROOT;
        public static final String MODEL_BY_PROJECT_AND_ID = Models.MODEL_ROOT_BY_ID + "/{modelId}";
        public static final String DELETE_MODEL_BY_ID = MODEL_BY_PROJECT_AND_ID;
        public static final String SHARE_MODEL = Projects.ROOT + "/models/share";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Links {
        public static final String GET_GENERATED_LINKS_IN_PROJECT_VERSION = Projects.ROOT
            + "/versions/{versionId}/links/generated";
        public static final String GENERATE_LINKS = Projects.ROOT + "/links/generate";
        public static final String ADD_BATCH = GET_GENERATED_LINKS_IN_PROJECT_VERSION + "/add-batch";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Jobs {
        protected static final String JOBS_PREFIX = "/jobs";

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Traces {
            public static final String GENERATE = JOBS_PREFIX + Links.GENERATE_LINKS;
        }

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Projects {
            public static final String PROJECT_JOBS_ROOT = JOBS_PREFIX + AppRoutes.Projects.ROOT;
            public static final String CREATE_PROJECT_VIA_JSON = PROJECT_JOBS_ROOT;
            public static final String PROJECT_BULK_UPLOAD = PROJECT_JOBS_ROOT + "/upload";
            public static final String UPDATE_PROJECT_VIA_FLAT_FILES = PROJECT_JOBS_ROOT + "/versions/{versionId}";
        }

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Meta {
            public static final String GET_USER_JOBS = JOBS_PREFIX + "/user";
            public static final String GET_PROJECT_JOBS = JOBS_PREFIX + "/project/{projectId}";
            private static final String JOB_ID = JOBS_PREFIX + "/{jobId}";
            public static final String DELETE_JOB = JOB_ID;
        }

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Models {
            public static final String TRAIN = JOBS_PREFIX + AppRoutes.Projects.BY_ID + "/models/train";
        }

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Logs {
            public static final String BY_JOB_ID = Meta.JOB_ID + "/logs";
            public static final String BY_JOB_ID_AND_STEP_NUM = BY_JOB_ID + "/{stepNum}";
        }
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Prompts {
        public static final String COMPLETE = "/prompt";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Health {
        public static final String GENERATE = "/health/versions/{versionId}";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Projects {
        protected static final String ROOT = "/projects";
        public static final String BY_ID = ROOT + "/{projectId}";
        public static final String TRANSFER_OWNERSHIP = BY_ID + "/transfer";
        public static final String GET_PROJECTS = ROOT;
        public static final String DELETE_PROJECT_BY_ID = ROOT + "/{projectId}";
        public static final String CREATE_OR_UPDATE_PROJECT_META = ROOT;

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Membership {
            public static final String GET_USER_PROJECTS = ROOT;
            public static final String GET_TEAM_PROJECTS = ROOT + "/team/{teamId}";
        }

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Entities {
            public static final String CHECK_IF_ARTIFACT_EXISTS = ROOT
                + "/versions/{versionId}/artifacts/validate";
        }

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Installations {
            public static final String BY_PROJECT = Projects.ROOT + "/installations/by-project/{id}";
        }
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Rules {
        public static final String CREATE_WARNING_IN_PROJECT = "/project/{projectId}/rules";
        public static final String GET_WARNINGS_IN_PROJECT_VERSION = Projects.ROOT
            + "/versions/{versionId}/warnings";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class TraceMatrix {
        public static final String BASE = Projects.ROOT + "/{projectVersionId}/matrices";
        public static final String BY_SOURCE_AND_TARGET_TYPES = BASE + "/{sourceTypeName}/{targetTypeName}";
        public static final String BY_ID = BASE + "/{traceMatrixId}";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Jira {

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Credentials {
            public static final String ROOT = Accounts.PREFIX + "/jira/credentials";
            public static final String REGISTER = Credentials.ROOT + "/{accessCode}";
            public static final String REFRESH = Credentials.ROOT;
            public static final String DELETE = Credentials.ROOT;
            public static final String VALIDATE = Credentials.ROOT + "/validate";
        }

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Installations {
            public static final String ROOT = Accounts.PREFIX + "/jira/installations";
            public static final String RETRIEVE_AVAILABLE = Installations.ROOT;
        }

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Import {
            public static final String ROOT = Projects.ROOT + "/import";
            public static final String BY_ID = Import.ROOT + "/jira/{orgId}/{id}";
            public static final String UPDATE = Versions.BY_ID + "/import/jira/{orgId}/{id}";
            public static final String RETRIEVE_JIRA_PROJECTS = Projects.ROOT + "/jira/{orgId}";
            public static final String IMPORT_INTO_EXISTING = Versions.BY_ID + "/import/jira/{orgId}/{id}";
        }
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Github {

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Credentials {
            public static final String REGISTER = Accounts.PREFIX + "/github/credentials/{accessCode}";
            public static final String DELETE = Accounts.PREFIX + "/github/credentials";
            public static final String VALID = Accounts.PREFIX + "/github/credentials/check";
        }

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Import {
            public static final String UPDATE = Versions.BY_ID + "/import/github/{owner}/{repositoryName}";
            public static final String IMPORT_INTO_EXISTING = UPDATE;
            private static final String ROOT = Projects.ROOT + "/import";
            public static final String BY_NAME = Import.ROOT + "/github/{owner}/{repositoryName}";
        }
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Versions {
        public static final String GET_VERSIONS = Projects.ROOT + "/{projectId}/versions";
        public static final String BY_ID = Projects.ROOT + "/versions/{versionId}";
        public static final String GET_CURRENT_VERSION = Projects.ROOT + "/{projectId}/versions/current";
        public static final String CREATE_NEW_MAJOR_VERSION = Projects.ROOT + "/{projectId}/versions/major";
        public static final String CREATE_NEW_MINOR_VERSION = Projects.ROOT + "/{projectId}/versions/minor";
        public static final String CREATE_NEW_REVISION_VERSION = Projects.ROOT + "/{projectId}/versions/revision";
        public static final String DELETE_VERSION_BY_ID = Versions.BY_ID;
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Retrieval {
        public static final String GET_PROJECT_IN_VERSION = Versions.BY_ID;
        public static final String GET_TRACES_IN_VERSION = Versions.BY_ID + "/traces";
        public static final String GET_ARTIFACTS_IN_VERSION = Versions.BY_ID + "/artifacts";
        public static final String GET_ARTIFACT_IDS_IN_VERSION = Versions.BY_ID + "/artifacts/query";

    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Sync {
        public static final String GET_CHANGES = Versions.BY_ID + "/changes";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Search {
        public static final String SEARCH = "/search/{versionId}";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Summarize {
        public static final String SUMMARIZE_ARTIFACTS = Projects.ROOT + "/versions/{versionId}/artifacts/summarize";
        public static final String SUMMARIZE_PROJECT = Projects.ROOT + "/versions/{versionId}/summarize";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Layout {
        public static final String REGENERATE_LAYOUT = Versions.BY_ID + "/layout";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Integrations {
        public static final String ROOT = "/integrations";

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Github {
            public static final String ROOT = Integrations.ROOT + "/github";

            @NoArgsConstructor(access = AccessLevel.NONE)
            public static class Repos {
                public static final String ROOT = Github.ROOT + "/repos";
                public static final String BY_OWNER_AND_NAME = ROOT + "/{owner}/{repositoryName}";
            }
        }
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Organizations {
        public static final String ROOT = "/organizations";
        public static final String BY_ID = ROOT + "/{orgId}";
        public static final String SELF = ROOT + "/self";

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Teams {
            public static final String ROOT = Organizations.BY_ID + "/teams";
            public static final String BY_ID = ROOT + "/{teamId}";
            public static final String SELF = ROOT + "/self";
        }
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Memberships {
        public static final String ROOT = "/members";
        public static final String BY_ENTITY_ID = ROOT + "/{entityId}";
        public static final String BY_ENTITY_ID_AND_MEMBERSHIP_ID = BY_ENTITY_ID + "/{membershipId}";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Billing {
        public static final String ROOT = "/billing";
        public static final String CHECKOUT = ROOT + "/checkout";
        public static final String CHANGE_TIER = ROOT + "/update-payment-tier";

        @NoArgsConstructor(access = AccessLevel.NONE)
        public static class Transaction {
            public static final String ROOT = Billing.ROOT + "/transactions";
            public static final String BY_ORG = ROOT + "/{orgId}";
            public static final String BY_ORG_MONTHLY = BY_ORG + "/month";
            public static final String MONTHLY = ROOT + "/month";
        }
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Stripe {
        public static final String ROOT = "/stripe";
        public static final String WEBHOOK = ROOT + "/webhook";
        public static final String CANCEL = ROOT + "/cancel/{sessionId}";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Onboarding {
        public static final String ROOT = "/onboarding";
    }

    @NoArgsConstructor(access = AccessLevel.NONE)
    public static class Statistics {
        public static final String ROOT = "/statistics";
        public static final String ONBOARDING_ROOT = ROOT + "/onboarding";
        public static final String ONBOARDING_BY_USER = ONBOARDING_ROOT + "/{userId}";
    }
}
