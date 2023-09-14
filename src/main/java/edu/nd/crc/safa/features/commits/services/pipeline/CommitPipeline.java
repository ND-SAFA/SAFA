package edu.nd.crc.safa.features.commits.services.pipeline;

import java.util.List;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.commits.services.pipeline.steps.AddRelatedTraces;
import edu.nd.crc.safa.features.commits.services.pipeline.steps.CommitArtifacts;
import edu.nd.crc.safa.features.commits.services.pipeline.steps.CommitTraces;
import edu.nd.crc.safa.features.commits.services.pipeline.steps.MarkInvisibleLinks;
import edu.nd.crc.safa.features.commits.services.pipeline.steps.SendNotifications;
import edu.nd.crc.safa.features.commits.services.pipeline.steps.SetLastUpdated;

public class CommitPipeline {
    ProjectCommit before;
    List<ICommitStep> steps;

    public CommitPipeline(ProjectCommit projectCommit) {
        this.before = projectCommit;
        this.steps = List.of(
            new AddRelatedTraces(),
            new MarkInvisibleLinks(),
            new CommitArtifacts(),
            new CommitTraces(),
            new SetLastUpdated(),
            new SendNotifications()
        );
    }

    public ProjectCommit commit(CommitService commitService) {
        ProjectCommit after = new ProjectCommit();
        after.setCommitVersion(this.before.getCommitVersion());
        for (ICommitStep step : this.steps) {
            step.performStep(commitService, this.before, after);
        }
        return after;
    }
}
