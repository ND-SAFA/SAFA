package edu.nd.crc.safa.features.jobs.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.github.entities.app.GithubImportDTO;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GithubProjectCreationJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * Creates a job responsible for pulling and parsing a GitHub repository
 */
public class CreateProjectViaGithubBuilder extends AbstractJobBuilder {

    /**
     * Identifier GitHub project to import.
     */
    GithubIdentifier githubIdentifier;

    SafaUser user;

    GithubImportDTO githubImportDTO;

    public CreateProjectViaGithubBuilder(ServiceProvider serviceProvider, GithubIdentifier githubIdentifier,
                                         GithubImportDTO githubImportDTO, SafaUser user) {
        super(serviceProvider, user);
        this.githubIdentifier = githubIdentifier;
        this.user = user;
        this.githubImportDTO = githubImportDTO;
    }

    @Override
    protected AbstractJob constructJobForWork() {
        return new GithubProjectCreationJob(jobDbEntity, serviceProvider, githubIdentifier, githubImportDTO, user);
    }

    @Override
    protected String getJobName() {
        return GithubProjectCreationJob.createJobName(this.githubIdentifier);
    }

    @Override
    protected Class<? extends AbstractJob> getJobType() {
        return GithubProjectCreationJob.class;
    }
}
