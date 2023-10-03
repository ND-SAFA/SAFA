package edu.nd.crc.safa.features.flatfiles.builder.steps;

import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.EntityParsingResult;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.BuilderUtility;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderArgs;
import edu.nd.crc.safa.features.flatfiles.parser.FlatFileParser;
import edu.nd.crc.safa.features.flatfiles.parser.TimFileParser;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntityType;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class ParseTraces implements IFlatFileBuilderStep {
    @Override
    public void perform(FlatFileBuilderArgs state, ServiceProvider serviceProvider) throws Exception {
        FlatFileParser flatFileParser = state.getFlatFileParser();
        TimFileParser timFileParser = state.getTimFileParser();
        ProjectCommitDefinition projectCommitDefinition = state.getProjectCommitDefinition();
        ProjectVersion projectVersion = state.getProjectVersion();
        List<ArtifactAppEntity> artifactsAdded = state.getArtifactsAdded();

        EntityParsingResult<TraceAppEntity, String> traceCreationResponse = flatFileParser.parseTraces(artifactsAdded);
        List<TraceAppEntity> tracesAdded = traceCreationResponse.getEntities();

        for (TraceAppEntity traceAppEntity : tracesAdded) {
            serviceProvider.getTraceLinkRepository().getByProjectAndSourceAndTarget(projectVersion.getProject(),
                traceAppEntity.getSourceName(), traceAppEntity.getTargetName()).ifPresent(t -> traceAppEntity.setId(t.getTraceLinkId()));
        }
        projectCommitDefinition.getTraces().setAdded(traceCreationResponse.getEntities());
        BuilderUtility.addErrorsToCommit(projectCommitDefinition,
            traceCreationResponse.getErrors(),
            ProjectEntityType.TRACES);
    }
}
