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

    public static class Projects {
        private static final String projectPrefix = "/projects";
        public static final String deleteProjectById = projectPrefix + "/{projectId}";
        public static final String addProjectMember = projectPrefix + "/{projectId}/members";
        public static final String getProjectMembers = projectPrefix + "/{projectId}/members";
        public static final String deleteProjectMembership = projectPrefix + "/members/{projectMembershipId}";

        // Project Controller
        public static final String createOrUpdateProjects = projectPrefix;
        public static final String getUserProjects = projectPrefix;

        // Document Controller
        public static final String createOrUpdateDocument = projectPrefix + "/{projectId}/documents";
        public static final String getProjectDocuments = projectPrefix + "/{projectId}/documents";
        public static final String deleteDocument = projectPrefix + "/documents/{documentId}";

        // Document Artifact Controller
        public static final String addArtifactsToDocument = projectPrefix + "/versions/{versionId}/documents"
            + "/{documentId}/artifacts";
        public static final String removeArtifactFromDocument = addArtifactsToDocument + "/{artifactId}";

        // Trace Link Controller
        public static final String getGeneratedLinksInProjectVersion = projectPrefix
            + "/versions/{versionId}/links/generated";
        public static final String generateLinks = projectPrefix + "/links/generate";

        // Retrieval of versioned entities
        public static final String getProjectInVersion = projectPrefix + "/versions/{versionId}";
        public static final String getArtifactsInVersion = getProjectInVersion + "/artifacts";
        public static final String getTracesInVersion = getProjectInVersion + "/traces";
        public static final String deleteVersionById = getProjectInVersion;

        // Version Controller
        public static final String getVersions = projectPrefix + "/{projectId}/versions";
        public static final String getCurrentVersion = projectPrefix + "/{projectId}/versions/current";
        public static final String createNewMajorVersion = projectPrefix + "/{projectId}/versions/major";
        public static final String createNewMinorVersion = projectPrefix + "/{projectId}/versions/minor";
        public static final String createNewRevisionVersion = projectPrefix + "/{projectId}/versions/revision";

        //Change Controller
        public static final String commitChange = projectPrefix + "/versions/{versionId}/commit";

        // Artifact Controller
        public static final String checkIfArtifactExists = projectPrefix
            + "/versions/{versionId}/artifacts/validate/{artifactName}";
        public static final String calculateProjectDelta = projectPrefix
            + "/delta/{baselineVersionId}/{targetVersionId}";

        // Flat file Controller
        public static final String updateProjectVersionFromFlatFiles = projectPrefix
            + "/versions/{versionId}/flat-files";
        public static final String projectFlatFiles = projectPrefix + "/flat-files";

        // Parse Data File controller
        public static final String parseArtifactFile = projectPrefix + "/parse/artifacts/{artifactType}";
        public static final String parseTraceFile = projectPrefix + "/parse/traces";

        // Trace Matrix Controller
        public static final String getTraceMatrices = projectPrefix + "/{projectId}/matrices";
        public static final String createTraceMatrix = projectPrefix + "/{projectId}/matrices/"
            + "{sourceArtifactTypeName}/{targetArtifactTypeName}";
        public static final String deleteTraceMatrix = projectPrefix + "/{projectId}/matrices/"
            + "{sourceArtifactTypeName}/{targetArtifactTypeName}";
    }
}
