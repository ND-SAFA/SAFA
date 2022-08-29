package edu.nd.crc.safa.features.jobs.entities.app;

import java.util.List;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

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
        switch (jobType) {
            case FLAT_FILE_PROJECT_CREATION:
                return AbstractJob.getJobSteps(FlatFileProjectCreationJob.class);
            case JIRA_PROJECT_CREATION:
                return AbstractJob.getJobSteps(CreateProjectViaJiraJob.class);
            case JIRA_PROJECT_UPDATE:
                return AbstractJob.getJobSteps(JiraProjectUpdateJob.class);
            case PROJECT_CREATION:
                return AbstractJob.getJobSteps(CommitJob.class);
            default:
                throw new SafaError("Unknown job type: %s.", jobType);
        }
    }
}
