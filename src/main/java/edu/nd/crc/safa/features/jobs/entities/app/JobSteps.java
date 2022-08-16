package edu.nd.crc.safa.features.jobs.entities.app;

import java.lang.reflect.Array;
import java.util.Arrays;
import java.util.stream.Stream;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

/**
 * Enumerates all the steps for each job
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
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
    public static String[] jiraProjectCreationSteps = { // Not final because modified in some tests
        "Authenticate User Credentials",
        "Retrieve JIRA project",
        "Create SAFA Project",
        "Convert Issues To Artifacts And Trace Links"
    };

    public static String[] githubProjectCreationSteps = {
        "Authenticate User Credentials",
        "Retrieve GitHub Repository",
        "Create SAFA Project",
        "Convert Filetree To Artifacts And TraceLinks"
    };

    public static String[] getJobSteps(JobType jobType) {
        switch (jobType) {
            case FLAT_FILE_PROJECT_CREATION:
                return concatWithStream(flatFileProjectCreation, projectCreationSteps);
            case JIRA_PROJECT_CREATION:
                return concatWithStream(jiraProjectCreationSteps, projectCreationSteps);
            case GITHUB_PROJECT_CREATION:
                return concatWithStream(githubProjectCreationSteps, projectCreationSteps);
            case PROJECT_CREATION:
                return projectCreationSteps;
            case TRAIN_MODEL:
                return modelTrainingSteps;
            default:
                throw new SafaError(jobType + " is under development.");
        }
    }

    static <T> T[] concatWithStream(T[] array1, T[] array2) {
        return Stream.concat(Arrays.stream(array1), Arrays.stream(array2))
            .toArray(size -> (T[]) Array.newInstance(array1.getClass().getComponentType(), size));
    }
}
