package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.Optional;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.github.entities.app.GithubImportDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.github.repositories.GithubProjectRepository;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * Responsible for providing step implementations for importing a GitHub project
 * into an existing SAFA project:
 * 1. Connecting to GitHub and accessing project
 * 2. Downloading the file tree for the selected branch
 * 3. Saving file paths as artifacts
 * 4. Returning project created
 */
public class GithubProjectImportJob extends GithubProjectCreationJob {

    public GithubProjectImportJob(SafaUser projectOwner,
                                  JobDbEntity jobDbEntity,
                                  ServiceProvider serviceProvider,
                                  GithubIdentifier githubIdentifier,
                                  GithubImportDTO githubImportDTO) {
        super(projectOwner, jobDbEntity, serviceProvider, githubIdentifier, githubImportDTO);
        setProjectCommitDefinition(new ProjectCommitDefinition(projectOwner, githubIdentifier.getProjectVersion(),
            false));
        getSkipSteps().add(CREATE_PROJECT_STEP_NUM);
    }

    @Override
    protected GithubProject getGithubProjectMapping(Project project) {
        GithubProjectRepository repository = this.getServiceProvider().getGithubProjectRepository();
        Optional<GithubProject> githubProjectOptional = repository.findByProjectAndOwnerAndRepositoryName(
            project, this.getGithubIdentifier().getRepositoryOwner(), this.getGithubIdentifier().getRepositoryName());

        if (githubProjectOptional.isPresent()) {
            throw new SafaError("Repository already imported");
        }

        return super.getGithubProjectMapping(project);
    }
}
