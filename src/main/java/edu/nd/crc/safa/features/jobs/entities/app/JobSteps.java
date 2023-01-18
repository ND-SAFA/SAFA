package edu.nd.crc.safa.features.jobs.entities.app;

import java.util.List;

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
        "Convert Issues To Artifacts And Trace Links"
    };

    public static List<String> getJobSteps(JobType jobType) {
        return AbstractJob.getJobSteps(jobType.getJobClass());
    }
}
