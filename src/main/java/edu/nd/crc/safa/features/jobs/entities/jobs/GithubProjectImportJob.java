package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.Optional;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.github.repositories.GithubProjectRepository;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;

/**
 * Responsible for providing step implementations for importing a GitHub project
 * into an existing SAFA project:
 * 1. Connecting to GitHub and accessing project
 * 2. Downloading the file tree for the selected branch
 * 3. Saving file paths as artifacts
 * 4. Returning project created
 */
public class GithubProjectImportJob extends GithubProjectCreationJob {

    public GithubProjectImportJob(JobDbEntity jobDbEntity,
                                  ServiceProvider serviceProvider,
                                  GithubIdentifier githubIdentifier) {
        super(jobDbEntity, serviceProvider, githubIdentifier);
    }

    @Override
    protected GithubProject getGithubProjectMapping(Project project) {
        GithubProjectRepository repository = this.serviceProvider.getGithubProjectRepository();
        Optional<GithubProject> githubProjectOptional = repository.findByProjectAndRepositoryName(
            project, this.githubIdentifier.getRepositoryName());

        if (githubProjectOptional.isPresent()) {
            throw new SafaError("Repository already imported");
        }

        return super.getGithubProjectMapping(project);
    }
}
