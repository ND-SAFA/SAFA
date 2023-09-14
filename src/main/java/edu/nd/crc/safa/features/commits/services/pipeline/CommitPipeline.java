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
    ProjectCommit commit;
    List<ICommitStep> steps;

    public CommitPipeline(ProjectCommit projectCommit) {
        this.commit = projectCommit;
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
        after.setCommitVersion(this.commit.getCommitVersion());
        for (ICommitStep step : this.steps) {
            step.performStep(commitService, this.commit, after);
        }
        return after;
    }
}
