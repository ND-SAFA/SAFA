package edu.nd.crc.safa.features.commits.pipeline.steps;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.commits.pipeline.ICommitStep;
import edu.nd.crc.safa.features.commits.services.CommitService;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.services.TraceService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class AddTracesToDeletedArtifacts implements ICommitStep {
    /**
     * Adds any related active traces to deleted artifacts.
     *
     * @param service The commit service to access database and other services.
     * @param commit  The commit being performed.
     * @param after   The commit final state.
     */
    @Override
    public void performStep(CommitService service, ProjectCommit commit, ProjectCommit after) {
        ProjectVersion projectVersion = commit.getCommitVersion();
        TraceService traceService = service.getTraceService();
        List<UUID> artifactIds = commit.getArtifacts().getRemoved()
            .stream().map(ArtifactAppEntity::getId).collect(Collectors.toList());
        List<TraceAppEntity> linksToArtifact = traceService
            .getTracesRelatedToArtifacts(projectVersion, artifactIds);
        commit.addTraces(ModificationType.REMOVED, linksToArtifact);
    }
}
