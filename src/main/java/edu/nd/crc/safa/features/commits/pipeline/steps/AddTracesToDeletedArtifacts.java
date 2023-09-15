package edu.nd.crc.safa.features.commits.pipeline.steps;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
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
     * @param service          The commit service to access database and other services.
     * @param commitDefinition The commit being performed.
     * @param result           The commit final state.
     */
    @Override
    public void performStep(CommitService service, ProjectCommitDefinition commitDefinition,
                            ProjectCommitAppEntity result) {
        ProjectVersion projectVersion = commitDefinition.getCommitVersion();
        TraceService traceService = service.getTraceService();
        List<UUID> artifactIds = commitDefinition.getArtifacts().getRemoved()
            .stream().map(ArtifactAppEntity::getId).collect(Collectors.toList());
        List<TraceAppEntity> linksToArtifact = traceService
            .getTracesRelatedToArtifacts(projectVersion, artifactIds);
        commitDefinition.addTraces(ModificationType.REMOVED, linksToArtifact);
    }
}
