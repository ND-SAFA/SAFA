package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.Optional;

import edu.nd.crc.safa.features.common.ProjectEntities;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssuesResponseDTO;
import edu.nd.crc.safa.features.jira.entities.db.JiraProject;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;

/**
 * Job to import a JIRA project into an existing SAFA project
 */
public class JiraProjectImportJob extends CreateProjectViaJiraJob {
    JiraConnectionService jiraConnectionService;

    public JiraProjectImportJob(JobDbEntity jobDbEntity,
                                ServiceProvider serviceProvider,
                                JiraIdentifier jiraIdentifier) {
        super(jobDbEntity, serviceProvider, jiraIdentifier);
        this.jiraConnectionService = this.serviceProvider.getJiraConnectionService();
    }

    @Override
    protected JiraProject getJiraProjectMapping(Project project, Long jiraProjectId) {
        Optional<JiraProject> optional = this.serviceProvider
            .getJiraProjectRepository()
            .findByProjectAndJiraProjectId(project, jiraProjectId);

        if (optional.isPresent()) {
            throw new SafaError("JIRA project already imported into this SAFA project");
        }

        return super.getJiraProjectMapping(project, jiraProjectId);
    }
}
