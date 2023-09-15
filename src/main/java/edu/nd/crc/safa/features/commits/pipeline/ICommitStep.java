package edu.nd.crc.safa.features.commits.pipeline;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.commits.services.CommitService;

/**
 * Defines interface for all commit steps.
 */
public interface ICommitStep {
    /**
     * Performs a step in the commit pipeline.
     *
     * @param service          The commit service to access database and other services.
     * @param commitDefinition The definition of the commit to perform.
     * @param result           The result of the commit.
     */
    void performStep(CommitService service, ProjectCommitDefinition commitDefinition, ProjectCommitAppEntity result);
}
