package edu.nd.crc.safa.config;

/**
 * The container centralizing all route names used within controllers and testing.
 * See usages of class RouteBuilder within tests for example of how to construct paths.
 */
public class Routes {
    // SAFA User Controller
    public static final String createAccountLink = "/accounts/create";
    public static final String loginLink = "/login";

    //Change Controller
    public static final String commitChange = "/project/versions/{versionId}/commit";

    // Artifact Controller
    public static final String checkIfArtifactExists = "/projects/{projectId}/artifacts/validate/{artifactName}";
    public static final String calculateProjectDelta = "/projects/delta/{baselineVersionId}/{targetVersionId}";

    // Flat file Controller
    public static final String updateProjectVersionFromFlatFiles = "/projects/versions/{versionId}/flat-files";
    public static final String projectFlatFiles = "/projects/flat-files";

    // Parse Data File controller
    public static final String parseArtifactFile = "/projects/parse/artifacts/{artifactType}";
    public static final String parseTraceFile = "/projects/parse/traces";

    // Project Controller
    public static final String projects = "/projects";
    public static final String projectById = "/projects/{projectId}";

    // Trace Link Controller
    public static final String getGeneratedLinks = "/projects/{projectId}/links/generated";
    public static final String generateLinks = "/projects/links/generate";

    // Version Controller
    public static final String getVersions = "/projects/{projectId}/versions";
    public static final String getVersionById = "/projects/versions/{versionId}";
    public static final String getCurrentVersion = "/projects/{projectId}/versions/current";
    public static final String createNewMajorVersion = "/projects/{projectId}/versions/major";
    public static final String createNewMinorVersion = "/projects/{projectId}/versions/minor";
    public static final String createNewRevisionVersion = "/projects/{projectId}/versions/revision";
}
