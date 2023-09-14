package edu.nd.crc.safa.features.commits.services.pipeline;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.commits.services.CommitService;

public interface ICommitStep {
    void performStep(CommitService service, ProjectCommit commit, ProjectCommit after);
}
