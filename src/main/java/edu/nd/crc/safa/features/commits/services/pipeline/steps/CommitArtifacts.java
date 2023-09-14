package edu.nd.crc.safa.features.commits.services.pipeline.steps;

import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.commits.services.pipeline.ICommitStep;
import edu.nd.crc.safa.features.delta.entities.app.ProjectChange;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.javatuples.Pair;

public class CommitArtifacts implements ICommitStep {
    @Override
    public void performStep(CommitService service, ProjectCommit commit, ProjectCommit after) {
        ProjectVersion projectVersion = commit.getCommitVersion();
        Pair<ProjectChange<ArtifactAppEntity>, List<CommitError>> artifactResponse = commitArtifactChanges(
            projectVersion,
            commit,
            service);

        after.setArtifacts(artifactResponse.getValue0());
        after.addErrors(artifactResponse.getValue1());
    }

    private Pair<ProjectChange<ArtifactAppEntity>, List<CommitError>> commitArtifactChanges(
        ProjectVersion projectVersion, ProjectCommit commit, CommitService commitService) throws SafaError {
        ArtifactVersionRepository artifactVersionRepository = commitService.getArtifactVersionRepository();
        return commitService.commitEntityChanges(
            projectVersion,
            commit.getArtifacts(),
            artifactVersionRepository,
            artifactVersionRepository::retrieveAppEntityFromVersionEntity,
            commit.isFailOnError(),
            commit.getUser());
    }
}
