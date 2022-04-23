package edu.nd.crc.safa.config;

/**
 * The container centralizing all route names used within controllers and testing.
 * See usages of class RouteBuilder within tests for example of how to construct paths.
 */
public class AppRoutes {
    public static class Accounts {
        public static final String loginLink = "/login";
        private static final String accountPrefix = "/accounts";
        public static final String createNewUser = accountPrefix + "/create";
    }

    public static class Jobs {
        private static final String jobRoot = "/jobs";
        public static final String createNewJob = jobRoot;
        private static final String jobId = jobRoot + "/{jobId}";
        public static final String getJobStatus = jobId + "/status";
        public static final String deleteJob = jobId;
        public static final String getJobResult = jobId + "/result";
    }

    public static class Projects {
        private static final String projectPrefix = "/projects";
        public static final String deleteProjectById = projectPrefix + "/{projectId}";
        public static final String createOrUpdateProjects = projectPrefix;
        public static final String getProjects = projectPrefix;

        public static class Import {
            public static final String importPrefix = projectPrefix + "/import";
            public static final String pullJiraProject = importPrefix + "/jira";
        }

        public static class Membership {
            public static final String addProjectMember = projectPrefix + "/{projectId}/members";
            public static final String getProjectMembers = projectPrefix + "/{projectId}/members";
            public static final String deleteProjectMembership = projectPrefix + "/members/{projectMembershipId}";
            public static final String getUserProjects = projectPrefix;
        }

        public static class Documents {
            public static final String createOrUpdateDocument = projectPrefix + "/versions/{versionId}/documents";
            public static final String getProjectDocuments = projectPrefix + "/{projectId}/documents";
            public static final String deleteDocument = projectPrefix + "/documents/{documentId}";
        }

        public static class DocumentArtifact {
            public static final String addArtifactsToDocument = projectPrefix + "/versions/{versionId}/documents"
                + "/{documentId}/artifacts";
            public static final String removeArtifactFromDocument = addArtifactsToDocument + "/{artifactId}";
        }

        public static class Links {
            public static final String getGeneratedLinksInProjectVersion = projectPrefix
                + "/versions/{versionId}/links/generated";
            public static final String generateLinks = projectPrefix + "/links/generate";
        }

        public static class Versions {
            public static final String getVersions = projectPrefix + "/{projectId}/versions";
            public static final String getCurrentVersion = projectPrefix + "/{projectId}/versions/current";
            public static final String createNewMajorVersion = projectPrefix + "/{projectId}/versions/major";
            public static final String createNewMinorVersion = projectPrefix + "/{projectId}/versions/minor";
            public static final String createNewRevisionVersion = projectPrefix + "/{projectId}/versions/revision";
        }

        public static class Entities {
            public static final String checkIfArtifactExists = projectPrefix
                + "/versions/{versionId}/artifacts/validate/{artifactName}";
            public static final String getProjectInVersion = projectPrefix + "/versions/{versionId}";
            public static final String getArtifactsInProjectVersion = getProjectInVersion + "/artifacts";
            public static final String getTracesInVersion = getProjectInVersion + "/traces";
            public static final String deleteVersionById = getProjectInVersion;
        }

        public static class Delta {
            public static final String calculateProjectDelta = projectPrefix
                + "/delta/{baselineVersionId}/{targetVersionId}";
        }

        public static class Commits {
            public static final String commitChange = projectPrefix + "/versions/{versionId}/commit";
        }

        public static class FlatFiles {
            public static final String updateProjectVersionFromFlatFiles = projectPrefix
                + "/versions/{versionId}/flat-files";
            public static final String projectFlatFiles = projectPrefix + "/flat-files";
            public static final String parseArtifactFile = projectPrefix + "/parse/artifacts/{artifactType}";
            public static final String parseTraceFile = projectPrefix + "/parse/traces";

        }

        public static class TraceMatrix {
            public static final String getTraceMatrices = projectPrefix + "/{projectId}/matrices";
            public static final String createTraceMatrix = projectPrefix + "/{projectId}/matrices/"
                + "{sourceArtifactTypeName}/{targetArtifactTypeName}";
            public static final String deleteTraceMatrix = projectPrefix + "/{projectId}/matrices/"
                + "{sourceArtifactTypeName}/{targetArtifactTypeName}";
        }

        public static class ArtifactType {
            public static final String getProjectArtifactTypes = projectPrefix + "/{projectId}/artifactTypes";
            public static final String createOrUpdateArtifactType = getProjectArtifactTypes;
            public static final String deleteArtifactType = projectPrefix + "/artifactTypes/{typeId}";
        }

        public static class Warnings {
            public static final String getWarningsInProjectVersion = projectPrefix + "/versions/{versionId}/warnings";
        }
    }
}
