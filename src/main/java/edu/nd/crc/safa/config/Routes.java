package edu.nd.crc.safa.config;

public class Routes {
    // SAFA User Controller
    public static final String createAccountLink = "/accounts/create";
    public static final String loginLink = "/login";

    // Artifact Controller
    public static final String createArtifact = "/projects/versions/{versionId}/artifacts";
    public static final String deleteArtifact = "/projects/versions/{versionId}/artifacts/{artifactName}";
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
    public static final String approveLinkById = "/projects/links/{traceLinkId}/approve";
    public static final String declineLinkById = "/projects/links/{traceLinkId}/decline";
    public static final String createNewLink = "/projects/versions/{versionId}/links/create/{sourceId}/{targetId}";

    // Version Controller
    public static final String getVersions = "/projects/{projectId}/versions";
    public static final String getVersionById = "/projects/versions/{versionId}";
    public static final String getCurrentVersion = "/projects/{projectId}/versions/current";
    public static final String createNewMajorVersion = "/projects/{projectId}/versions/major";
    public static final String createNewMinorVersion = "/projects/{projectId}/versions/minor";
    public static final String createNewRevisionVersion = "/projects/{projectId}/versions/revision";
}
