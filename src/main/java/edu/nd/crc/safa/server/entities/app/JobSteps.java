package edu.nd.crc.safa.server.entities.app;

import java.lang.reflect.Array;
import java.util.Arrays;
import java.util.stream.Stream;

import edu.nd.crc.safa.server.entities.api.jobs.JobType;

/**
 * Enumerates all the steps for each job
 */
public class JobSteps {

    private static final String[] flatFileProjectCreation = {
        "Parsing Artifact Files",
        "Parsing Trace Files",
        "Generating Traces",
    };
    private static final String[] projectCreationSteps = {
        "Saving Artifacts",
        "Saving Traces",
        "Generating Layout",
        "Done"
    };
    private static final String[] modelTrainingSteps = {
        "Gather related documents",
        "Create training data",
        "Model training",
        "Done"
    };
    public static String[] jiraProjectCreationSteps = {
        "Authenticate User Credentials",
        "Retrieve JIRA project",
        "Create SAFA Project",
        "Convert Issues To Artifacts And Trace Links"
    };

    public static String[] getJobSteps(JobType jobType) {
        switch (jobType) {
            case FLAT_FILE_PROJECT_CREATION:
                return concatWithStream(flatFileProjectCreation, projectCreationSteps);
            case JIRA_PROJECT_CREATION:
                return concatWithStream(jiraProjectCreationSteps, projectCreationSteps);
            case PROJECT_CREATION:
                return projectCreationSteps;
            case TRAIN_MODEL:
                return modelTrainingSteps;
            default:
                throw new RuntimeException(jobType + " is under development.");
        }
    }

    static <T> T[] concatWithStream(T[] array1, T[] array2) {
        return Stream.concat(Arrays.stream(array1), Arrays.stream(array2))
            .toArray(size -> (T[]) Array.newInstance(array1.getClass().getComponentType(), size));
    }
}
