package edu.nd.crc.safa.features.jobs.entities.jobs;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.github.entities.app.GithubCommitDiffResponseDTO;
import edu.nd.crc.safa.features.github.entities.app.GithubImportDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.github.repositories.GithubProjectRepository;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
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

    public GithubProjectUpdateJob(JobDbEntity jobDbEntity,
                                  ServiceProvider serviceProvider,
                                  GithubIdentifier githubIdentifier,
                                  GithubImportDTO githubImportDTO,
                                  SafaUser user) {
        super(jobDbEntity, serviceProvider, githubIdentifier, githubImportDTO, user);
        setProjectCommit(new ProjectCommit(githubIdentifier.getProjectVersion(), false));
        getSkipSteps().add(CREATE_PROJECT_STEP_NUM);
    }

    @Override
    protected GithubProject getGithubProjectMapping(Project project) {
        GithubProjectRepository repository = this.serviceProvider.getGithubProjectRepository();

        this.githubProject = repository.findByProjectAndOwnerAndRepositoryName(
            project,
            this.githubIdentifier.getRepositoryOwner(),
            this.githubIdentifier.getRepositoryName()
        ).orElseThrow(() -> new SafaError("Linked project not found"));

        applyImportSettings(project, this.githubProject);

        return this.githubProject;
    }

    @Override
    protected String getDefaultTypeName() {
        return this.githubProject.getArtifactType().getName();
    }

    @Override
    protected List<ArtifactAppEntity> getArtifacts() {
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        GithubConnectionService connectionService = serviceProvider.getGithubConnectionService();
        GithubCommitDiffResponseDTO diffResponseDTO = connectionService.getDiffBetweenOldCommitAndHead(
            credentials,
            githubProject.getRepositoryName(),
            githubProject.getLastCommitSha(),
            githubProject.getBranch()
        );

        log.info("Retrieving diff");
        for (GithubCommitDiffResponseDTO.GithubFileDiffDTO diff : diffResponseDTO.getFiles()) {

            String path = diff.getFilename();
            if (shouldSkipFile(path)) {
                continue;
            }

            log.info(diff.toString());
            String type = diff.getStatus().name();
            String summary = diff.getSha();
            String body = diff.getBlobUrl();

            Map<String, JsonNode> attributes = getAttributes(path);
            String[] pathParts = path.split(Pattern.quote(File.separator));
            String name = pathParts[pathParts.length - 1];

            ArtifactAppEntity artifact = new ArtifactAppEntity(
                null,
                type,
                name,
                summary,
                body,
                DocumentType.ARTIFACT_TREE,
                attributes
            );

            artifacts.add(artifact);
        }

        return artifacts;
    }
}
