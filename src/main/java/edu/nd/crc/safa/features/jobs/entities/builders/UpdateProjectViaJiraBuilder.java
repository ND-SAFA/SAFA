package edu.nd.crc.safa.features.jobs.entities.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jobs.entities.app.JiraProjectCreationJob;
import edu.nd.crc.safa.features.jobs.entities.app.JiraProjectUpdateJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;

/**
 * Builds job for pulling issues from JIRA and updating project.
 */
public class UpdateProjectViaJiraBuilder extends CreateProjectViaJiraBuilder {

    public UpdateProjectViaJiraBuilder(ServiceProvider serviceProvider,
                                       JiraIdentifier jiraIdentifier) {
        super(serviceProvider, jiraIdentifier);
        if (jiraIdentifier.getProjectVersion() == null) {
            throw new IllegalArgumentException("Expected non-null project version when updating project.");
        }
    }

    @Override
    protected JiraIdentifier constructIdentifier() {
        return this.jiraIdentifier;
    }

    @Override
    JobDefinition constructJobForWork() {
        String jobName = JiraProjectCreationJob.createJobName(this.jiraIdentifier);
        JobDbEntity jobDbEntity = this.serviceProvider
            .getJobService()
            .createNewJob(JobType.JIRA_PROJECT_UPDATE, jobName);

        // Step - Create jira project creation job
        JiraProjectUpdateJob jiraProjectCreationjob = new JiraProjectUpdateJob(
            jobDbEntity,
            serviceProvider,
            this.identifier
        );
        return new JobDefinition(jobDbEntity, jiraProjectCreationjob);
    }
}
