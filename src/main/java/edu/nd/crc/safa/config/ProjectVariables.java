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
    public static final String DATAFILES_PARAM = "datafiles";
    public static final int ARTIFACT_CONTENT_LENGTH = 1000000;
    public static final double TRACE_THRESHOLD = 0.5;
}


