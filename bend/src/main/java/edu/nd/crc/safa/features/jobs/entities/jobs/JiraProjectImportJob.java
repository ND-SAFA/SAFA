package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jira.entities.api.JiraImportSettings;
import edu.nd.crc.safa.features.jira.entities.db.JiraProject;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * Job to import a JIRA project into an existing SAFA project
 */
public class JiraProjectImportJob extends CreateProjectViaJiraJob {

    public JiraProjectImportJob(JobDbEntity jobDbEntity,
                                ServiceProvider serviceProvider,
                                JiraIdentifier jiraIdentifier,
                                SafaUser user,
                                JiraImportSettings importSettings) {
        super(jobDbEntity, serviceProvider, jiraIdentifier, user, importSettings);
        setProjectCommitDefinition(new ProjectCommitDefinition(user, jiraIdentifier.getProjectVersion(), false));
        getSkipSteps().add(CREATE_PROJECT_STEP_INDEX);
    }

    @Override
    protected JiraProject getJiraProjectMapping(Project project, UUID orgId, Long jiraProjectId) {
        Optional<JiraProject> optional = this.getServiceProvider()
            .getJiraProjectRepository()
            .findByProjectAndJiraProjectId(project, jiraProjectId);

        if (optional.isPresent()) {
            throw new SafaError("JIRA project already imported into this SAFA project");
        }

        return super.getJiraProjectMapping(project, orgId, jiraProjectId);
    }
}
