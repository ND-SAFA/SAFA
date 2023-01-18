package edu.nd.crc.safa.features.jobs.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.JiraProjectImportJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * Builds job for importing a JIRA project into an existing SAFA project
 */
public class ImportIntoProjectViaJiraBuilder extends CreateProjectViaJiraBuilder {

    public ImportIntoProjectViaJiraBuilder(ServiceProvider serviceProvider,
                                           JiraIdentifier jiraIdentifier,
                                           SafaUser user) {
        super(serviceProvider, jiraIdentifier, user);
        if (jiraIdentifier.getProjectVersion() == null) {
            throw new IllegalArgumentException(
                "Expected non-null project version when updating project.");
        }
    }

    @Override
    protected JiraIdentifier constructIdentifier() {
        return this.jiraIdentifier;
    }

    @Override
    AbstractJob constructJobForWork() {
        return new JiraProjectImportJob(
            jobDbEntity,
            serviceProvider,
            this.identifier,
            user
        );
    }
}
