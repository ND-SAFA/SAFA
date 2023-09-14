package edu.nd.crc.safa.features.commits.services.pipeline.steps;

import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.commits.services.pipeline.ICommitStep;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.services.TraceService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class AddRelatedTraces implements ICommitStep {
    @Override
    public void performStep(CommitService service, ProjectCommit commit, ProjectCommit after) {
        ProjectVersion projectVersion = commit.getCommitVersion();
        TraceService traceService = service.getTraceService();
        // Step - Add related trace links to be removed.
        for (ArtifactAppEntity artifact : commit.getArtifacts().getRemoved()) {
            List<TraceAppEntity> linksToArtifact = traceService
                .getTracesInProjectVersionRelatedToArtifact(projectVersion, artifact.getName());
            commit.addTraces(ModificationType.REMOVED, linksToArtifact);
        }
    }
}
