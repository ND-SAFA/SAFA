package edu.nd.crc.safa.features.commits.pipeline;

import java.util.List;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.commits.pipeline.steps.AddTracesToDeletedArtifacts;
import edu.nd.crc.safa.features.commits.pipeline.steps.CommitArtifacts;
import edu.nd.crc.safa.features.commits.pipeline.steps.CommitTraces;
import edu.nd.crc.safa.features.commits.pipeline.steps.MarkInvisibleLinks;
import edu.nd.crc.safa.features.commits.pipeline.steps.SendNotifications;
import edu.nd.crc.safa.features.commits.pipeline.steps.SetLastUpdated;
import edu.nd.crc.safa.features.commits.services.CommitService;

/**
 * Contains the order of steps to be performed for each commit.
 */
public class CommitPipeline {
    private final ProjectCommitDefinition commit;
    private final List<ICommitStep> steps;

    public CommitPipeline(ProjectCommitDefinition projectCommitDefinition) {
        this.commit = projectCommitDefinition;
        this.steps = List.of(
            new AddTracesToDeletedArtifacts(),
            new MarkInvisibleLinks(),
            new CommitArtifacts(),
            new CommitTraces(),
            new SetLastUpdated(),
            new SendNotifications()
        );
    }

    /**
     * Runs the commit steps using service.
     *
     * @param commitService Provides access to services and other resources.
     * @return The processed commit.
     */
    public ProjectCommitAppEntity commit(CommitService commitService) {
        ProjectCommitAppEntity result = new ProjectCommitAppEntity();
        result.setCommitVersion(this.commit.getCommitVersion());
        for (ICommitStep step : this.steps) {
            step.performStep(commitService, this.commit, result);
        }
        return result;
    }
}
