package edu.nd.crc.safa.features.jobs.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.github.entities.app.GithubImportDTO;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GithubProjectUpdateJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

public class UpdateProjectViaGithubBuilder extends CreateProjectViaGithubBuilder {

    public UpdateProjectViaGithubBuilder(ServiceProvider serviceProvider,
                                         GithubIdentifier githubIdentifier,
                                         GithubImportDTO githubImportDTO,
                                         SafaUser user) {
        super(serviceProvider, githubIdentifier, githubImportDTO, user);

        if (githubIdentifier.getProjectVersion() == null) {
            throw new IllegalArgumentException("Expected non-null project version when updating project.");
        }
    }

    @Override
    protected AbstractJob constructJobForWork() {
        return new GithubProjectUpdateJob(
            getUser(),
            getJobDbEntity(),
            getServiceProvider(),
            getGithubIdentifier(),
            getGithubImportDTO()
        );
    }
}
