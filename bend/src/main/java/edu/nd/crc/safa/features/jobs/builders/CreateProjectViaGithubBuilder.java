package edu.nd.crc.safa.features.jobs.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.github.entities.app.GithubImportDTO;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.jobs.GithubProjectCreationJob;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AccessLevel;
import lombok.Getter;

/**
 * Creates a job responsible for pulling and parsing a GitHub repository
 */
public class CreateProjectViaGithubBuilder extends AbstractJobBuilder {

    /**
     * Identifier GitHub project to import.
     */
    @Getter(AccessLevel.PROTECTED)
    private final GithubIdentifier githubIdentifier;

    @Getter(AccessLevel.PROTECTED)
    private final GithubImportDTO githubImportDTO;

    public CreateProjectViaGithubBuilder(ServiceProvider serviceProvider, GithubIdentifier githubIdentifier,
                                         GithubImportDTO githubImportDTO, SafaUser user) {
        super(user, serviceProvider);
        this.githubIdentifier = githubIdentifier;
        this.githubImportDTO = githubImportDTO;
    }

    @Override
    protected AbstractJob constructJobForWork() {
        return new GithubProjectCreationJob(getUser(), getJobDbEntity(), getServiceProvider(), githubIdentifier,
            githubImportDTO);
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
