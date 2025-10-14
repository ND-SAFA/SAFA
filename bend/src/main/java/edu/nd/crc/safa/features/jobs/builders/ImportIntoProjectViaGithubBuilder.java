package edu.nd.crc.safa.features.jobs.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.github.entities.app.GithubImportDTO;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GithubProjectImportJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * Creates a job responsible for importing a GitHub repository into an existing project
 */
public class ImportIntoProjectViaGithubBuilder extends CreateProjectViaGithubBuilder {

    public ImportIntoProjectViaGithubBuilder(ServiceProvider serviceProvider,
                                             GithubIdentifier githubIdentifier,
                                             GithubImportDTO githubImportDTO,
                                             SafaUser user) {
        super(serviceProvider, githubIdentifier, githubImportDTO, user);

        if (githubIdentifier.getProjectVersion() == null) {
            throw new IllegalArgumentException(
                "Expected non-null project version when importing into project.");
        }
    }

    @Override
    protected AbstractJob constructJobForWork() {
        return new GithubProjectImportJob(
            getUser(),
            getJobDbEntity(),
            getServiceProvider(),
            getGithubIdentifier(),
            getGithubImportDTO()
        );
    }
}
