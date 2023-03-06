package edu.nd.crc.safa.features.jobs.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GithubProjectUpdateJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

public class UpdateProjectViaGithubBuilder extends CreateProjectViaGithubBuilder {

    public UpdateProjectViaGithubBuilder(ServiceProvider serviceProvider,
                                         GithubIdentifier githubIdentifier,
                                         SafaUser user) {
        super(serviceProvider, githubIdentifier, user);

        if (githubIdentifier.getProjectVersion() == null) {
            throw new IllegalArgumentException("Expected non-null project version when updating project.");
        }
    }

    @Override
    protected GithubIdentifier constructIdentifier() {
        return this.githubIdentifier;
    }

    @Override
    AbstractJob constructJobForWork() {
        return new GithubProjectUpdateJob(
            jobDbEntity,
            serviceProvider,
            this.githubIdentifier
        );
    }
}
