package edu.nd.crc.safa.features.commits.pipeline.steps;

import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactVersionRepository;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.commits.pipeline.ICommitStep;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.delta.entities.app.ProjectChange;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.javatuples.Pair;

public class CommitArtifacts implements ICommitStep {
    /**
     * Commits the artifact changes to project version.
     *
     * @param service          The commit service to access database and other services.
     * @param commitDefinition The commit being performed.
     * @param result           The commit final state.
     */
    @Override
    public void performStep(CommitService service, ProjectCommitDefinition commitDefinition,
                            ProjectCommitAppEntity result) {
        ProjectVersion projectVersion = commitDefinition.getCommitVersion();
        Pair<ProjectChange<ArtifactAppEntity>, List<CommitError>> artifactResponse = commitArtifactChanges(
            projectVersion,
            commitDefinition,
            service);

        result.setArtifacts(artifactResponse.getValue0());
        result.addErrors(artifactResponse.getValue1());
    }

    private Pair<ProjectChange<ArtifactAppEntity>, List<CommitError>> commitArtifactChanges(
        ProjectVersion projectVersion, ProjectCommitDefinition commit, CommitService commitService) throws SafaError {
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
