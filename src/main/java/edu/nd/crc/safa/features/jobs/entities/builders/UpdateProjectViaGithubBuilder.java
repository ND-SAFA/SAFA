package edu.nd.crc.safa.features.jobs.entities.builders;

import java.io.IOException;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.jobs.entities.app.GithubProjectCreationJob;
import edu.nd.crc.safa.features.jobs.entities.app.GithubProjectUpdateJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;

public class UpdateProjectViaGithubBuilder extends CreateProjectViaGithubBuilder {

    public UpdateProjectViaGithubBuilder(ServiceProvider serviceProvider,
                                         GithubIdentifier githubIdentifier) {
        super(serviceProvider, githubIdentifier);

        if (githubIdentifier.getProjectVersion() == null) {
            throw new IllegalArgumentException("Expected non-null project version when updating project.");
        }
    }

    @Override
    protected GithubIdentifier constructIdentifier() {
        return this.githubIdentifier;
    }

    @Override
    JobDefinition constructJobForWork() throws IOException {
        String jobName = GithubProjectCreationJob.createJobName(this.githubIdentifier);
        JobDbEntity jobDbEntity = this.serviceProvider
            .getJobService()
            .createNewJob(JobType.GITHUB_PROJECT_UPDATE, jobName);

        // Step - Create jira project creation job
        GithubProjectUpdateJob githubProjectUpdateJob = new GithubProjectUpdateJob(
            jobDbEntity,
            serviceProvider,
            this.githubIdentifier
        );
        return new JobDefinition(jobDbEntity, githubProjectUpdateJob);
    }
}
