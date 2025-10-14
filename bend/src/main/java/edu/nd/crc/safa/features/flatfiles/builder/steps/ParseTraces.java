package edu.nd.crc.safa.features.flatfiles.builder.steps;

import java.util.List;
import java.util.Optional;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.EntityParsingResult;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.BuilderUtility;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderStore;
import edu.nd.crc.safa.features.flatfiles.parser.FlatFileParser;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntityType;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.TraceLink;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class ParseTraces implements IFlatFileBuilderStep {
    @Override
    public void perform(FlatFileBuilderStore state, ServiceProvider serviceProvider) throws Exception {
        FlatFileParser flatFileParser = state.getFlatFileParser();

        ProjectCommitDefinition projectCommitDefinition = state.getProjectCommitDefinition();
        ProjectVersion projectVersion = state.getProjectVersion();
        List<ArtifactAppEntity> artifactsAdded = state.getArtifactsAdded();

        EntityParsingResult<TraceAppEntity, String> traceCreationResponse = flatFileParser.parseTraces(artifactsAdded);
        List<TraceAppEntity> tracesAdded = traceCreationResponse.getEntities();

        for (TraceAppEntity traceAppEntity : tracesAdded) {
            Optional<TraceLink> linkOptional = serviceProvider
                .getTraceLinkRepository()
                .getByProjectAndSourceAndTarget(projectVersion.getProject(), traceAppEntity.getSourceName(),
                    traceAppEntity.getTargetName());

            if (linkOptional.isPresent()) {
                traceAppEntity.setId(linkOptional.get().getTraceLinkId());
            } else {
                traceAppEntity.setId(null);
            }
        }
        projectCommitDefinition.getTraces().setAdded(traceCreationResponse.getEntities());
        BuilderUtility.addErrorsToCommit(projectCommitDefinition,
            traceCreationResponse.getErrors(),
            ProjectEntityType.TRACES);
    }
}
