package edu.nd.crc.safa.config;

import org.springframework.dao.DataIntegrityViolationException;

/**
 * The central container of all database constraints defined in project offering
 * translated messages.
 */
public class AppConstraints {

    // Project Entities
    public static final String UNIQUE_ARTIFACT_NAME_PER_PROJECT = "UNIQUE_ARTIFACT_NAME_PER_PROJECT";
    public static final String UNIQUE_ARTIFACT_TYPE_PER_PROJECT = "UNIQUE_ARTIFACT_TYPE_PER_PROJECT";
    public static final String SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET = "SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET";
    public static final String UNIQUE_ARTIFACT_BODY_PER_VERSION = "UNIQUE_ARTIFACT_BODY_PER_VERSION";
    public static final String UNIQUE_VERSION_ID_PER_PROJECT = "UNIQUE_VERSION_ID_PER_PROJECT";

    //Permissions
    public static final String SINGLE_ROLE_PER_PROJECT = "SINGLE_ROLE_PER_PROJECT";

    //Generic
    public static final String NULL_VALUE = "NULL not allowed for column";

    public static final String[] registeredConstraints = new String[]{
        UNIQUE_ARTIFACT_NAME_PER_PROJECT,
        UNIQUE_ARTIFACT_TYPE_PER_PROJECT,
        SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET,
        UNIQUE_ARTIFACT_BODY_PER_VERSION,
        UNIQUE_VERSION_ID_PER_PROJECT,
        SINGLE_ROLE_PER_PROJECT,
        NULL_VALUE
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
            case UNIQUE_ARTIFACT_NAME_PER_PROJECT:
                return "artifact with given name already exists.";
            case UNIQUE_ARTIFACT_TYPE_PER_PROJECT:
                return "Artifact type is already defined in project.";
            case SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET:
                return "Found duplicate trace link defined between source and target.";
            case UNIQUE_ARTIFACT_BODY_PER_VERSION:
                return "Found duplicate version of given artifact.";
            case UNIQUE_VERSION_ID_PER_PROJECT:
                return "version already exists in project.";
            case SINGLE_ROLE_PER_PROJECT:
                return "A user with given email already exists in the project.";
            case NULL_VALUE:
                return createNullError(cause);
            default:
                throw new RuntimeException("Constrain friendly name is not defined.");
        }
    }

    private static String createNullError(String cause) {
        int startIndex = cause.indexOf(NULL_VALUE) + NULL_VALUE.length() + 2; // acounnts for space and start quote
        int endIndex = cause.indexOf("\"", startIndex);
        String columnName = cause.substring(startIndex, endIndex);
        return String.format("Expected %s to have a non-null value.", columnName);
    }
}
