package edu.nd.crc.safa.features.commits.pipeline.steps;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.commits.pipeline.ICommitStep;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;

public class MarkInvisibleLinks implements ICommitStep {
    @Override
    public void performStep(CommitService service, ProjectCommit commit, ProjectCommit after) {
        // Step - Mark decline trace links as invisible
        commit
            .getTraces()
            .getModified()
            .stream()
            .filter(t -> t.getApprovalStatus() == ApprovalStatus.DECLINED)
            .forEach(t -> t.setVisible(false));
    }
}
