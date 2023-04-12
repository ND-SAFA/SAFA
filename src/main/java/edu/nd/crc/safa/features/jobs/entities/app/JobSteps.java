package edu.nd.crc.safa.features.jobs.entities.app;

import java.util.List;

import edu.nd.crc.safa.features.jobs.JobExecutionUtilities;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

/**
 * Enumerates all the steps for each job
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class JobSteps {

    public static String[] jiraProjectCreationSteps = { // Not final because modified in some tests
        "Authenticate User Credentials",
        "Retrieve JIRA project",
        "Create SAFA Project",
        "Creating SAFA Project to Jira Project Mapping",
        "Importing Issues and Links",
        "Committing Entities",
        "Done"
    };

    public static List<String> getJobSteps(Class<? extends AbstractJob> jobType) {
        return JobExecutionUtilities.getJobStepNames(jobType);
    }
}
