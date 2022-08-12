package edu.nd.crc.safa.features.jobs.entities.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jobs.entities.app.JiraProjectCreationJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

/**
 * Builds job for pulling issues from JIRA and updating project.
 */
public class UpdateProjectByJiraJobBuilder extends AbstractJobBuilder<JiraIdentifier, String> {
    Long jiraProjectId;
    String cloudId;

    public UpdateProjectByJiraJobBuilder(
        ServiceProvider serviceProvider,
        Long jiraProjectId,
        String cloudId
    ) {
        super(serviceProvider);
        this.jiraProjectId = jiraProjectId;
        this.cloudId = cloudId;
    }

    @Override
    protected JiraIdentifier constructIdentifier() {
        Project project = new Project("", ""); // Set once parse starts
        this.serviceProvider.getProjectService().saveProjectWithCurrentUserAsOwner(project);
        ProjectVersion projectVersion = this.serviceProvider.getProjectService().createInitialProjectVersion(project);
        return new JiraIdentifier(projectVersion, this.jiraProjectId, this.cloudId);
    }

    @Override
    protected String constructJobWork(JiraIdentifier input) {
        return null;
    }

    @Override
    JobDefinition constructJobForWork(String change) {
        String jobName = JiraProjectCreationJob.createJobName(jiraProjectId.toString());
        JobDbEntity jobDbEntity = this.serviceProvider
            .getJobService()
            .createNewJob(JobType.JIRA_PROJECT_CREATION, jobName);

        // Step - Create jira project creation job
        JiraProjectCreationJob jiraProjectCreationjob = new JiraProjectCreationJob(
            jobDbEntity,
            serviceProvider,
            this.identifier
        );
        return new JobDefinition(jobDbEntity, jiraProjectCreationjob);
    }
}
