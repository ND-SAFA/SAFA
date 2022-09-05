package edu.nd.crc.safa.features.jobs.entities.builders;

import java.io.IOException;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.jobs.entities.app.GithubProjectCreationJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

/**
 * Creates a job responsible for pulling and parsing a GitHub repository
 */
public class CreateProjectViaGithubBuilder extends AbstractJobBuilder<GithubIdentifier> {

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
    JobDefinition constructJobForWork() throws IOException {
        String jobName = GithubProjectCreationJob.createJobName(this.githubIdentifier);
        JobDbEntity jobDbEntity = this.serviceProvider
            .getJobService()
            .createNewJob(JobType.GITHUB_PROJECT_CREATION, jobName);
        GithubProjectCreationJob job = new GithubProjectCreationJob(jobDbEntity,
            serviceProvider, this.githubIdentifier);

        return new JobDefinition(jobDbEntity, job);
    }
}
