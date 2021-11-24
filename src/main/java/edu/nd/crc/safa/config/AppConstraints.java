package edu.nd.crc.safa.config;

import org.springframework.dao.DataIntegrityViolationException;

/**
 * The central container of all database constraints defined in project offering
 * translated messages.
 */
public class AppConstraints {

    public static final String UNIQUE_ARTIFACT_NAME_PER_PROJECT = "UNIQUE_ARTIFACT_NAME_PER_PROJECT";
    public static final String UNIQUE_ARTIFACT_TYPE_PER_PROJECT = "UNIQUE_ARTIFACT_TYPE_PER_PROJECT";
    public static final String SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET = "SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET";
    public static final String UNIQUE_ARTIFACT_BODY_PER_VERSION = "UNIQUE_ARTIFACT_BODY_PER_VERSION";
    public static final String UNIQUE_VERSION_ID_PER_PROJECT = "UNIQUE_VERSION_ID_PER_PROJECT";

    public static final String[] registeredConstraints = new String[]{
        UNIQUE_ARTIFACT_NAME_PER_PROJECT,
        UNIQUE_ARTIFACT_TYPE_PER_PROJECT,
        SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET,
        UNIQUE_ARTIFACT_BODY_PER_VERSION,
        UNIQUE_VERSION_ID_PER_PROJECT
    };

    public static String getConstraintError(DataIntegrityViolationException e) {
        String cause = e.getMostSpecificCause().toString();

        for (String constraintId : registeredConstraints) {
            if (cause.contains(constraintId)) {
                return getErrorMessage(constraintId);
            }
        }
        throw e;
    }

    private static String getErrorMessage(String constraintId) {
        switch (constraintId) {
            case UNIQUE_ARTIFACT_NAME_PER_PROJECT:
                return "artifact with given name already exists.";
            case UNIQUE_ARTIFACT_TYPE_PER_PROJECT:
                return "artifact type is already defined in project.";
            case SINGLE_TRACE_BETWEEN_SOURCE_AND_TARGET:
                return "found duplicate trace link defined between source and target.";
            case UNIQUE_ARTIFACT_BODY_PER_VERSION:
                return "found duplicate version of artifact.";
            case UNIQUE_VERSION_ID_PER_PROJECT:
                return "version already exists in project.";
            default:
                throw new RuntimeException("Constrain friendly name is not defined.");
        }
    }
}
