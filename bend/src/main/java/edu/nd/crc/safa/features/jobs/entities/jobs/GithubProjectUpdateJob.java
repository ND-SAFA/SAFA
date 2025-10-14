package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.github.entities.app.GithubCommitDiffResponseDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubImportDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.github.repositories.GithubProjectRepository;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import com.fasterxml.jackson.databind.JsonNode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Internal job responsible for updating an existing imported GitHub project
 */
public class GithubProjectUpdateJob extends GithubProjectCreationJob {

    private static final Logger log = LoggerFactory.getLogger(GithubProjectUpdateJob.class);

    public GithubProjectUpdateJob(SafaUser user,
                                  JobDbEntity jobDbEntity,
                                  ServiceProvider serviceProvider,
                                  GithubIdentifier githubIdentifier,
                                  GithubImportDTO githubImportDTO) {
        super(user, jobDbEntity, serviceProvider, githubIdentifier, githubImportDTO);
        setProjectCommitDefinition(new ProjectCommitDefinition(user, githubIdentifier.getProjectVersion(), false));
        getSkipSteps().add(CREATE_PROJECT_STEP_NUM);
    }

    @Override
    protected GithubProject getGithubProjectMapping(Project project) {
        GithubProjectRepository repository = this.getServiceProvider().getGithubProjectRepository();

        this.setGithubProject(repository.findByProjectAndOwnerAndRepositoryName(
            project,
            this.getGithubIdentifier().getRepositoryOwner(),
            this.getGithubIdentifier().getRepositoryName()
        ).orElseThrow(() -> new SafaError("Linked project not found")));

        applyImportSettings(project, this.getGithubProject());

        return this.getGithubProject();
    }

    @Override
    protected String getDefaultTypeName() {
        return this.getGithubProject().getArtifactType().getName();
    }

    @Override
    protected List<ArtifactAppEntity> getArtifacts(JobLogger logger) {
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        GithubConnectionService connectionService = getServiceProvider().getGithubConnectionService();
        GithubCommitDiffResponseDTO diffResponseDTO = connectionService.getDiffBetweenOldCommitAndHead(
            getCredentials(),
            getGithubProject().getOwner(),
            getGithubProject().getRepositoryName(),
            getGithubProject().getLastCommitSha(),
            getGithubProject().getBranch()
        );

        log.info("Retrieving diff");
        for (GithubCommitDiffResponseDTO.GithubFileDiffDTO diff : diffResponseDTO.getFiles()) {

            String path = diff.getFilename();
            if (shouldSkipFile(path)) {
                logger.log("%s will not be imported due to inclusion/exclusion criteria.", path);
                continue;
            }
            logger.log("Importing %s.", path);

            log.info(diff.toString());
            String type = diff.getStatus().name();
            String summary = diff.getSha();
            String body = diff.getBlobUrl();

            Map<String, JsonNode> attributes = getAttributes(path);

            ArtifactAppEntity artifact = new ArtifactAppEntity(
                null,
                type,
                path,
                summary,
                body,
                attributes
            );

            artifacts.add(artifact);
        }

        return artifacts;
    }
}
