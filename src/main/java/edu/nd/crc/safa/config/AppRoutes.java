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
        public static final String projectById = projectPrefix + "/{projectId}";
        public static final String addProjectMember = projectPrefix + "/{projectId}/members";
        public static final String getProjectMembers = projectPrefix + "/{projectId}/members";
        public static final String deleteProjectMembership = projectPrefix + "/members/{projectMembershipId}";

        // Project Controller
        public static final String projects = projectPrefix;

        // Trace Link Controller
        public static final String getGeneratedLinksInProjectVersion = projectPrefix
            + "/versions/{versionId}/links/generated";
        public static final String generateLinks = projectPrefix + "/links/generate";

        // Version Controller
        public static final String getVersions = projectPrefix + "/{projectId}/versions";
        public static final String getVersionById = projectPrefix + "/versions/{versionId}";
        public static final String getCurrentVersion = projectPrefix + "/{projectId}/versions/current";
        public static final String createNewMajorVersion = projectPrefix + "/{projectId}/versions/major";
        public static final String createNewMinorVersion = projectPrefix + "/{projectId}/versions/minor";
        public static final String createNewRevisionVersion = projectPrefix + "/{projectId}/versions/revision";

        //Change Controller
        public static final String commitChange = projectPrefix + "/versions/{versionId}/commit";

        // Artifact Controller
        public static final String checkIfArtifactExists = projectPrefix
            + "/{projectId}/artifacts/validate/{artifactName}";
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
