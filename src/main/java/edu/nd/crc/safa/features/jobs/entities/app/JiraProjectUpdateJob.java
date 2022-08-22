package edu.nd.crc.safa.features.jobs.entities.app;

import edu.nd.crc.safa.common.ProjectEntities;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssuesResponseDTO;
import edu.nd.crc.safa.features.jira.services.JiraConnectionService;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;

public class JiraProjectUpdateJob extends JiraProjectCreationJob {
    JiraConnectionService jiraConnectionService;

    public JiraProjectUpdateJob(JobDbEntity jobDbEntity,
                                ServiceProvider serviceProvider,
                                JiraIdentifier jiraIdentifier) {
        super(jobDbEntity, serviceProvider, jiraIdentifier);
        this.jiraConnectionService = this.serviceProvider.getJiraConnectionService();
    }

    @Override
    public ProjectEntities retrieveJiraEntities() {
        JiraIssuesResponseDTO dto = jiraConnectionService.retrieveUpdatedJIRAIssues(
            credentials,
            this.jiraIdentifier.getJiraProjectId(),
            jiraProject.getLastUpdate());

        return this.serviceProvider
            .getJiraParsingService()
            .parseProjectEntitiesFromIssues(dto.getIssues());
    }
}
