package edu.nd.crc.safa.server.entities.app;

import edu.nd.crc.safa.server.entities.api.JobType;

/**
 * Enumerates all the steps for each job
 */
public class JobSteps {

    private static final String[] projectCreationSteps = {
        "Artifact creation",
        "Trace creation",
        "Trace generation",
        "Layout generation"
    };

    private static final String[] modelTrainingSteps = {
        "Gather related documents",
        "Create training data",
        "Model training"
    };

    public static String[] getJobSteps(JobType jobType) {
        switch (jobType) {
            case PROJECT_CREATION:
                return projectCreationSteps;
            case TRAIN_MODEL:
                return modelTrainingSteps;
            default:
                throw new RuntimeException(jobType + " is under development.");
        }
    }
}
