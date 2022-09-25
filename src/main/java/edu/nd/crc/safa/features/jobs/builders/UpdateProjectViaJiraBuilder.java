package edu.nd.crc.safa.features.jobs.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.JiraProjectUpdateJob;

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
    AbstractJob constructJobForWork() {
        return new JiraProjectUpdateJob(
            jobDbEntity,
            serviceProvider,
            this.identifier
        );
    }
}
