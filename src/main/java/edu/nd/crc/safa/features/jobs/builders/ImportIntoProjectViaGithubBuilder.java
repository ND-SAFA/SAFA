package edu.nd.crc.safa.features.jobs.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GithubProjectImportJob;

/**
 * Creates a job responsible for importing a GitHub repository into an existing project
 */
public class ImportIntoProjectViaGithubBuilder extends CreateProjectViaGithubBuilder {

    public ImportIntoProjectViaGithubBuilder(ServiceProvider serviceProvider,
                                             GithubIdentifier githubIdentifier) {
        super(serviceProvider, githubIdentifier);

        if (githubIdentifier.getProjectVersion() == null) {
            throw new IllegalArgumentException(
                "Expected non-null project version when importing into project.");
        }
    }

    @Override
    protected GithubIdentifier constructIdentifier() {
        return this.githubIdentifier;
    }

    @Override
    AbstractJob constructJobForWork() {
        return new GithubProjectImportJob(
            jobDbEntity,
            serviceProvider,
            this.githubIdentifier
        );
    }
}
