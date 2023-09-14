package edu.nd.crc.safa.features.commits.pipeline.steps;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.commits.pipeline.ICommitStep;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;

public class MarkInvisibleLinks implements ICommitStep {
    /**
     * Marks any declined links as invisible.
     *
     * @param service The commit service to access database and other services.
     * @param commit  The commit being performed.
     * @param after   The commit final state.
     */
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
