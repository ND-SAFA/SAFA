package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jira.entities.api.JiraImportSettings;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssueDTO;
import edu.nd.crc.safa.features.jira.entities.db.JiraProject;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * Job to update an already imported JIRA project
 */
public class JiraProjectUpdateJob extends CreateProjectViaJiraJob {
    private final JiraConnectionService jiraConnectionService;

    public JiraProjectUpdateJob(JobDbEntity jobDbEntity,
                                ServiceProvider serviceProvider,
                                JiraIdentifier jiraIdentifier,
                                SafaUser user,
                                JiraImportSettings importSettings) {
        super(jobDbEntity, serviceProvider, jiraIdentifier, user, importSettings);
        this.jiraConnectionService = this.getServiceProvider().getJiraConnectionService();
        setProjectCommitDefinition(new ProjectCommitDefinition(user, jiraIdentifier.getProjectVersion(), false));
        getSkipSteps().add(CREATE_PROJECT_STEP_INDEX);
    }

    @Override
    public ProjectEntities retrieveJiraEntities() {
        List<JiraIssueDTO> issues = jiraConnectionService.retrieveUpdatedJIRAIssues(
            getCredentials(),
            getJiraIdentifier().getOrgId(),
            this.getJiraIdentifier().getJiraProjectId(),
            getJiraProject().getLastUpdate());

        return this.getServiceProvider()
            .getJiraParsingService()
            .parseProjectEntitiesFromIssues(issues);
    }

    @Override
    protected JiraProject getJiraProjectMapping(Project project, UUID orgId, Long jiraProjectId) {
        Optional<JiraProject> optional = this.getServiceProvider()
            .getJiraProjectRepository()
            .findByProjectAndJiraProjectId(project, jiraProjectId);

        if (optional.isEmpty()) {
            throw new SafaError("JIRA project is not mapped to this SAFA project");
        }

        return optional.get();
    }
}
