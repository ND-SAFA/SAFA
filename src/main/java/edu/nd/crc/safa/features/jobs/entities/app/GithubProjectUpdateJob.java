package edu.nd.crc.safa.features.jobs.entities.app;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.github.entities.api.GithubIdentifier;
import edu.nd.crc.safa.features.github.entities.app.GithubCommitDiffResponseDTO;
import edu.nd.crc.safa.features.github.entities.db.GithubProject;
import edu.nd.crc.safa.features.github.repositories.GithubProjectRepository;
import edu.nd.crc.safa.features.github.services.GithubConnectionService;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Internal job responsible for updating an existing imported GitHub project
 */
public class GithubProjectUpdateJob extends GithubProjectCreationJob {

    private static final Logger log = LoggerFactory.getLogger(GithubProjectUpdateJob.class);

    public GithubProjectUpdateJob(JobDbEntity jobDbEntity,
                                  ServiceProvider serviceProvider,
                                  GithubIdentifier githubIdentifier) {
        super(jobDbEntity, serviceProvider, githubIdentifier);
    }

    @Override
    protected GithubProject getGithubProjectMapping(Project project) {
        GithubProjectRepository repository = this.serviceProvider.getGithubProjectRepository();

        this.githubProject = repository.findByProjectAndRepositoryName(
            project,
            this.githubIdentifier.getRepositoryName()
        ).orElseThrow(() -> new SafaError("Linked project not found"));
        return this.githubProject;
    }

    @Override
    protected List<ArtifactAppEntity> getArtifacts() {
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        GithubConnectionService connectionService = serviceProvider.getGithubConnectionService();
        GithubCommitDiffResponseDTO diffResponseDTO = connectionService.getDiffBetweenOldCommitAndHead(
            credentials,
            githubProject.getRepositoryName(),
            githubProject.getLastCommitSha()
        );

        for (GithubCommitDiffResponseDTO.GithubFileDiffDTO diff: diffResponseDTO.getFiles()) {
            log.info(diff.toString());
            String name = diff.getFilename();
            String type = diff.getStatus().name();
            String summary = diff.getSha();
            String body = diff.getBlobUrl();

            ArtifactAppEntity artifact = new ArtifactAppEntity(
                "",
                type,
                name,
                summary,
                body,
                DocumentType.ARTIFACT_TREE,
                new Hashtable<>()
            );

            artifacts.add(artifact);
        }

        return artifacts;
    }
}
