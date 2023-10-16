package edu.nd.crc.safa.features.jobs.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jira.entities.api.JiraImportSettings;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.JiraProjectUpdateJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * Builds job for pulling issues from JIRA and updating project.
 */
public class UpdateProjectViaJiraBuilder extends CreateProjectViaJiraBuilder {

    public UpdateProjectViaJiraBuilder(ServiceProvider serviceProvider,
                                       JiraIdentifier jiraIdentifier,
                                       SafaUser user,
                                       JiraImportSettings importSettings) {
        super(serviceProvider, jiraIdentifier, user, importSettings);
        if (jiraIdentifier.getProjectVersion() == null) {
            throw new IllegalArgumentException("Expected non-null project version when updating project.");
        }
    }

    @Override
    protected AbstractJob constructJobForWork() {
        return new JiraProjectUpdateJob(
            getJobDbEntity(),
            getServiceProvider(),
            this.getJiraIdentifier(),
            getUser(),
            getImportSettings()
        );
    }
}
