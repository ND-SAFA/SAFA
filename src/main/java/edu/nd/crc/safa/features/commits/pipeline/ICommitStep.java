package edu.nd.crc.safa.features.commits.pipeline;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.commits.services.CommitService;

/**
 * Defines interface for all commit steps.
 */
public interface ICommitStep {
    /**
     * Performs a step in the commit pipeline.
     *
     * @param service The commit service to access database and other services.
     * @param commit  The commit being performed.
     * @param after   The commit final state.
     */
    void performStep(CommitService service, ProjectCommit commit, ProjectCommit after);
}
