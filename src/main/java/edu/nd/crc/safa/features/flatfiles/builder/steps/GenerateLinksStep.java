package edu.nd.crc.safa.features.flatfiles.builder.steps;

import java.util.List;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.builder.FlatFileBuilderStore;
import edu.nd.crc.safa.features.generation.tgen.entities.TGenRequestAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

public class GenerateLinksStep implements IFlatFileBuilderStep {
    @Override
    public void perform(FlatFileBuilderStore state, ServiceProvider serviceProvider) throws Exception {
        ProjectCommitDefinition projectCommitDefinition = state.getProjectCommitDefinition();
        ProjectVersion projectVersion = state.getProjectVersion();
        TGenRequestAppEntity TGenRequestAppEntity = state.getFlatFileParser().getTGenRequestAppEntity();

        // Step - Generate trace link requests (post-artifact construction if successful)
        ProjectAppEntity projectAppEntity = new ProjectAppEntity(projectCommitDefinition);
        List<TraceAppEntity> generatedLinks = serviceProvider.getTraceGenerationService().generateTraceLinks(
            TGenRequestAppEntity,
            projectAppEntity
        );

        generatedLinks = serviceProvider.getTraceGenerationService().removeOverlappingLinks(
            projectCommitDefinition.getTraces().getAdded(),
            generatedLinks);

        for (TraceAppEntity traceAppEntity : generatedLinks) {
            serviceProvider
                .getTraceLinkRepository()
                .getByProjectAndSourceAndTarget(
                    projectVersion.getProject(),
                    traceAppEntity.getSourceName(), traceAppEntity.getTargetName())
                .ifPresent(t -> traceAppEntity.setId(t.getTraceLinkId()));
        }
    }
}
