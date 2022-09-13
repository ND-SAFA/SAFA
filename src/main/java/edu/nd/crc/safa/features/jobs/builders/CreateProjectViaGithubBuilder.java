package edu.nd.crc.safa.features.jobs.builders;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.jobs.GithubProjectCreationJob;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

/**
 * Creates a job responsible for pulling and parsing a GitHub repository
 */
public class CreateProjectViaGithubBuilder extends AbstractJobBuilder<GithubIdentifier> {

    /**
     * Identifier GitHub project to import.
     */
    GithubIdentifier githubIdentifier;

    public CreateProjectViaGithubBuilder(
        ServiceProvider serviceProvider,
        GithubIdentifier githubIdentifier) {
        super(serviceProvider);
        this.githubIdentifier = githubIdentifier;
    }

    @Override
    protected GithubIdentifier constructIdentifier() {
        Project project = new Project("", "");

        this.serviceProvider.getProjectService().saveProjectWithCurrentUserAsOwner(project);
        ProjectVersion projectVersion = this.serviceProvider.getVersionService().createInitialProjectVersion(project);
        this.githubIdentifier.setProjectVersion(projectVersion);
        return this.githubIdentifier;
    }

    @Override
    AbstractJob constructJobForWork() {
        return new GithubProjectCreationJob(this.jobDbEntity, serviceProvider, this.githubIdentifier);
    }

    @Override
    String getJobName() {
        return GithubProjectCreationJob.createJobName(this.githubIdentifier);
    }

    @Override
    JobType getJobType() {
        return JobType.PROJECT_CREATION_VIA_GITHUB;
    }
}
