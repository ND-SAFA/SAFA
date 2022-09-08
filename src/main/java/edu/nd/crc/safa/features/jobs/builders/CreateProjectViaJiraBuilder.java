package edu.nd.crc.safa.features.jobs.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJiraJob;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

/**
 * Builds job for pulling issues from JIRA and updating project.
 */
public class CreateProjectViaJiraBuilder extends AbstractJobBuilder<JiraIdentifier> {
    JiraIdentifier jiraIdentifier;

    public CreateProjectViaJiraBuilder(
        ServiceProvider serviceProvider,
        JiraIdentifier jiraIdentifier
    ) {
        super(serviceProvider);
        this.jiraIdentifier = jiraIdentifier;
    }

    @Override
    protected JiraIdentifier constructIdentifier() {
        Project project = new Project("", ""); // Set once parse starts
        this.serviceProvider.getProjectService().saveProjectWithCurrentUserAsOwner(project);
        ProjectVersion projectVersion = this.serviceProvider.getVersionService().createInitialProjectVersion(project);
        this.jiraIdentifier.setProjectVersion(projectVersion);
        return this.jiraIdentifier;
    }

    @Override
    AbstractJob constructJobForWork() {
        // Step - Create jira project creation job
        return new CreateProjectViaJiraJob(
            this.jobDbEntity,
            serviceProvider,
            this.identifier
        );
    }

    @Override
    String getJobName() {
        return CreateProjectViaJiraJob.createJobName(this.identifier);
    }

    @Override
    JobType getJobType() {
        return JobType.JIRA_PROJECT_CREATION;
    }
}
