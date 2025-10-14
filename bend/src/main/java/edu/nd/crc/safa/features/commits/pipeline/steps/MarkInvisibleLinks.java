package edu.nd.crc.safa.features.commits.pipeline.steps;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.commits.pipeline.ICommitStep;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;

public class MarkInvisibleLinks implements ICommitStep {
    /**
     * Marks any declined links as invisible.
     *
     * @param service          The commit service to access database and other services.
     * @param commitDefinition The commit being performed.
     * @param result           The commit final state.
     */
    @Override
    public void performStep(CommitService service, ProjectCommitDefinition commitDefinition,
                            ProjectCommitAppEntity result) {
        // Step - Mark decline trace links as invisible
        commitDefinition
            .getTraces()
            .getModified()
            .stream()
            .filter(t -> t.getApprovalStatus() == ApprovalStatus.DECLINED)
            .forEach(t -> t.setVisible(false));
    }
}
