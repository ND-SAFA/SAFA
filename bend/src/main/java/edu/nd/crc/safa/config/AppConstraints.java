package edu.nd.crc.safa.config;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.springframework.dao.DataIntegrityViolationException;

/**
 * The central container of all database constraints defined in project offering
 * translated messages.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class AppConstraints {

    // Projects
    public static final String UNIQUE_VERSION_ID_PER_PROJECT = "UNIQUE_VERSION_ID_PER_PROJECT";

    // Artifacts
    public static final String UNIQUE_ARTIFACT_NAME_PER_PROJECT = "UNIQUE_ARTIFACT_NAME_PER_PROJECT";
    public static final String UNIQUE_ARTIFACT_TYPE_PER_PROJECT = "UNIQUE_ARTIFACT_TYPE_PER_PROJECT";
    public static final String UNIQUE_ARTIFACT_BODY_PER_VERSION = "UNIQUE_ARTIFACT_BODY_PER_VERSION";
    public static final String UNIQUE_KEYNAME_PER_PROJECT = "UNIQUE_KEYNAME_PER_PROJECT";

    // Traces
    public static final String SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET = "SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET";
    public static final String SINGLE_TRACE_VERSION_PER_PROJECT_VERSION = "SINGLE_TRACE_VERSION_PER_PROJECT_VERSION";
    public static final String UNIQUE_TRACE_MATRIX_PER_PROJECT = "UNIQUE_TRACE_MATRIX_PER_PROJECT";

    // Documents
    public static final String UNIQUE_ARTIFACT_PER_DOCUMENT = "UNIQUE_ARTIFACT_PER_DOCUMENT";

    // FTA / Safety Nodes
    public static final String UNIQUE_ARTIFACT_PARENT_PER_FTA_ARTIFACT = "UNIQUE_ARTIFACT_PARENT_PER_FTA_ARTIFACT";
    public static final String UNIQUE_ARTIFACT_PARENT_PER_SAFETY_ARTIFACT =
        "UNIQUE_ARTIFACT_PARENT_PER_SAFETY_ARTIFACT";

    // Safa User
    public static final String UNIQUE_EMAIL = "UNIQUE_EMAIL";

    //Permissions
    public static final String SINGLE_ROLE_PER_PROJECT = "SINGLE_ROLE_PER_PROJECT";
    //Generic
    public static final String NULL_VALUE = "NULL not allowed for column";
    //Documents
    public static final String SINGLE_DEFAULT_DOCUMENT_PER_USER = "SINGLE_DEFAULT_DOCUMENT_PER_USER";
    //Models
    public static final String UNIQUE_MODEL_PROJECT_RECORD = "UNIQUE_MODEL_PROJECT_RECORD";

    protected static final String[] registeredConstraints = new String[]{
        AppConstraints.UNIQUE_VERSION_ID_PER_PROJECT,
        AppConstraints.UNIQUE_ARTIFACT_NAME_PER_PROJECT,
        AppConstraints.UNIQUE_ARTIFACT_TYPE_PER_PROJECT,
        AppConstraints.UNIQUE_ARTIFACT_BODY_PER_VERSION,
        AppConstraints.UNIQUE_KEYNAME_PER_PROJECT,
        AppConstraints.SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET,
        AppConstraints.SINGLE_TRACE_VERSION_PER_PROJECT_VERSION,
        AppConstraints.UNIQUE_TRACE_MATRIX_PER_PROJECT,
        AppConstraints.UNIQUE_ARTIFACT_PER_DOCUMENT,
        AppConstraints.UNIQUE_ARTIFACT_PARENT_PER_FTA_ARTIFACT,
        AppConstraints.UNIQUE_ARTIFACT_PARENT_PER_SAFETY_ARTIFACT,
        AppConstraints.UNIQUE_EMAIL,
        AppConstraints.SINGLE_ROLE_PER_PROJECT,
        AppConstraints.NULL_VALUE,
        AppConstraints.UNIQUE_MODEL_PROJECT_RECORD
    };

    public static String getConstraintError(DataIntegrityViolationException e) {
        String cause = e.getMostSpecificCause().toString();

        for (String constraintId : registeredConstraints) {
            if (cause.contains(constraintId)) {
                return getErrorMessage(constraintId, cause);
            }
        }

        throw e;
    }

    private static String getErrorMessage(String constraintId, String cause) {
        switch (constraintId) {
            case AppConstraints.UNIQUE_ARTIFACT_NAME_PER_PROJECT:
                return "artifact with given name already exists.";
            case AppConstraints.UNIQUE_ARTIFACT_TYPE_PER_PROJECT:
                return "Artifact type is already defined in project.";
            case AppConstraints.SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET:
                return "Found duplicate trace link defined between source and target.";
            case AppConstraints.UNIQUE_ARTIFACT_BODY_PER_VERSION:
                return "Found duplicate version of given artifact.";
            case AppConstraints.UNIQUE_VERSION_ID_PER_PROJECT:
                return "version already exists in project.";
            case AppConstraints.SINGLE_ROLE_PER_PROJECT:
                return "A user with given email already exists in the project.";
            case AppConstraints.SINGLE_TRACE_VERSION_PER_PROJECT_VERSION:
                return "This trace link already contains an entry for this project version";
            case AppConstraints.UNIQUE_TRACE_MATRIX_PER_PROJECT:
                return "Trace matrix between given types is already created";
            case AppConstraints.UNIQUE_ARTIFACT_PER_DOCUMENT:
                return "This artifact has already been added to this document.";
            case AppConstraints.UNIQUE_EMAIL:
                return "Email is already registered under some other account.";
            case AppConstraints.UNIQUE_ARTIFACT_PARENT_PER_FTA_ARTIFACT:
                return "Attempted to create FTA artifact already associated with another FTA artifact.";
            case AppConstraints.UNIQUE_ARTIFACT_PARENT_PER_SAFETY_ARTIFACT:
                return "Attempted to create Safety artifact already associated with another Safety artifact.";
            case AppConstraints.NULL_VALUE:
                return createNullError(cause);
            case AppConstraints.UNIQUE_MODEL_PROJECT_RECORD:
                return "Model is already associated with project, second record of this was attempted.";
            case AppConstraints.UNIQUE_KEYNAME_PER_PROJECT:
                return "Key already exists within this artifact type.";
            default:
                throw new SafaError("Database constraint was violated. %s", cause);
        }
    }

    private static String createNullError(String cause) {
        // accounts for space and start quote
        int startIndex = cause.indexOf(AppConstraints.NULL_VALUE) + AppConstraints.NULL_VALUE.length() + 2; //
        int endIndex = cause.indexOf("\"", startIndex);
        String columnName = cause.substring(startIndex, endIndex);
        return String.format("Expected %s to have a non-null value.", columnName);
    }
}
