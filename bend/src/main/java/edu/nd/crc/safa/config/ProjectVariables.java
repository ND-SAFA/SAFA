package edu.nd.crc.safa.config;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

/**
 * Holds constants to magic string variables that may arise
 * during development.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class ProjectVariables {
    public static final String TIM_FILENAME = "tim.json";
    public static final String EMPTY_TIM_CONTENT = "{\"artifacts\": [], \"traces\": []}";
    public static final String DATAFILES_PARAM = "datafiles";
    public static final double TRACE_THRESHOLD = 0.5;
    public static final boolean PROJECT_CREATION_AS_COMPLETE_SET = false;
    public static final String AS_COMPLETE_SET = "asCompleteSet";
    public static final String SUMMARIZE_ARTIFACTS = "summarizeArtifacts";
    public static final String ARTIFACT_EXISTS = "artifactExists";
}


