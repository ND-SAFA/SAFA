package edu.nd.crc.safa.features.jobs.entities.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jobs.entities.app.CreateProjectViaJiraJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
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
    JobDefinition constructJobForWork() {
        String jobName = CreateProjectViaJiraJob.createJobName(this.jiraIdentifier);
        JobDbEntity jobDbEntity = this.serviceProvider
            .getJobService()
            .createNewJob(JobType.JIRA_PROJECT_CREATION, jobName);

        // Step - Create jira project creation job
        CreateProjectViaJiraJob createProjectCreationjob = new CreateProjectViaJiraJob(
            jobDbEntity,
            serviceProvider,
            this.identifier
        );
        return new JobDefinition(jobDbEntity, createProjectCreationjob);
    }
}
