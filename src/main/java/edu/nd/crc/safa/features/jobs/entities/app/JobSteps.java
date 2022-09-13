package edu.nd.crc.safa.features.jobs.entities.app;

import java.util.List;

import edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJiraJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJsonJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.FlatFileProjectCreationJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GenerateLinksJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GithubProjectCreationJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GithubProjectUpdateJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.JiraProjectUpdateJob;
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
            case PROJECT_CREATION_VIA_FLAT_FILE:
                return AbstractJob.getJobSteps(FlatFileProjectCreationJob.class);
            case PROJECT_CREATION_VIA_JIRA:
                return AbstractJob.getJobSteps(CreateProjectViaJiraJob.class);
            case PROJECT_CREATION_VIA_GITHUB:
                return AbstractJob.getJobSteps(GithubProjectCreationJob.class);
            case PROJECT_CREATION_VIA_JSON:
                return AbstractJob.getJobSteps(CreateProjectViaJsonJob.class);
            case PROJECT_UPDATE_VIA_JIRA:
                return AbstractJob.getJobSteps(JiraProjectUpdateJob.class);
            case PROJECT_UPDATE_VIA_GITHUB:
                return AbstractJob.getJobSteps(GithubProjectUpdateJob.class);
            case GENERATE_LINKS:
                return AbstractJob.getJobSteps(GenerateLinksJob.class);
            default:
                throw new SafaError("Unknown job type: %s.", jobType);
        }
    }
}
