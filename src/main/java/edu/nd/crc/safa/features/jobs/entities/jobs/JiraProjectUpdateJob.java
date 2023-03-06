package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssuesResponseDTO;
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
    JiraConnectionService jiraConnectionService;

    public JiraProjectUpdateJob(JobDbEntity jobDbEntity,
                                ServiceProvider serviceProvider,
                                JiraIdentifier jiraIdentifier,
                                SafaUser user) {
        super(jobDbEntity, serviceProvider, jiraIdentifier, user);
        this.jiraConnectionService = this.serviceProvider.getJiraConnectionService();
    }

    @Override
    public ProjectEntities retrieveJiraEntities() {
        JiraIssuesResponseDTO dto = jiraConnectionService.retrieveUpdatedJIRAIssues(
            credentials,
            jiraIdentifier.getOrgId(),
            this.jiraIdentifier.getJiraProjectId(),
            jiraProject.getLastUpdate());

        return this.serviceProvider
            .getJiraParsingService()
            .parseProjectEntitiesFromIssues(dto.getIssues());
    }

    @Override
    protected JiraProject getJiraProjectMapping(Project project, UUID orgId, Long jiraProjectId) {
        Optional<JiraProject> optional = this.serviceProvider
                .getJiraProjectRepository()
                .findByProjectAndJiraProjectId(project, jiraProjectId);

        if (optional.isEmpty()) {
            throw new SafaError("JIRA project is not mapped to this SAFA project");
        }

        return optional.get();
    }
}
